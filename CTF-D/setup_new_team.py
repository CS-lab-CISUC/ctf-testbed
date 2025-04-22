import os
from dotenv import load_dotenv
import requests
import json

import initialize_event
################################################################################################################################################################################################################################################
####################################################      ADD Challenges     ############################################################################################################################################################
################################################################################################################################################################################################################################################

def setup_new_team():
    load_dotenv()
    url = os.getenv("CTFD_URL")
    token = os.getenv("CTFD_TOKEN")

    if not url or not token:
        print("Erro: CTFD_URL ou CTFD_TOKEN não definidos no .env")
        return

    counter_teams = initialize_event.add_users(url, token, users_file="setup_new_users.json", teams_file="setup_new_teams.json")

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
    setup_new_team()
