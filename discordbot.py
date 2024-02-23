import discord
from discord.ext import commands
from pyslash import SlashCommand, SlashContext

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
s = SlashCommand(bot, sync_commands=True)

@s.slash(name="ping", description="Check the bot's latency.")
async def _ping(ctx: SlashContext):
    # Calculate the latency of the bot
    latency = round(ctx.bot.latency * 1000)  # in milliseconds

    # Respond to the user with the ping information
    await ctx.send(f"Pong! Latency: {latency}ms")

bot.run("YOUR_BOT_TOKEN")
