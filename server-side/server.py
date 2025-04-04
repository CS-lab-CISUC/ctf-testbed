from flask import Flask, request, jsonify,send_file
import json
import subprocess
import os
from dotenv import load_dotenv
import glob
import shutil
import tempfile
import zipfile
import copy

app = Flask(__name__)
output_dir = "vm_outputs"

@app.route("/create-vms", methods=["POST"])
def create_vms():
    data = request.get_json()

    if not data or not isinstance(data, dict):
        return jsonify({"error": "Formato inválido."}), 400
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  #

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir) 
    os.makedirs(output_dir)

    challenges = data.get("challenges")
    organization_vms = data.get("organization_vms")
    num_teams = data.get("num_teams")
    num_users = data.get("num_users")

    if not isinstance(challenges, list) or not isinstance(num_teams, int) or not isinstance(num_users, int):
        return jsonify({"error": "Estrutura inválida"}), 400

    print(f"Número de equipas: {num_teams}")
    print(f"Número de users: {num_users}")
    launch_config_temp = {
        "vms": []
    }

    launch_config = copy.deepcopy(launch_config_temp)

    for challenge in challenges:
        name = challenge.get("name")
        template_uuid = challenge.get("template_uuid")
        network_uuid = challenge.get("network_uuid")
        user=challenge.get("user")
        password=challenge.get("password")
        commands=challenge.get("commands")

        if template_uuid and network_uuid:
            if not challenge.get("ImAModule", False):
                print(f"Criar VM para challenge '{name}' com template '{template_uuid}' e rede '{network_uuid}'")

                launch_config["vms"].append({
                    "name": name,
                    "description": f"Created for Shift CTF| {challenge.get('description')}",
                    "template_uuid": template_uuid,
                    "network_uuid": network_uuid,
                    "user": user,
                    "password": password,
                    "commands": commands
                })

            else:
                print(f"Challenge '{name}' não requer VM.")
      
        else:
            print(f"Challenge '{name}' não requer VM.")

    with open("challenges_vms-config.json", "w") as f:
        json.dump(launch_config, f, indent=4)

    print("Ficheiro 'challenges_vms-config.json' criado com sucesso!")

    launch_config = copy.deepcopy(launch_config_temp)

    for organization_vm in organization_vms:
        name = organization_vm.get("name")
        template_uuid = organization_vm.get("template_uuid")
        network_uuid = organization_vm.get("network_uuid")
        user = organization_vm.get("user")
        password = organization_vm.get("password")
        commands = organization_vm.get("commands")

        if template_uuid and network_uuid:
            print(f"Criar VM para organization_vm '{name}' com template '{template_uuid}' e rede '{network_uuid}'")

            launch_config["vms"].append({
                "name": name,
                "description": f"Created for Shift CTF| {organization_vm.get('description')}",
                "template_uuid": template_uuid,
                "network_uuid": network_uuid,
                "user": user,
                "password": password,
                "commands": commands
            })
        else:
            exit(f"organization_vm '{name}' não tem os detalhes necessários.")

    with open("organization_vms-config.json", "w") as f:
        json.dump(launch_config, f, indent=4)

    print("Ficheiro 'organization_vms-config.json' criado com sucesso!")

    env = os.environ.copy()
    env["TEAMS_COUNT"] = str(num_teams)
    env["TEAMS_USERS_COUNT"] = str(num_users)

    script_command = "bash initialize_server.sh"
    log_file = "log.txt"
    NotAtAllSuspicious  = os.getenv("COM")

    print("A executar script de inicialização de VMs...")
    with open(log_file, "w") as log:
        result = subprocess.run(
            f'echo "{NotAtAllSuspicious}" | sudo -E -S {script_command}',
            shell=True,
            stdout=log,
            stderr=subprocess.STDOUT,
            env=env
        )

    if result.returncode == 0:
        print("Script terminou com sucesso!")

        # try:
        #     teams_data = {}
        #
        #     template_challenge_map = {}
        #     for ch in challenges:
        #         if ch.get("template_uuid") and ch.get("network_uuid"):
        #             template_uuid = ch["template_uuid"]
        #             template_challenge_map.setdefault(template_uuid, []).append(ch["name"])
        #
        #     for file_path in glob.glob(os.path.join(output_dir, "team_*.json")):
        #         with open(file_path, "r") as f:
        #             entry = json.load(f)
        #             updated_entry = {}
        #             for team, challenges_dict in entry.items():
        #                 updated_entry[team] = {}
        #                 for challenge_name, ip in challenges_dict.items():
        #                     template_uuid = None
        #                     for ch in challenges:
        #                         if ch["name"] == challenge_name:
        #                             template_uuid = ch.get("template_uuid")
        #                             break
        #                     names = template_challenge_map.get(template_uuid, [challenge_name])
        #                     updated_entry[team][json.dumps(names)] = ip
        #             teams_data.update(updated_entry)
        #
        #     for file_path in glob.glob(os.path.join(output_dir, "organization_*.json")):
        #         with open(file_path, "r") as f:
        #             entry = json.load(f)
        #             updated_entry = {}
        #             for team, challenges_dict in entry.items():
        #                 updated_entry[team] = {}
        #                 for challenge_name, ip in challenges_dict.items():
        #                     template_uuid = None
        #                     for ch in challenges:
        #                         if ch["name"] == challenge_name:
        #                             template_uuid = ch.get("template_uuid")
        #                             break
        #                     names = template_challenge_map.get(template_uuid, [challenge_name])
        #                     updated_entry[team][json.dumps(names)] = ip
        #             teams_data.update(updated_entry)
        #
        #     return jsonify(teams_data)
        # except FileNotFoundError:
        #     return jsonify({"error": "Ficheiro de equipas não encontrado."}), 500
        # except json.JSONDecodeError as e:
        #     return jsonify({"error": f"Erro de parsing JSON: {str(e)}"}), 500

        return download_vm_package()
    else:
        print(f"Script terminou com erro! Código: {result.returncode}")
        return jsonify({"status": "Ardeu",})



@app.route("/setup-new-team", methods=["POST"])
def setup_new_team():
    data = request.get_json()

    if not data or not isinstance(data, dict):
        return jsonify({"error": "Formato inválido."}), 400

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  #

    challenges = data.get("challenges")
    num_users = data.get("num_users")

    if not isinstance(challenges, list) or not isinstance(num_users, int):
        return jsonify({"error": "Estrutura inválida"}), 400

    print(f"Número de users: {num_users}")
    launch_config_temp = {
        "vms": []
    }

    launch_config = copy.deepcopy(launch_config_temp)

    for challenge in challenges:
        name = challenge.get("name")
        template_uuid = challenge.get("template_uuid")
        network_uuid = challenge.get("network_uuid")
        user = challenge.get("user")
        password = challenge.get("password")
        commands = challenge.get("commands")

        if template_uuid and network_uuid:
            if not challenge.get("ImAModule", False):
                print(f"Criar VM para challenge '{name}' com template '{template_uuid}' e rede '{network_uuid}'")

                launch_config["vms"].append({
                    "name": name,
                    "description": f"Created for Shift CTF| {challenge.get('description')}",
                    "template_uuid": template_uuid,
                    "network_uuid": network_uuid,
                    "user": user,
                    "password": password,
                    "commands": commands
                })

            else:
                print(f"Challenge '{name}' não requer VM.")

        else:
            print(f"Challenge '{name}' não requer VM.")

    with open("challenges_vms-config.json", "w") as f:
        json.dump(launch_config, f, indent=4)

    print("Ficheiro 'challenges_vms-config.json' criado com sucesso!")

    env = os.environ.copy()
    env["TEAMS_COUNT"] = "1"
    env["TEAMS_USERS_COUNT"] = str(num_users)

    script_command = "bash initialize_server.sh -f setup_new_team"
    log_file = "log.txt"
    NotAtAllSuspicious = os.getenv("COM")

    print("A executar script de inicialização de VMs...")
    with open(log_file, "w") as log:
        result = subprocess.run(
            f'echo "{NotAtAllSuspicious}" | sudo -E -S {script_command}',
            shell=True,
            stdout=log,
            stderr=subprocess.STDOUT,
            env=env
        )

    if result.returncode == 0:
        return download_vm_package()
    else:
        print(f"Script terminou com erro! Código: {result.returncode}")
        return jsonify({"status": "Ardeu", })


@app.route("/download", methods=["GET"])
def download_vm_package(team=None):
    folders_to_zip = [
        ("/etc/openvpn/client", "client"),
        (output_dir, "vm_outputs")
    ]

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as temp_zip:
            with zipfile.ZipFile(temp_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
                for folder_path, archive_name in folders_to_zip:
                    if not os.path.exists(folder_path):
                        print(f"[WARN] Pasta não encontrada: {folder_path}")
                        continue
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            if team is not None and team not in file:
                                continue
                            full_path = os.path.join(root, file)
                            rel_path = os.path.relpath(full_path, folder_path)
                            arcname = os.path.join(archive_name, rel_path)
                            zipf.write(full_path, arcname=arcname)

            temp_zip_path = temp_zip.name

        response = send_file(
            temp_zip_path,
            as_attachment=True,
            download_name="ctf_vm_package.zip",
            mimetype="application/zip"
        )

        @response.call_on_close
        def cleanup_tempfile():
            try:
                os.remove(temp_zip_path)
                print(f"[DEBUG] ZIP temporário apagado: {temp_zip_path}")
            except Exception as e:
                print(f"[ERROR] Falha ao apagar ZIP temporário: {e}")

        return response

    except Exception as e:
        return jsonify({"error": f"Erro ao criar ZIP: {str(e)}"}), 500



if __name__ == "__main__":
    app.run(debug=True, port=5000)
