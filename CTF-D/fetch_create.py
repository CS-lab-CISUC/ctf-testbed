import requests
import os
from dotenv import load_dotenv

def fetch_challenges(session, url):
    response = session.get(f"{url}/challenges")
    if response.status_code == 200:
        challenges = response.json().get("data", [])
        print("\n=== Lista de Challenges ===")
        for challenge in challenges:
            print(f"- ID: {challenge['id']} | Nome: {challenge['name']} | Categoria: {challenge['category']} | Valor: {challenge['value']}")
        return challenges
    else:
        print("Erro ao obter challenges:", response.text)
        return []

def fetch_teams_and_members(session, url):
    response = session.get(f"{url}/teams")
    if response.status_code == 200:
        teams = response.json().get("data", [])
        print("\n=== Lista de Equipas ===")
        for team in teams:
            print(f"\n> Equipa: {team['name']} (ID: {team['id']})")
            members_resp = session.get(f"{url}/teams/{team['id']}/members")
            if members_resp.status_code == 200:
                members = members_resp.json().get("data", [])
                if members:
                    for member in members:
                        print(f"  - {member['name']} ({member['email']})")
                else:
                    print("  [Sem membros]")
            else:
                print("  Erro ao obter membros:", members_resp.text)
        return teams
    else:
        print("Erro ao obter equipas:", response.text)
        return []

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

    fetch_challenges(session, url)
    fetch_teams_and_members(session, url)

    session.close()

if __name__ == "__main__":
    main()
