from flask import Flask, request, jsonify
import json
import subprocess
import os
from dotenv import load_dotenv
import glob
import shutil

app = Flask(__name__)

@app.route("/create-vms", methods=["POST"])
def create_vms():
    data = request.get_json()

    if not data or not isinstance(data, dict):
        return jsonify({"error": "Formato inválido."}), 400
    
    output_dir = "./vm_outputs"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir) 
    os.makedirs(output_dir)

    challenges = data.get("challenges")
    num_teams = data.get("num_teams")

    if not isinstance(challenges, list) or not isinstance(num_teams, int):
        return jsonify({"error": "Estrutura inválida"}), 400

    print(f"Número de equipas: {num_teams}")
    launch_config = {
        "subnet_base": "192.168",
        "challenges": []
    }

    for idx, challenge in enumerate(challenges, start=1):
        name = challenge.get("name")
        template_uuid = challenge.get("template_uuid")
        network_uuid = challenge.get("network_uuid")
        user=challenge.get("user")
        password=challenge.get("password")
        commands=challenge.get("commands")

        if template_uuid and network_uuid:
            print(f"Criar VM para challenge '{name}' com template '{template_uuid}' e rede '{network_uuid}'")

            launch_config["challenges"].append({
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

    with open("launch_vms-config.json", "w") as f:
        json.dump(launch_config, f, indent=4)

    print("Ficheiro 'launch_vms-config.json' criado com sucesso!")

    env = os.environ.copy()
    env["TEAMS_COUNT"] = str(num_teams)

    script_command = "bash initialize_server.sh"
    log_file = "log.txt"
    NotAtAllSuspicious  = os.getenv("COM")

    print("A executar script de inicialização de VMs...")
    with open(log_file, "w") as log:
        result = subprocess.run(
            f'echo "{NotAtAllSuspicious}" | sudo -S {script_command}',
            shell=True,
            stdout=log,
            stderr=subprocess.STDOUT,
            env=env
        )

    if result.returncode == 0:
        print("Script terminou com sucesso!")

        try:
            teams_data = {}
            for file_path in glob.glob("./vm_outputs/team_*.json"):
                with open(file_path, "r") as f:
                    entry = json.load(f)
                    teams_data.update(entry)
            return jsonify(teams_data)
        except FileNotFoundError:
            return jsonify({"error": "Ficheiro de equipas não encontrado."}), 500
        except json.JSONDecodeError as e:
            return jsonify({"error": f"Erro de parsing JSON: {str(e)}"}), 500

   


    else:
        print(f"Script terminou com erro! Código: {result.returncode}")
        return jsonify({"status": "Ardeu",})
   

if __name__ == "__main__":
    app.run(debug=True, port=5000)
