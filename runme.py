import os
import json


if not os.path.exists("config.json"):

    bot_token = input("Enter your bot token: ").strip()


    with open("config.json", "w") as config_file:
        json.dump({"token": bot_token}, config_file)
else:
    print("config.json found.")


os.system("pip install -r requirements.txt")


os.system("python bot.py")
