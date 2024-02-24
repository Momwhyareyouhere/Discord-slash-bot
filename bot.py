import discord
from discord.ext import commands
from pyslash import SlashCommand, SlashContext

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
s = SlashCommand(bot, sync_commands=True)

@s.slash(name="ping", description="Check the bot's latency.")
async def _ping(ctx: SlashContext):

    latency = round(ctx.bot.latency * 1000)  

    await ctx.send(f"Pong! Latency: {latency}ms")

bot.run("YOUR_BOT_TOKEN")
