import requests
import subprocess

def add_challenges(url, token):
    counter_challenges_vm = 0
    counter_challenges = 0
    
    s = requests.Session() #Abertura de session da API
    s.headers.update({"Authorization": f"Token {token}"}) #Update do header da sessão com o token

    challenges = {
        "Challenge 1": { #Challenge 1 nome genérico apenas para identificação.
            #POST PARA O CHALLENGE
            "name": "Um bom começo com criptografia", #Nome do desafio
            "category": "Crypto", #Categoria
            "description": "Texto encriptado: 'Q1NMQUJ7dEhpU19pU19lTmNSeVB0RWRfSW5fQmFTZTY0fQ=='", #Descrição displayed ao user
            "value": 500, #Valor de pontos que o user ganha ao acertar a pergunta
            "state": "visible", #Estado do desafio, se é visivel ou não para os utilizadores do site
            "type": "standard", #Tipo do desafio??? Em princípio deve ser sempre standard
            "max_attempts": 0, #Número máximo de tentativas. 0 para infinitas
            #POST PARA AS HINTS
            "hint": "Base64 é um ótimo método para criptografar informações.", #Desafios faceis apenas têm uma dica portanto nada de mais
            "hint_cost": 250, #Custo da dica
            #POST PARA A FLAG
            "flag": "CSLAB{tHiS_iS_eNcRyPtEd_In_BaSe64}", #FLAG
            "flag_type": "static", #Tipo da flag, normalmente sempre static
            #POST PARA O FICHEIRO, EM CASO DE NONE SIGNIFICA QUE NÃO POSSUI FICHEIRO PARA ANEXAR AO DESAFIO
            "file_path": None,
            "template_uuid": None,
            "network_uuid": None
        },
        #Mesmos comentarios que acima
        "Challenge 2": {
            "name": "Um ficheiro pode conter muita informação...", 
            "category": "Misc",
            "description": "Tanta informação por ai escondida...",
            "value": 500,
            "state": "visible",
            "type": "standard",
            "max_attempts": 0,
            "hint": "Verifica os metadados do arquivo.",
            "hint_cost": 250,
            "flag": "CSLAB{us3_3x1ft00l}",
            "flag_type": "static",
            "file_path": "data\\chlng_id_3\\shift-appens-ctf.png",  # Caminho para o arquivo
            "template_uuid": None,
            "network_uuid": None
        },
        "Challenge 3": {
            "name": "Jogo das escondidas",
            "category": "Misc",
            "description": "Quem nunca escondeu algo dentro de um arquivo?",
            "value": 1000,
            "state": "visible",
            "type": "standard",
            "max_attempts": 0,
            "hint": "Experimenta utilizar steghide para descobrir o que a imagem tem por trás",
            "hint_cost": 250,
            "flag": "CSLAB{0h_N0_U_f0und_m3}",
            "flag_type": "static",
            "file_path": "data\\chlng_id_4\\departamento_eng_informatica.jpg",  # Caminho para o arquivo
            "template_uuid": None,
            "network_uuid": None
        },
        "Challenge 4": {
            "name": "Um Código estranho...",
            "category": "Misc",
            "description": "Isto está na moda",
            "value": 500,
            "state": "visible",
            "type": "standard",
            "max_attempts": 0,
            "hint": "Experimenta utilizar um digitalizador de QRCodes.",
            "hint_cost": 250,
            "flag": "CSLAB{QR_C0d€_ls_Us3ful}",
            "flag_type": "static",
            "file_path": "data\\chlng_id_5\\qr-code.png",  # Caminho para o arquivo
            "template_uuid": None,
            "network_uuid": None
        },
        "Challenge 5": {
            "name": "Nem todos os arquivos são normais...",
            "category": "Misc",
            "description": "Nunca vi um arquivo de tal tipo. Deveria explorar não?",
            "value": 500,
            "state": "visible",
            "type": "standard",
            "max_attempts": 0,
            "hint": "Experimenta utilizar um editor de texto.",
            "hint_cost": 250,
            "flag": "CSLAB{H1dD3N_Beh1nD_3v3ryt1ng}",
            "flag_type": "static",
            "file_path": "data\\chlng_id_6\\hidden_flag.cslab",  # Caminho para o arquivo
            "template_uuid": None,
            "network_uuid": None
        },
        "Challenge 6": {
            "name": "Teste VM",
            "category": "",
            "description": "Test VM",
            "value": 500,
            "state": "visible",
            "type": "standard",
            "max_attempts": 0,
            "hint": "Test VM",
            "hint_cost": 250,
            "flag": "Test_Flag",
            "flag_type": "static",
            "file_path": None,
            "template_uuid": "988fb130-5eb2-1a2c-cba2-d41b1dd5f5a6",
            "network_uuid": "ea5aca40-b7d2-b896-5efd-dce07151d4ba"
        }
    }

    for challenge_name, challenge_data in challenges.items():
        # Criação de desafios, percorrendo o dicionário

        challenge_response = s.post(
            f"{url}/challenges", #Post para challenges
            json={k: v for k, v in challenge_data.items() if k not in ['hint', 'hint_cost', 'flag', 'flag_type', 'file_path', 'template_uuid', 'network_uuid']},
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
