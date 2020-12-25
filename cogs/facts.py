import json, requests, random
import discord
from discord.ext import commands

class Facts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cat', aliases=['feline'])
    async def cat(self, ctx):
        data = requests.get('https://catfact.ninja/facts').json()['data'][0]
        await ctx.send('{0}'.format(data['fact']))
    
    @commands.command(name='toss')
    async def toss(self, ctx, *args):
        if not args:
            await ctx.send(f'{random.choice(["Heads", "Tails"])}')
            return
        elif len(args) > 2:
            await ctx.send('Need only two items, baka~')
            return
        await ctx.send(f'{random.choice(args)}')

def setup(bot):
    bot.add_cog(Facts(bot))