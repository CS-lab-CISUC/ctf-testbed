import requests
import time

def add_users(url, token):


    headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
    }

    # Criação da sessão
    session = requests.Session()
    session.headers.update(headers)

    # Dados dos utilizador que vão ser criados
    users_data = {
    "User_1": {
        "name": "Joaquim Silva", #Nome da pessoa
        "email": "joaquimsilva@gmail.com", #Email da pessoa
        "password": "joaquimsilva", #Password da pessoa
        "type": "user", #Tipo é sempre utilizador
        "verified": True, #Estou a colocar verificado a true, não sei a influencia disto
        "hidden": False, #Indica se o utilizador deve ser ocultado dos restantes
        "banned": False, #Indica se o utilizador está banido
        "fields": [], #Fields adiciona varias opçoes ao user
        "country": "PT", #Country -> abreviatura
        "team": "Team_3"
    },
    "User_2": {
        "name": "Mario Esteves",
        "email": "marioesteves@gmail.com",
        "password": "marioesteves",
        "type": "user",
        "verified": True,
        "hidden": False,
        "banned": False,
        "fields": [],
        "country": "PT",
        "team": "Team_3"
    },
    "User_3": {
        "name": "Jose Antunes",
        "email": "joseantunes@gmail.com",
        "password": "joseantunes",
        "type": "user",
        "verified": True,
        "hidden": False,
        "banned": False,
        "fields": [],
        "country": "PT",
        "team": "Team_2"
    },
    "User_4": {
        "name": "Maria Barcelona",
        "email": "mariabarcelona@gmail.com",
        "password": "mariabarcelona",
        "type": "user",
        "verified": True,
        "hidden": False,
        "banned": False,
        "fields": [],
        "country": "PT",
        "team": "Team_2"
    }
    }

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
    teams_data = {
    "Team_3": {
        "name": "Team 3",
        "password": "joaquimsilvateam",
    },
    "Team_2": {
        "name": "Team 2",
        "password": "joseantunes",
    },
    }

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