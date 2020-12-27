import os, json, dotenv

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

import discord
from discord.ext import commands

# from cogs import greetings, facts, stats, python, basement
cogs = ["cogs.greetings", "cogs.facts", "cogs.stats", "cogs.python", "cogs.basement"]

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

if __name__ == "__main__":
    for cog in cogs:
        bot.load_extension(cog)

    bot.run(TOKEN)
