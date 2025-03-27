import os
from dotenv import load_dotenv
import requests
import json


################################################################################################################################################################################################################################################
####################################################      ADD Challenges     ############################################################################################################################################################
################################################################################################################################################################################################################################################





def add_challenges(url, token,challenges_file="challenges.json"):
    counter_challenges_vm = 0
    counter_challenges = 0
    
    s = requests.Session() #Abertura de session da API
    s.headers.update({"Authorization": f"Token {token}"}) #Update do header da sessão com o token

    try:
        with open(challenges_file, "r", encoding="utf-8") as f:
            challenges = json.load(f)
    except FileNotFoundError:
        print(f"Ficheiro '{challenges_file}' não encontrado.")
        return 0, 0
    except json.JSONDecodeError as e:
        print(f"Erro a fazer parsing do ficheiro JSON: {e}")
        return 0, 0
    
    for challenge_name, challenge_data in challenges.items():
        # Criação de desafios, percorrendo o dicionário

        challenge_response = s.post(
            f"{url}/challenges", #Post para challenges
            json={k: v for k, v in challenge_data.items() if k not in ['hint', 'hint_cost', 'flag', 'flag_type', 'file_path', 'template_uuid', 'network_uuid', 'user', 'password', 'commands','ImAModule']},
            #Json com a data do desafio, ou seja, envia apenas os dados necessários para criação do desafio
            headers={"Content-Type": "application/json"} #header
        )
        
        if challenge_response.status_code == 200: #Em caso de resposta de sucesso
            print(f"Challenge '{challenge_name}' criado com sucesso!")
            counter_challenges += 1
            # Obter o ID do challenge criado

            challenge_id = challenge_response.json().get("data", {}).get("id") #Obtém o id do challenge criado
            # Adicionar a flag
            flag_data = { #Data para definição da flag para o desafio criado anteriormente
                "challenge_id": challenge_id,  
                "content": challenge_data['flag'],
                "type": challenge_data['flag_type']
            }
            flag_response = s.post(f"{url}/flags", json=flag_data, headers={"Content-Type": "application/json"}) #Post para criação da flag
            print(f"Flag adicionada: {flag_response.json()}") #print para debug

            # Adicionar a dica
            hint_data = { #Data para adição da dica ao challenge criado anteriormente
                "challenge_id": challenge_id,
                "content": challenge_data['hint'],
                "cost": challenge_data['hint_cost']
            }
            hint_response = s.post(f"{url}/hints", json=hint_data, headers={"Content-Type": "application/json"}) #Post para criação da dica
            print(f"Dica adicionada: {hint_response.json()}")

            # Verificar se há um arquivo para upload
            file_path = challenge_data.get("file_path") #Verifica se no challenge data a flag que possui ficheiro de texto não é None
            if file_path:
                try:
                    with open(file_path, 'rb') as file: #Abertura para leitura do ficheiro como ficheiro binário
                        file_response = s.post( #Post para o endpoint de ficheiros
                            f"{url}/files",
                            files=[("file", file)],
                            data={"challenge_id": challenge_id, "type": "challenge"}, #Data contém o challenge_id com o type a challenge
                        )

                    if file_response.status_code == 200: #Mensagens para debug em caso de sucesso/falha
                        print("Arquivo enviado com sucesso!")
                        print(f"Resposta do upload: {file_response.json()}")  # Exibir resposta do upload
                    else:
                        print(f"Erro ao enviar arquivo: {file_response.status_code}, {file_response.text}")
                except FileNotFoundError:
                    print(f"Arquivo '{file_path}' não encontrado!")
            else:
                print("Nenhum arquivo para enviar.")

            
            #Verifica se é um challenge que necessita de dar start a uma VM
            if challenge_data["template_uuid"] and challenge_data["network_uuid"]: #Caso o atributo não seja None, executa os seguintes comandos:
                #subprocess.run(["ls", "-l"]) #Uso do subprocess.run para fazer a utilização de parâmetros e ser mais simples.
                #subprocess.run(["pwd"])
                counter_challenges_vm += 1




            
        else:
            print(f"Erro ao criar challenge '{challenge_name}': {challenge_response.status_code}, {challenge_response.text}")



        #Get Challenges
        '''
        challenge_response = s.get(f"{url}/challenges")
        with open("info_challenges.txt", "w") as f:
            f.write(str(challenge_response.json()))

        files_response = s.get(f"{url}/files")
        with open("info_files.txt", "w") as f:
            f.write(str(files_response.json()))
        '''


    return counter_challenges, counter_challenges_vm


################################################################################################################################################################################################################################################
####################################################       ADD USERS      ############################################################################################################################################################
################################################################################################################################################################################################################################################




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
        "team": "Team_2"
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
        "team": "Team_2"
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
        "team": "Team_3"
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
        "team": "Team_3"
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
    "Team_2": {
        "name": "Team 2",
        "password": "joaquimsilvateam",
    },
    "Team_3": {
        "name": "Team 3",
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






################################################################################################################################################################################################################################################
#######################################################       Main      ############################################################################################################################################################
################################################################################################################################################################################################################################################



def main():
    load_dotenv()  
    url = os.getenv("CTFD_URL")
    token = os.getenv("CTFD_TOKEN")

    if not url or not token:
        print("Erro: CTFD_URL ou CTFD_TOKEN não definidos no .env")
        return

        
    counter_challenges, counter_challenges_vm = add_challenges(url, token)
    counter_teams = add_users(url, token)
    if counter_challenges > 0 and  counter_teams > 0: #Consideremos que a adição dos challenges e dos utilizados funciona se o contador for maior que 0
        print(f"Counter_challenges = {counter_challenges}, Counter_Challenges_VM = {counter_challenges_vm}")
        print(f"Counter_teams = {counter_teams}")
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
            "num_teams": counter_teams
        }
        response = requests.post("http://127.0.0.1:5000/create-vms", json=payload)
        print("\nResposta do servidor Flask:", response.text)

        session.close()


if __name__ == "__main__":
    main()
