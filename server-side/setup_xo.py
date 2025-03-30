import asyncio
import json
import uuid
import aiohttp
import re
import paramiko
import time
import argparse
import datetime

import dotenv
import os

# Network UUIDs
receive_lock = asyncio.Lock()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Execute command on xo through JSON-RPC")
    parser.add_argument("--tmp", required=True, help="Temp folder")
    parser.add_argument("--env", required=True, help="Env")
    parser.add_argument("--prefix", required=True, help="Event prefix")
    parser.add_argument("--vm_prefix", required=True, help="VMs prefix")
    parser.add_argument("--action", required=True, help="Action")
    parser.add_argument("--params", nargs='+', required=False, help="Parameters")
    return parser.parse_args()

async def send_rpc(ws, method, params=None):
    async with receive_lock:
        request_id = str(uuid.uuid4())
        request = {"jsonrpc": "2.0", "method": method, "params": params or {}, "id": request_id}
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

async def connect(args):
    """Handles challenge processing and VM creation asynchronously"""
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(XO_WS_URL) as ws:
            await send_rpc(ws, "session.signIn", {"username": USERNAME, "password": PASSWORD})
            results = None
            if args.action == 'cleanup':
                results = await cleanup(ws, args)

            elif args.action == 'setup':
                results = await setup(ws, args)

            elif args.action == 'check':
                results = await get_existing_teams(ws, args)

            return results


async def getlAllObjects(ws, args):
    response = await send_rpc(ws, "proxy.getAll",  {})
    print(json.dumps(response, indent=4))

async def cleanup(ws, args):
    IDs = await get_network_id(ws, args)
    if IDs is not None and len(IDs) > 0:
        for network_id in IDs:
            await deleteVIFs(ws, args, network_id)
            await delete_network(ws, args, network_id)

async def get_network_id(ws, args):
    """Finds a network by name, deletes it, and creates a new one."""
    params = json.loads(args.params[0])
    network_name = params['network_name']
    objects = await send_rpc(ws, "xo.getAllObjects")
    if "result" not in objects:
        print("[DEBUG] Failed to retrieve objects.")
        return

    IDs = []
    network_to_delete = False
    for obj in objects['result'].values():
        if isinstance(obj, dict):
            if obj.get("type") == "network" and obj.get("name_label") == network_name:
                print(json.dumps(obj, indent=4))
                network_to_delete = obj
                IDs.append(network_to_delete['id'])

    if not network_to_delete:
        print(f"[DEBUG] No network found with the name '{network_name}'.")
        return
    else:
        print(f"[DEBUG] Found {len(IDs)} with the name '{network_name}'.")


    return IDs

async def delete_network(ws, args, network_id):
    """Finds a network by name, deletes it, and creates a new one."""

    params = json.loads(args.params[0])
    network_name = params['network_name']

    delete_response = await send_rpc(ws, "network.delete", {"id": network_id})
    if delete_response is None:
        print("[DEBUG] Failed to delete network.")
        return

    print("[DEBUG] Network deleted successfully.")

async def deleteVIFs(ws, args, network_id):
    # await getlAllObjects(ws, args)

    response = await send_rpc(ws, "xo.getAllObjects", {"filter": {"type": "VM"}})
    if "result" not in response:
        return 0
    count = 0
    print(args)
    params = json.loads(args.params[0])
    for vm in response["result"].values():
        name = vm.get("name_label", "")
        openvpn_vm_id = vm['id']
        if params['openvpn_vm_name'] == name:
            VIFs = vm['VIFs']

            response_vif = await send_rpc(ws, "xo.getAllObjects", {"filter": {"type": "VIF"}})
            if response_vif and "result" in response_vif:
                for vif_id, vif_info in response_vif["result"].items():
                    vif_vm_id = vif_info.get("$VM")
                    vif_network_id = vif_info.get("$network")

                    if vif_vm_id == openvpn_vm_id and vif_network_id == network_id:
                        print(f"[DEBUG] Removing Temporary VIF ({vif_id}) from VM {vif_vm_id}")
                        await send_rpc(ws, "vif.disconnect", {"id": vif_id})
                        await send_rpc(ws, "vif.delete", {"id": vif_id})
                        count += 1

        elif args.prefix in name:
            a = 0
            print(f"[DEBUG] Removing VM ({name}) ID {openvpn_vm_id}")
            await send_rpc(ws, "vm.delete", {"id": openvpn_vm_id})

    return

async def get_pool_id(ws, pool_name):
    """Retrieve the first available pool ID dynamically."""
    response = await send_rpc(ws, "xo.getAllObjects")
    if "result" not in response:
        print("[DEBUG] Failed to get pool ID.")
        return

    for obj in response['result'].values():
        if obj.get("name_label") == pool_name and obj.get("type") == "pool":
            print("[DEBUG] Pool ID.")
            pool_id = obj.get("id")  # Return the first pool ID found
            return pool_id

    print("[DEBUG] Failed to get pool ID.")
    return None

async def setup_network(ws, args):
    """Finds a network by name, deletes it, and creates a new one."""
    params = json.loads(args.params[0])
    network_name = params['network_name']
    pool_name = params['pool_name']

    pool_id = await get_pool_id(ws, pool_name)
    if not pool_id:
        return

    print("[DEBUG] Creating new network...")
    response = await send_rpc(ws, "network.create", {
        "pool": pool_id,
        "name": network_name,
        "description": f"CTF network {datetime.datetime.now()}"
    })

    if response is  None:
        print(f"[DEBUG] Failed to create new network. Response: {response}")

    new_network_id = response['result']
    if response is not None:
        print(f"Network id: {new_network_id}")
    else:
        print(f"[DEBUG] Failed to create new network. Response: {response}")

    with open(f'{args.tmp}/temp_new_network.txt', "w") as file:
        json.dump({'network_id': new_network_id}, file, indent=4)

    return new_network_id


async def setup(ws, args):
    Results = []
    network_id = await setup_network(ws, args)
    Results.append(network_id)
    Results.append(await setupVIFsOpenVPN(ws, args, network_id))

    return Results

async def setupVIFsOpenVPN(ws, args, network_id):
    # await getlAllObjects(ws, args)

    response = await send_rpc(ws, "xo.getAllObjects", {"filter": {"type": "VM"}})
    if "result" not in response:
        return 0
    count = 0
    params = json.loads(args.params[0])
    VIF_ids = []
    for vm in response["result"].values():
        name = vm.get("name_label", "")
        openvpn_vm_id = vm['id']
        if params['openvpn_vm_name'] == name:
            VIFs = vm['VIFs']
            for i in range(int(params['add_vifs'])):
                if openvpn_vm_id == openvpn_vm_id:
                    print(f"[DEBUG] Creating VIF on VM {openvpn_vm_id}")
                    response = await send_rpc(ws, "vm.createInterface", {"vm": openvpn_vm_id, "network": network_id})
                    if response and "result" in response:
                        VIF_id = response["result"]
                        print(response)
                        VIF_ids.append(VIF_id)

    return VIF_ids

async def get_existing_teams(ws, args):
    response = await send_rpc(ws, "xo.getAllObjects", {"filter": {"type": "VM"}})
    if "result" not in response:
        return 0
    max_team_number = 0
    for vm in response["result"].values():
        name = vm.get("name_label", "")
        match = re.search(rf"{args.vm_prefix}-(\d+)", name)
        if match:
            max_team_number = max(max_team_number, int(match.group(1)))
    return max_team_number


if __name__ == "__main__":
    args = parse_arguments()
    config = dotenv.dotenv_values(args.env)
    XO_WS_URL = config['XO_WS_URL']
    USERNAME = config['USERNAME']
    PASSWORD = config['PASSWORD']
    DEFAULT_VM_DESCRIPTION = config['DEFAULT_VM_DESCRIPTION']
    OUTPUT_FILE = config['OUTPUT_FILE']
    SSH_USER = config['SSH_USER']
    SSH_PASSWORD = config['SSH_PASSWORD']

    result = asyncio.run(connect(args))
    print(result)
    # with open(OUTPUT_FILE, "w") as file:
    #     json.dump(result, file, indent=4)
    # print(f"Results stored in {OUTPUT_FILE}")