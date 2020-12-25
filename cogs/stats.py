import discord
from discord.ext import commands, tasks
from collections import defaultdict

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mute_role = ['muted']
        self.moderator_role = ["mod", 'moderator']

        self.founder_role = ['admin']
        self.team_lead_role = ['team lead']
        self.writer_role = ['writer']
        self.artist_role = ['artist']
        self.coder_role = ['coder']
        self.musician_role = ['music composer']
        self.pr_role = ['pr']


    @commands.command(name='setmuterole')
    async def setmuterole(self, ctx, *, role: str):
        if ctx.message.author.guild_permissions.administrator or ctx.author.id == 441578258602131456:
            self.mute_role.append(role.lower())
            await ctx.send(f'Successfully appended {role} to Muted Roles.')
        else:
            await ctx.send(f'You don\'t have enough permissions for that, {ctx.author.display_name}.')

    @commands.command(name='setmodrole')
    async def setmodrole(self, ctx, *, role: str):
        if ctx.message.author.guild_permissions.administrator or ctx.author.id == 441578258602131456:
            self.moderator_role.append(role.lower())
            await ctx.send(f'Successfully appended {role} to Moderator Roles.')
        else:
            await ctx.send(f'You don\'t have enough permissions for that, {ctx.author.display_name}.')

    async def getMembersInfo(self, ctx):
        member_count, bot_count = 0, 0
        muted_users, moderators = [], []
        members = await ctx.guild.fetch_members().flatten()

        for member in members:
            if member.bot:
                bot_count += 1
            else:
                if any([True for r in member.roles if r.name.lower() in self.moderator_role]):
                    moderators.append(member.name)

                if any([True for r in member.roles if r.name.lower() in self.mute_role]):
                    muted_users.append(member.name)

                member_count += 1

        return len(members), member_count, bot_count, muted_users, moderators

    async def getStaffInfo(self, ctx):
        staff_info = defaultdict(lambda: [])

        members = await ctx.guild.fetch_members().flatten()

        for member in members:
            if not member.bot:
                if any([True for r in member.roles if r.name.lower() in self.founder_role]):
                    staff_info[tuple(self.founder_role)].append(member.name)

                if any([True for r in member.roles if r.name.lower() in self.team_lead_role]):
                    staff_info[tuple(self.team_lead_role)].append(member.name)

                if any([True for r in member.roles if r.name.lower() in self.writer_role]):
                    staff_info[tuple(self.writer_role)].append(member.name)

                if any([True for r in member.roles if r.name.lower() in self.artist_role]):
                    staff_info[tuple(self.artist_role)].append(member.name)

                if any([True for r in member.roles if r.name.lower() in self.coder_role]):
                    staff_info[tuple(self.coder_role)].append(member.name)

                if any([True for r in member.roles if r.name.lower() in self.musician_role]):
                    staff_info[tuple(self.musician_role)].append(member.name)

                if any([True for r in member.roles if r.name.lower() in self.pr_role]):
                    staff_info[tuple(self.pr_role)].append(member.name)

        return staff_info

    @commands.command(name='stats')
    async def stats(self, ctx):
        all_members_count, member_count, bot_count, muted_users, moderators = await self.getMembersInfo(ctx)

        moderators = ', '.join(moderators) or "None"
        muted_users = ', '.join(muted_users) or "None"
        embed=discord.Embed(title="__Stats of {}__".format(ctx.guild.name), color=0x70dbff)
        embed.add_field(name="Total Members", value=all_members_count, inline=False)
        embed.add_field(name="Members", value=member_count, inline=True)
        embed.add_field(name="Bot", value=bot_count, inline=True)
        embed.add_field(name="Moderators", value=moderators, inline=False)
        embed.add_field(name="Residents of Sock's Basement", value=muted_users, inline=True)
        embed.set_footer(text="MooseBoard. Team Icebreaker ©")
        await ctx.send(embed=embed)

    @commands.command(name='team')
    async def team(self, ctx):
        staffInfo = await self.getStaffInfo(ctx)

        founder = ', '.join(staffInfo[tuple(self.founder_role)]) or "None"
        team_leads = ', '.join(staffInfo[tuple(self.team_lead_role)]) or "None"
        writers = ', '.join(staffInfo[tuple(self.writer_role)]) or "None"
        artists = ', '.join(staffInfo[tuple(self.artist_role)]) or "None"
        coders = ', '.join(staffInfo[tuple(self.coder_role)]) or "None"
        musicians = ', '.join(staffInfo[tuple(self.musician_role)]) or "None"
        pr = ', '.join(staffInfo[tuple(self.pr_role)]) or "None"

        embed=discord.Embed(title="__Meet the Team__", color=0x70dbff)
        embed.add_field(name="Founder", value=founder, inline=False)
        embed.add_field(name="Team Leads", value=team_leads, inline=False)
        embed.add_field(name="Writers", value=writers, inline=False)
        embed.add_field(name="Artists", value=artists, inline=False)
        embed.add_field(name="Coders", value=coders, inline=False)
        embed.add_field(name="Composers", value=musicians, inline=False)
        embed.add_field(name="PR", value=pr, inline=True)
        embed.set_footer(text="MooseBoard. Team Icebreaker ©")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Stats(bot))