import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_hug = None
        self.last_hello = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command(name='hello', aliases=['adios'])
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        if self.last_hello == member:
            await ctx.send('Hello again, {0}.'.format(member.display_name))
        else:
            await ctx.send('Hello there, {0}.'.format(member.display_name))

        self.last_hello = member

    @commands.command(name='hug')
    async def hug(self, ctx, *, member: discord.Member = None):
        if member == ctx.author:
            if self.last_hug == (ctx.author, member):
                await ctx.send('For the love of god, someone hug this bastard!')
            elif self.last_hug[1] == member:
                await ctx.send('You got a hug once. Pretty sure, you\'ll get one again.')
            else:
                await ctx.send('Dude, you can\'t hug yourself.')
        elif member is not None:
            await ctx.send('{0} hugs {1}.'.format(ctx.author.display_name, member.display_name))
        else:
            await ctx.send('Choose someone to hug, dumbass.')

        self.last_hug = (ctx.author, member)

def setup(bot):
    bot.add_cog(Greetings(bot))