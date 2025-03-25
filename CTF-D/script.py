import add_challenge
import add_user
import os
from dotenv import load_dotenv

def main():
    load_dotenv()  
    url = os.getenv("CTFD_URL")
    token = os.getenv("CTFD_TOKEN")


    counter_challenges, counter_challenges_vm = add_challenge.add_challenges(url, token)
    counter_teams = add_user.add_users(url, token)
    if counter_challenges > 0 and  counter_teams > 0: #Consideremos que a adição dos challenges e dos utilizados funciona se o contador for maior que 0
        print(f"Counter_challenges = {counter_challenges}, Counter_Challenges_VM = {counter_challenges_vm}")
        print(f"Counter_teams = {counter_teams}")

if __name__ == "__main__":
    main()
