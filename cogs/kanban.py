import discord
from discord.ext import commands

class Kanban(commands.Cog):
    def __init__(self, bot):
        pass

def setup(bot):
    bot.add_cog(Kanban(bot))