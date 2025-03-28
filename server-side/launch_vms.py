import asyncio
import json
import uuid
import aiohttp
import asyncssh
import re
import paramiko
import time
import argparse
import threading
import dotenv
import os
from collections import defaultdict
import pathlib
import random

def generate_random_mac():
    mac = [0x02, 0x00, 0x00,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


lock = threading.Lock()


team_ips = defaultdict(dict)


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

    request_id = str(uuid.uuid4())
    print(f"[DEBUG] UUID:{request_id}")
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
    return None




async def create_vm(ws, vm_name, template_uuid):
    """Creates the VM with two VIFs (VIF0=Challenge Network, VIF1=SSH)"""
    params = {
        "name_label": vm_name,
        "name_description": DEFAULT_VM_DESCRIPTION,
        "template": template_uuid,
        "bootAfterCreate": True,
        "VIFs": [
            {"network": NETWORK_UUID,"mac": generate_random_mac()},  # VIF0: Main network (eth0)
            {"network": TEMP_NETWORK_UUID,"mac": generate_random_mac()}  # VIF1: Temporary SSH access
        ]
    }
    response = await send_rpc(ws, "vm.create", params)
    return response.get("result") if response else None


async def wait_for_vm_ready(ws, vm_id, max_retries=50, delay=20):
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

async def get_vm_ip(ws, vm_id, max_retries=50, delay=20):
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

async def wait_for_ssh(ip,challenge , max_retries=50, delay=10):
    for attempt in range(1, max_retries + 1):
        try:
            async with asyncssh.connect(ip, username=challenge.get('user'), password=challenge.get('password'), known_hosts=None) as conn:
                print(f"[DEBUG] SSH is available on {ip}")
                return True
        except Exception:
            print(f"[DEBUG] Waiting for SSH on {ip}... Attempt {attempt}/{max_retries}")
            await asyncio.sleep(delay)
    return False

def expect_prompt(shell, prompt='$', timeout=10):
    """Read from shell until we get the prompt or timeout."""
    shell.settimeout(timeout)
    buffer = ''
    while True:
        try:
            data = shell.recv(1024).decode()
            if not data:
                break
            buffer += data
            if prompt in buffer:
                break
        except Exception:
            break
    return buffer

def send_command(shell, command, password=None):
    """Send command and handle sudo password if needed."""
    print(f"[DEBUG] Sending: {command}")
    shell.send(command + "\n")
    output = expect_prompt(shell)
    print(f"[DEBUG] Output:\n{output}")

    if "[sudo] password for" in output:
        print("[DEBUG] Sending sudo password...")
        shell.send(password + "\n")
        output = expect_prompt(shell)
        print(f"[DEBUG] Post-password Output:\n{output}")

    return output

# Espera até que a interface 'Wired connection 1' tenha o IP estático atribuído
def check_static_ip(ssh, expected_ip):
    stdin, stdout, stderr = ssh.exec_command("ip addr show")
    output = stdout.read().decode()
    return expected_ip in output


def execute_commands(VM_IP, commands, challenge):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"[DEBUG] Connecting to {VM_IP} as {challenge.get('user')}...")
        ssh.connect(VM_IP, username=challenge.get('user'), password=challenge.get('password'))

        shell = ssh.invoke_shell()
        time.sleep(2)

        initial_output = expect_prompt(shell)
        print(f"[DEBUG] Initial Shell Output:\n{initial_output}")

        for command in commands:
            send_command(shell, command, password=challenge.get('password'))

        challenge_commands = challenge.get("commands", [])
        if isinstance(challenge_commands, list):
            for command in challenge_commands:
                send_command(shell, command, password=challenge.get('password'))

        for attempt in range(5):
            if check_static_ip(ssh, challenge["static_ip"]):
                print(f"[DEBUG] Static IP {challenge['static_ip']} successfully verified.")
                break
            print(f"[DEBUG] Static IP {challenge['static_ip']} not yet applied. Retrying...")
            time.sleep(5)
        else:
            
            print(f"[ERROR] Static IP {challenge['static_ip']} not detected after retries.")
            return False

        shell.close()
        ssh.close()
        print(f"[DEBUG] Commands executed successfully!")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to execute commands on {VM_IP}: {e}")
        return False







async def configure_vm_network(ws, vm_id, static_ip,gateway, interface_name, commands,challenge):
    if not await wait_for_vm_ready(ws, vm_id):
        return

    temp_ip = await get_vm_ip(ws, vm_id)
    if not temp_ip or not await wait_for_ssh(temp_ip,challenge):
        print(f"[ERROR] Failed to connect through ssh wait_for_ssh: {temp_ip} {challenge}")
        return

    formatted_commands = [
        cmd.replace("{static_ip}", static_ip).replace("{interface_name}", interface_name).replace("{gateway}", gateway)
        for cmd in commands
    ]

    challenge["static_ip"] = static_ip

    for attempt in range(5):
        success = execute_commands(temp_ip, formatted_commands, challenge)
        if success:
            break
        print(f"[WARN] Attempt {attempt+1} failed. Retrying configuration in 5s...")
        await asyncio.sleep(5)
    else:
        print(f"[ERROR] All retries failed for VM {vm_id}. Skipping VIF removal.")
        return

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


async def process_challenge(args,config,challenge,idx):

    """Handles challenge processing and VM creation asynchronously"""
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(XO_WS_URL) as ws:
            print(f"[Thread-{idx}] Authenticating...")
            auth_response = await send_rpc(ws, "session.signInWithPassword",
                                           {"email": USERNAME, "password": PASSWORD})


            if not auth_response:
                print(f"[Thread-{idx}] Authentication failed!")
                return
            vm_name = f"{args.prefix}-{args.team}-{challenge.get('name')}"
            template_uuid = challenge.get("template_uuid")
            static_ip = f"{args.subnet}.{idx+2}"
            gateway = f"{args.subnet}.{1}"

            vm_id = await create_vm(ws, vm_name, template_uuid)
            if not vm_id:
                print(f"[Thread-{idx}] [ERROR] Failed to create VM {vm_name}")
                return

            print(f"[Thread-{idx}] [DEBUG] Created VM {vm_name} with ID {vm_id}")
            
            team_key = f"{args.team}"
            with lock:
                team_ips[team_key][challenge.get("name")] = static_ip


            await configure_vm_network(ws, vm_id, static_ip, gateway, args.interface_name, args.commands,challenge)

def run_thread(args,config,challenge, idx):
    asyncio.run(process_challenge(args,config,challenge, idx))



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

    challenges = config.get("vms", [])
    num_challenges = len(challenges)

    threads = []

    print("Runningn Threads")
     
    for idx, challenge in enumerate(challenges):
        thread = threading.Thread(target=run_thread, args=(args,config,challenge, idx))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

   



    print("[DEBUG] team_ips final:", json.dumps(team_ips, indent=2))  # debug obrigatório

    # Guarda os IPs num ficheiro individual por equipa
    print(f"[DEBUG] Current working dir: {os.getcwd()}")

    output_path = pathlib.Path(f"./vm_outputs/{args.team.replace(' ', '_').lower()}.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)  # <- cria o diretório ./tmp se necessário

    with open(output_path, "w") as f:
        json.dump({args.team: team_ips[args.team]}, f)

    print("End Of Script")
