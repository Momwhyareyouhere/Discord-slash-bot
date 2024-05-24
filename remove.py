import discord
import asyncio
import json
import os
from discord.ext import commands

config_file = 'config.json'


if not os.path.exists(config_file):
    print("Run first runme.py")
    exit()


with open(config_file) as f:
    config = json.load(f)

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    application_id = bot.user.id  
    headers = {
        "Authorization": f"Bot {bot.http.token}"
    }
    

    url = f"https://discord.com/api/v10/applications/{application_id}/commands"
    async with bot.http._HTTPClient__session.get(url, headers=headers) as response:
        if response.status == 200:
            commands = await response.json()
            for command in commands:
                delete_url = f"https://discord.com/api/v10/applications/{application_id}/commands/{command['id']}"
                async with bot.http._HTTPClient__session.delete(delete_url, headers=headers) as del_response:
                    if del_response.status == 204:
                        print(f"Successfully deleted global command: {command['name']}")
                    else:
                        print(f"Failed to delete global command: {command['name']} - Status: {del_response.status}")
                await asyncio.sleep(1)  
        else:
            print(f"Failed to fetch global commands: {response.status}")
    
    await bot.close()  

bot.run(config['token'])
