import discord
from discord.ext import commands

class Python(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='eval')
    async def eval(self, ctx, *, cmd: str):
        await ctx.send('{0}'.format(eval(cmd)))

    @commands.is_owner()
    @commands.command(name='exec')
    async def exec(self, ctx, *, cmd: str):
        await ctx.send('{0}'.format(exec(cmd)))


def setup(bot):
    bot.add_cog(Python(bot))
