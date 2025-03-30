import os
from dotenv import load_dotenv
import requests
import json

import initialize_event
################################################################################################################################################################################################################################################
####################################################      ADD Challenges     ############################################################################################################################################################
################################################################################################################################################################################################################################################

def add_users(url, token,users_file="users.json",teams_file="teams.json"):
    exit("TBD!")

    headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
    }

    # Criação da sessão
    session = requests.Session()
    session.headers.update(headers)

    # Dados dos utilizador que vão ser criados
    try:
        with open(users_file, "r", encoding="utf-8") as f:
            users_data = json.load(f)
    except FileNotFoundError:
        print(f"Ficheiro '{users_file}' não encontrado.")
        return 0, 0
    except json.JSONDecodeError as e:
        print(f"Erro a fazer parsing do ficheiro JSON: {e}")
        return 0, 0
     

    #Criação de utilizadores e armazenamento dos IDS criados para ser possivel adicionar os utilizadores às equipas
    user_ids = {}
    for username, user_info in users_data.items():
        response = session.post(f"{url}/users", json={k: v for k, v in user_info.items() if k not in ["team"]}) #post para o endpoint de users com a user_info criada acima

        if response.status_code == 200:
            user_id = response.json().get("data", {}).get("id") #Em caso de sucesso, obtém-se o id do user e armazena-se
            user_ids[username] = [user_id, user_info["team"]]

            print(f"Usuário '{user_info['name']}' criado com sucesso! ID: {user_id}")
        else:
            print(f"Erro ao criar usuário '{user_info['name']}': {response.text}")


    # Criação de teams
    try:
        with open(teams_file, "r", encoding="utf-8") as f:
            teams_data = json.load(f)
    except FileNotFoundError:
        print(f"Ficheiro '{teams_file}' não encontrado.")
        return 0, 0
    except json.JSONDecodeError as e:
        print(f"Erro a fazer parsing do ficheiro JSON: {e}")
        return 0, 

    team_ids = {} #Armazenamento do id das teams para posterior associação dos utilizadores
    teams_counter = 0
    for team_name, team_info in teams_data.items():
        response = session.post(f"{url}/teams", json=team_info) #Post para o endpoint das equipas

        if response.status_code == 200:
            team_id = response.json().get("data", {}).get("id") #Obtenção do id da equipa e armazenamento do mesmo
            team_ids[team_name] = team_id
            teams_counter += 1
            print(f"Equipe '{team_info['name']}' criada com sucesso! ID: {team_id}")
        else:
            print(f"Erro ao criar equipe '{team_info['name']}': {response.text}")
 

    # Adição de utilizadores à equipa
    for team_name, team_id in team_ids.items():
        for user, user_info in user_ids.items():
            print(user_info)
            if team_name == user_info[1]:
                response = session.post(f"{url}/teams/{team_id}/members", json={"user_id": user_info[0]}) #Endpoint para associação de utilizadores à equipa
                if response.status_code == 200:
                    print(f"Usuário '{user}' adicionado à equipe '{team_name}' com sucesso!")
                else:
                    print(f"Erro ao adicionar usuário '{user}' à equipe '{team_name}': {response.text}")



    session.close()

    return teams_counter

def setup_new_team():
    load_dotenv()
    url = os.getenv("CTFD_URL")
    token = os.getenv("CTFD_TOKEN")

    if not url or not token:
        print("Erro: CTFD_URL ou CTFD_TOKEN não definidos no .env")
        return

    # TODO: add team/useres
    # counter_teams = add_users(url, token)

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    })
    with open("challenges.json", "r", encoding="utf-8") as f:
        all_challenges = list(json.load(f).values())

    challenges_with_vm = [ch for ch in all_challenges if ch.get("template_uuid") is not None]
    payload = {
        "challenges": challenges_with_vm,
        "num_users": initialize_event.num_vpn_users
    }
    response = requests.post("http://127.0.0.1:5000/setup-new-team", json=payload)
    if response.status_code == 200:
        # Open a file in binary write mode and save the response content as a ZIP file
        with open("output-setup-new-team.zip", "wb") as f:
            f.write(response.content)
        print("ZIP file has been saved as 'output.zip'")
    else:
        print(f"Failed to get response. Status code: {response.status_code}")

    session.close()


if __name__ == "__main__":
    #main()
    setup_new_team()
