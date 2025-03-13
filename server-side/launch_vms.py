import asyncio
import json
import uuid
import aiohttp
import asyncssh
import re
import paramiko
import time
import argparse

import dotenv
import os

receive_lock = asyncio.Lock()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Launch VMs with specified parameters")
    parser.add_argument("--env", required=True, help="Env")
    parser.add_argument("--prefix", required=True, help="Event Prefix")
    parser.add_argument("--team", required=True, help="Team Description")
    parser.add_argument("--network_uuid", required=True, help="Network UUID")
    parser.add_argument("--config", required=True, help="Path to config file")
    parser.add_argument("--subnet", required=True, help="Subnet prefix (e.g., 10.1.1)")
    parser.add_argument("--interface_name", required=True, help="Interface name (e.g., eth0)")
    parser.add_argument("--commands", nargs='+', required=True, help="List of commands to execute on each VM")
    return parser.parse_args()



async def send_rpc(ws, method, params):
    async with receive_lock:  
        request_id = str(uuid.uuid4())
        request = {"jsonrpc": "2.0", "method": method, "params": params, "id": request_id}
        await ws.send_str(json.dumps(request))

        while True:
            msg = await ws.receive()
            if msg.type == aiohttp.WSMsgType.TEXT:
                response = json.loads(msg.data)
                if response.get("id") == request_id:
                    return response
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
    return None



async def create_vm(ws, vm_name, template_uuid):
    """Creates the VM with two VIFs (VIF0=Challenge Network, VIF1=SSH)"""
    params = {
        "name_label": vm_name,
        "name_description": DEFAULT_VM_DESCRIPTION,
        "template": template_uuid,
        "bootAfterCreate": True,
        "VIFs": [
            {"network": NETWORK_UUID},  # VIF0: Main network (eth0)
            {"network": TEMP_NETWORK_UUID}  # VIF1: Temporary SSH access
        ]
    }
    response = await send_rpc(ws, "vm.create", params)
    return response.get("result") if response else None


async def wait_for_vm_ready(ws, vm_id, max_retries=30, delay=20):
    for attempt in range(1, max_retries + 1):
        response = await send_rpc(ws, "xo.getAllObjects", {"filter": {"id": vm_id}})
        if response and "result" in response:
            vm_info = response["result"].get(vm_id, {})
            power_state = vm_info.get("power_state", "")
            if power_state == "Running":
                addresses = vm_info.get("addresses", {})
                if addresses:
                    print(f"[DEBUG] VM {vm_id} is fully booted and IP assigned.")
                    return True
                else:
                    print(f"[DEBUG] VM {vm_id} is running but no IP yet. Retrying ({attempt}/{max_retries})...")
        await asyncio.sleep(delay)
    print(f"[ERROR] VM {vm_id} did not fully boot in time.")
    return False

async def get_vm_ip(ws, vm_id, max_retries=30, delay=20):
    for attempt in range(1, max_retries + 1):
        response = await send_rpc(ws, "xo.getAllObjects", {"filter": {"id": vm_id}})
        if response and "result" in response:
            vm_info = response["result"].get(vm_id, {})
            addresses = vm_info.get("addresses", {})
            for key, ip in addresses.items():
                if "/ipv4/" in key:
                    return ip 
        await asyncio.sleep(delay)
    return None

async def wait_for_ssh(ip, max_retries=20, delay=10):
    for attempt in range(1, max_retries + 1):
        try:
            async with asyncssh.connect(ip, username=SSH_USER, password=SSH_PASSWORD, known_hosts=None) as conn:
                print(f"[DEBUG] SSH is available on {ip}")
                return True
        except Exception:
            print(f"[DEBUG] Waiting for SSH on {ip}... Attempt {attempt}/{max_retries}")
            await asyncio.sleep(delay)
    return False

def execute_commands(VM_IP, commands):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"[DEBUG] Connecting to {VM_IP} as {SSH_USER}...")
        ssh.connect(VM_IP, username=SSH_USER, password=SSH_PASSWORD)

        shell = ssh.invoke_shell()
        time.sleep(1)  
        initial_output = shell.recv(1024).decode()
        print(f"[DEBUG] Initial Shell Output:\n{initial_output}")

        for command in commands:
            print(f"[DEBUG] Executing: {command}")
            shell.send(command + "\n")
            time.sleep(1)  
            output = shell.recv(4096).decode()
            print(f"[DEBUG] Command Output:\n{output}")

            if "[sudo] password for" in output:
                print("[DEBUG] Detected sudo password prompt, entering password...")
                shell.send(SSH_PASSWORD + "\n")
                time.sleep(1)  
                output = shell.recv(4096).decode()
                print(f"[DEBUG] Post-Password Output:\n{output}")

        ssh.close()
        print(f"[DEBUG] Commands executed successfully!")

    except paramiko.AuthenticationException:
        print("[ERROR] Authentication failed, please check credentials.")
    except paramiko.SSHException as sshException:
        print(f"[ERROR] Unable to establish SSH connection: {sshException}")
    except Exception as e:
        print(f"[ERROR] General error: {e}")


async def configure_vm_network(ws, vm_id, static_ip, gateway,interface_name, commands):
    """Creates an asyncio task for network configuration"""
    return asyncio.create_task(configure_vm_network_async(ws, vm_id, static_ip,gateway, interface_name, commands))


async def configure_vm_network_async(ws, vm_id, static_ip,gateway, interface_name, commands):
    """Waits for VM readiness and configures the network"""
    if not await wait_for_vm_ready(ws, vm_id):
        return

    temp_ip = await get_vm_ip(ws, vm_id)
    if not temp_ip or not await wait_for_ssh(temp_ip):
        return

    
    formatted_commands = [
        cmd.replace("{static_ip}", static_ip).replace("{interface_name}", interface_name).replace("{gateway}", gateway)
        for cmd in commands
    ]

    execute_commands(temp_ip, formatted_commands)

    
    response = await send_rpc(ws, "xo.getAllObjects", {"filter": {"type": "VIF"}})
    if response and "result" in response:
 
         for vif_id, vif_info in response["result"].items():
             vif_vm_id = vif_info.get("$VM")  
             vif_network_id = vif_info.get("$network")  
 
 
             if vif_vm_id == vm_id and vif_network_id == TEMP_NETWORK_UUID:  
                 print(f"[DEBUG] Removing Temporary VIF ({vif_id}) from VM {vm_id}")
                 await send_rpc(ws, "vif.delete", {"id": vif_id})
                 return
 
    print(f"[ERROR] Could not find Temporary VIF for VM {vm_id}")

async def get_existing_teams(ws):
    response = await send_rpc(ws, "xo.getAllObjects", {"filter": {"type": "VM"}})
    if "result" not in response:
        return 0  
    max_team_number = 0
    for vm in response["result"].values():
        name = vm.get("name_label", "")
        match = re.match(r"CTF-TEAM-(\d+)", name)
        if match:
            max_team_number = max(max_team_number, int(match.group(1)))
    return max_team_number


async def process_challenges(args,config):
    """Handles challenge processing and VM creation asynchronously"""
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(XO_WS_URL) as ws:
            await send_rpc(ws, "session.signIn", {"username": USERNAME, "password": PASSWORD})
            results = []
            tasks = []  

            max_team_number = await get_existing_teams(ws)
            new_team_number = max_team_number + 1
            cont=0
            gateway = f"{args.subnet}.{1}"

            for challenge in config.get("challenges", []):
                cont+=1
                vm_name = f"{args.prefix}-{args.team}-CTF-TEAM-{new_team_number}-C-{cont}"
                template_uuid = challenge.get("template_uuid")
                static_ip = f"{args.subnet}.{cont+1}"

                vm_id = await create_vm(ws, vm_name, template_uuid)
                if not vm_id:
                    print(f"[ERROR] Failed to create VM {vm_name}")
                    continue

                print(f"[DEBUG] VM {vm_name} created with ID {vm_id}")

                task = await configure_vm_network(ws, vm_id, static_ip, gateway, args.interface_name, args.commands)
                tasks.append(task)

                results.append({"name": vm_name, "vm_id": vm_id})

            await asyncio.gather(*tasks)

            return results



if __name__ == "__main__":
    args = parse_arguments()
    with open(args.config, "r") as file:
        config = json.load(file)

    # Load environment variables from .env file
    config_env = dotenv.dotenv_values(args.env)

    # Network UUIDs
    XO_WS_URL = config_env['XO_WS_URL']
    USERNAME = config_env['USERNAME']
    PASSWORD = config_env['PASSWORD']
    DEFAULT_VM_DESCRIPTION = config_env['DEFAULT_VM_DESCRIPTION']
    OUTPUT_FILE = config_env['OUTPUT_FILE']
    SSH_USER = config_env['SSH_USER']
    SSH_PASSWORD = config_env['SSH_PASSWORD']
    TEMP_NETWORK_UUID = "f36baa81-d4c7-11c7-6a04-2c7315460201"  # VIF1 for SSH -> Eth3
    NETWORK_UUID = args.network_uuid  # VIF0 (Final network) -> CTF SubNet

    result = asyncio.run(process_challenges(args,config))
    with open(OUTPUT_FILE, "w") as file:
        json.dump(result, file, indent=4)
    print(f"Results stored in {OUTPUT_FILE}")
