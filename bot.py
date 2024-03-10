import discord
from discord.ext import commands
from pyslash import SlashCommand, SlashContext

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
s = SlashCommand(bot, sync_commands=True)

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

bot.run("YOUR_BOT_TOKEN")
