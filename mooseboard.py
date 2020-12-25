import os, json, dotenv

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

import discord
from discord.ext import commands

from cogs import greetings, facts, stats, python, basement

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.members = True
    greetings.setup(bot)
    facts.setup(bot)
    stats.setup(bot)
    python.setup(bot)
    basement.setup(bot)

bot.run(TOKEN)