import os
import json

os.system('cls' if os.name == 'nt' else 'clear') 

os.system("pip install -r requirements.txt")

os.system('cls' if os.name == 'nt' else 'clear') 

if not os.path.exists("config.json"):
    print("config.json not found creating one..")

    bot_token = input("Enter your bot token: ").strip()


    with open("config.json", "w") as config_file:
        json.dump({"token": bot_token}, config_file)
else:
    print("config.json found.")

os.system('cls' if os.name == 'nt' else 'clear') 




os.system("python bot.py")
