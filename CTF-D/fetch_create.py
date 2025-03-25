import requests
import os
from dotenv import load_dotenv

def fetch_challenges(session, url):
    response = session.get(f"{url}/challenges")
    if response.status_code != 200:
        print("Erro ao obter challenges:", response.text)
        return []

    challenges = response.json().get("data", [])
    print("\n=== Lista de Challenges ===")
    all_challenges = []

    for ch in challenges:
        ch_id = ch["id"]
        detail_resp = session.get(f"{url}/challenges/{ch_id}")
        if detail_resp.status_code != 200:
            print(f"- Erro ao obter detalhes do challenge ID {ch_id}")
            continue

        challenge_data = detail_resp.json().get("data", {})
        name = challenge_data.get("name")
        category = challenge_data.get("category")
        description = challenge_data.get("description")
        value = challenge_data.get("value")
        state = challenge_data.get("state")
        type_ = challenge_data.get("type")
        max_attempts = challenge_data.get("max_attempts")

        hint_resp = session.get(f"{url}/challenges/{ch_id}/hints")
        hint_data = hint_resp.json().get("data", []) if hint_resp.status_code == 200 else []
        hint = hint_data[0]["content"] if hint_data else None
        hint_cost = hint_data[0]["cost"] if hint_data else None

        flag_resp = session.get(f"{url}/challenges/{ch_id}/flags")
        flag_data = flag_resp.json().get("data", []) if flag_resp.status_code == 200 else []
        flag = flag_data[0]["content"] if flag_data else None
        flag_type = flag_data[0]["type"] if flag_data else None

        files_resp = session.get(f"{url}/challenges/{ch_id}/files")
        files = files_resp.json().get("data", []) if files_resp.status_code == 200 else []

        file_paths = [f["location"] for f in files] if files else []

        print(f"\n--- Challenge ID {ch_id} ---")
        print(f"Nome: {name}")
        print(f"Categoria: {category}")
        print(f"Descrição: {description}")
        print(f"Valor: {value}")
        print(f"Estado: {state}")
        print(f"Tipo: {type_}")
        print(f"Número Máximo de Tentativas: {max_attempts}")
        print(f"Dica: {hint}")
        print(f"Custo da Dica: {hint_cost}")
        print(f"Flag: {flag}")
        print(f"Tipo da Flag: {flag_type}")
        print(f"Ficheiros: {file_paths if file_paths else 'Nenhum'}")
        print(f"Template UUID: {challenge_data.get('template_uuid')}")
        print(f"Network UUID: {challenge_data.get('network_uuid')}")

                
        challenge_info = {
            "name": name,
            "category": category,
            "description": description,
            "value": value,
            "state": state,
            "type": type_,
            "max_attempts": max_attempts,
            "hint": hint,
            "hint_cost": hint_cost,
            "flag": flag,
            "flag_type": flag_type,
            "file_paths": file_paths,
            "template_uuid": challenge_data.get("template_uuid"),
            "network_uuid": challenge_data.get("network_uuid")
        }
        all_challenges.append(challenge_info)

    return all_challenges

def fetch_teams(session, url):
    response = session.get(f"{url}/teams")
    if response.status_code != 200:
        print("Erro ao obter equipas:", response.text)
        return 0

    teams = response.json().get("data", [])
    print(f"\n=== Lista de Equipas (Total: {len(teams)}) ===")
    for team in teams:
        print(f"- {team['name']} (ID: {team['id']})")

    return len(teams)

def main():
    load_dotenv()
    url = os.getenv("CTFD_URL")
    token = os.getenv("CTFD_TOKEN")

    if not url or not token:
        print("Erro: CTFD_URL ou CTFD_TOKEN não definidos no .env")
        return

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    })

    challenges = fetch_challenges(session, url)
    fetch_teams(session, url)

    vm_challenges = [ch for ch in challenges if ch["template_uuid"] and ch["network_uuid"]]

    if vm_challenges:
        try:
            flask_response = requests.post(
                "http://127.0.0.1:5000/create-vms",
                json=vm_challenges
            )
            if flask_response.status_code == 200:
                print("\n Desafios com VM enviados com sucesso para o servidor Flask.")
                print("Resposta:")
                print(flask_response.json())
            else:
                print("\n Erro ao enviar para o servidor Flask:")
                print(flask_response.status_code, flask_response.text)
        except requests.exceptions.RequestException as e:
            print("\n Erro de conexão ao servidor Flask:")
            print(e)
    else:
        print("\nℹ Nenhum desafio com VM para enviar.")

    session.close()

