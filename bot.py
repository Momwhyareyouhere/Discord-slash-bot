import discord
from discord.ext import commands
from pyslash import SlashCommand, SlashContext
import asyncio
import platform
import random
import os
import json

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
s = SlashCommand(bot, sync_commands=True)



with open("config.json", "r") as config_file:
    config = json.load(config_file)
    TOKEN = config["token"]

@s.slash(name="roll", description="Roll a six-sided dice")
async def _roll(ctx: SlashContext):
    try:
        await ctx.defer()  
        result = random.randint(1, 6)
        await ctx.send(f"You rolled a {result}!")

    except discord.errors.HTTPException as e:
        if e.status == 429:
            await asyncio.sleep(5)  
            raise  
        else:
            raise  


@s.slash(name="ping", description="Show the bot's latency and system information")
async def _ping(ctx: SlashContext):
    try:
        await ctx.defer()  
        latency = round(bot.latency * 1000)  
        python_version = platform.python_version()

        response = f"Pong!\nLatency: **{latency}ms**\nPython Version: **{python_version}**"
        await ctx.send(response)

    except discord.errors.HTTPException as e:
        if e.status == 429:
            await asyncio.sleep(5) 
            raise  
        else:
            raise  


@s.slash(name="ban", description="Ban a member from the server")
async def _ban(ctx: SlashContext, member: discord.Member, reason: str = "No reason provided"):
    try:
        await ctx.defer()
        
        
        if ctx.author == ctx.guild.owner or ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.administrator:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} has been banned. Reason: {reason}")
        else:
            await ctx.send("You do not have permission to ban members.")

    except discord.errors.HTTPException as e:
        if e.status == 429:
            await asyncio.sleep(5) 
            raise  
        else:
            raise  


@s.slash(name="unban", description="Show banned members or unban a member")
async def _unban(ctx: SlashContext):
    try:
        await ctx.defer()
        
        
        if ctx.author == ctx.guild.owner or ctx.author.guild_permissions.ban_members or ctx.author.guild_permissions.administrator:
            bans = await ctx.guild.bans()
            if bans:
                banned_users = {ban.user.id: ban.user.name for ban in bans}

                ban_list_str = "\n".join([f"{user_id}: {username}" for user_id, username in banned_users.items()])
                await ctx.send("Banned members:\n" + ban_list_str)

                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel

                await ctx.send("Please enter the username or user ID of the member you want to unban:")

                while True:
                    try:
                        message = await bot.wait_for("message", check=check, timeout=60)  # Timeout after 60 seconds
                        input_value = message.content
                        try:
                            user_id = int(input_value)
                            if user_id in banned_users:
                                member_to_unban = discord.Object(id=user_id)
                                await ctx.guild.unban(member_to_unban)
                                await ctx.send(f"User with ID {user_id} has been unbanned.")
                                break
                            else:
                                await ctx.send("Invalid user ID. Please try again.")
                        except ValueError:
                            for banned_id, banned_name in banned_users.items():
                                if input_value.lower() in banned_name.lower():
                                    member_to_unban = discord.Object(id=banned_id)
                                    await ctx.guild.unban(member_to_unban)
                                    await ctx.send(f"User {banned_name} has been unbanned.")
                                    break
                            else:
                                await ctx.send("User not found. Please try again.")
                    except asyncio.TimeoutError:
                        await ctx.send("Unban operation timed out.")
                        break
            else:
                await ctx.send("No members are currently banned.")
        else:
            await ctx.send("You do not have permission to unban members.")

    except discord.errors.HTTPException as e:
        if e.status == 429:
            await asyncio.sleep(5)
            raise
        else:
            raise

@s.slash(name="kick", description="Kick a member from the server")
async def _kick(ctx: SlashContext, member: discord.Member, reason: str = "No reason provided"):
    try:
        await ctx.defer()
        
        
        if ctx.author == ctx.guild.owner or ctx.author.guild_permissions.kick_members or ctx.author.guild_permissions.administrator:
            await member.kick(reason=reason)
            await ctx.send(f"{member.mention} has been kicked. Reason: {reason}")
        else:
            await ctx.send("You do not have permission to kick members.")

    except discord.errors.HTTPException as e:
        if e.status == 429:
            await asyncio.sleep(5) 
            raise  
        else:
            raise

@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear') 
    print(f"Logged in as {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print(f"Invite Link: https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot+applications.commands")

@s.slash(name="invite", description="DMs the member with the bot invite link")
async def _invite(ctx: SlashContext):
    try:
        await ctx.defer()
        
        invite_link = f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot+applications.commands"
        await ctx.author.send(f"[Invite Link]({invite_link})")
        await ctx.send("Invite link has been sent to your DMs.")
        
    except discord.errors.HTTPException as e:
        if e.status == 429:
            await asyncio.sleep(5) 
            raise  
        else:
            raise


bot.run(bot.run(TOKEN))
