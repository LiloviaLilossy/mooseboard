import discord
from discord.ext import commands, tasks

from  datetime import datetime, timedelta
import json, asyncio

date_format = '"%m/%d/%Y %H:%M:%S"'

class Basement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trapped_kids = {}
        self.bot.loop.create_task(self.basement_clear())

    def parseTime(self, time):
        # 2d 2h 2m 2s
        parsedTime = timedelta()
        time = time.split()
        for val in time:
            if val[-1] == 'd':
                parsedTime += timedelta(days=int(val[:-1]))
            if val[-1] == 'h':
                parsedTime += timedelta(hours=int(val[:-1]))
            if val[-1] == 'm':
                parsedTime += timedelta(minutes=int(val[:-1]))
            if val[-1] == 's':
                parsedTime += timedelta(seconds=int(val[:-1]))
        return parsedTime

    @commands.command(name='mute', aliases=['basement', 'lock'])
    async def mute(self, ctx, member: discord.Member, *, time: str):
        when_out_of_basement = datetime.now() + self.parseTime(time)
        self.trapped_kids[member.id] = {'basement_time': when_out_of_basement.strftime(date_format),
                                        'channel': ctx.channel.id,
                                        'guild': ctx.guild.id}
        print(self.trapped_kids[member.id])

    async def basement_clear(self):
        await self.bot.wait_until_ready()
        while True:
            to_be_removed = []
            for id in self.trapped_kids.keys():
                basement_time = datetime.strptime(self.trapped_kids[id]['basement_time'], date_format)
                print(basement_time)
                if basement_time <= datetime.now():
                    await self.bot.get_guild(self.trapped_kids[id]['guild']).get_channel(self.trapped_kids[id]['channel']).send('Works')
                    to_be_removed.append(id)
            for id in to_be_removed:
                if id in self.trapped_kids:
                    del self.trapped_kids[id]
            await asyncio.sleep(1)
                

def setup(bot):
    bot.add_cog(Basement(bot))