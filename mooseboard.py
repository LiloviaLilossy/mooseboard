import os
import json

TOKEN = 'your-token-here'

default_call = "?"

import discord
from discord.ext import commands
import random

def write_json(board_list, selected):
    with open("selected.txt", "w") as outfile:
        outfile.write(selected)
        outfile.close()

    with open("board.json", "w") as outfile:
        json_object = json.dumps(board_list, indent = 4)
        outfile.write(json_object)
        outfile.close()

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def index_in_list(a_list, index):
    return index < len(a_list)

try:
    f = open('board.json',) 
    list_of_boards = json.load(f)
    f.close()
except FileNotFoundError:
    list_of_boards = {}

global selected
try:
    f = open('selected.txt') 
    selected = f.read()
    f.close()
except FileNotFoundError:
    selected = ""

bot = commands.Bot(command_prefix=default_call)

@bot.event
async def on_ready():
    print('Logged in as {0}: {1}'.format(bot.user.name, bot.user.id))

@bot.command()
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))

@bot.command()
async def toss(ctx):
    await ctx.send('```The coin landed on: {0}```'.format(random.choice(["Heads", "Tails"])))

@bot.command()
async def tasks(ctx, *args):
    server = str(ctx.guild.id)
    name = str(ctx.author.id)
    if len(ctx.author.roles) > 1:
    # if name == '441578258602131456':
        global selected

        try:
            func = args[0]
        except:
            func = None

        try:
            value = args[1]
        except:
            value = None
        
        try:
            subvalue = args[2]
        except:
            subvalue = None

        if func:
            if func == "new":
                if value:
                    if not list_of_boards.get(server, {}):
                        list_of_boards[server] = {}
                    if not list_of_boards.get(server, {}).get(name, {}):
                        list_of_boards[server][name] = {}
                    list_of_boards[server][name][value] = {}
                    selected = value
                    await ctx.send("```Created a new task board {0}.```".format(value))
                    write_json(list_of_boards, selected)
                else:
                    await ctx.send("```The board name is not given.```")

            elif func == "remove":
                if value:
                    if list_of_boards.get(server, {}).get(name, {}):
                        if is_integer(value):
                            value = int(value)
                            if index_in_list(list_of_boards[server][name], value - 1):
                                key_list = list(list_of_boards[server][name].keys())
                                list_of_boards[server][name].pop(key_list[value - 1])
                                await ctx.send("```Removed the task board '{0}'.```".format(key_list[value - 1]))
                                selected = ""
                                write_json(list_of_boards, selected)
                            else:
                                await ctx.send("```Index does not exist!```")
                    else:
                        await ctx.send("```The board list is empty.```")
                else:
                    await ctx.send("```The board name is not given.```")

            elif func == "sel":
                if selected:
                    if value:
                        if list_of_boards.get(server, {}).get(name, {}):
                            if is_integer(value):
                                value = int(value)
                                if index_in_list(list_of_boards[server][name], value - 1):
                                    key_list = list(list_of_boards[server][name].keys())
                                    selected = key_list[value - 1]
                                    await ctx.send("```The selected board is {0}```".format(selected))
                                    write_json(list_of_boards, selected)
                                else:
                                    await ctx.send("```Index does not exist!```")

            elif func == "add":
                if selected:
                    if args:
                        if list_of_boards.get(server, {}).get(name, {}):
                            for value in args[1:]:
                                list_of_boards[server][name][selected][value] = False
                                await ctx.send("```Added the {0} to {1}```".format(value, selected))
                            write_json(list_of_boards, selected)
                        else:
                            await ctx.send("```The task list is empty.```")
                    else:
                        await ctx.send("```The task is not given.```")
                else:
                    await ctx.send("```A list is not selected.```")

            elif func == "boards":
                if list_of_boards.get(server, {}).get(name, {}):
                    final_string = "No. of boards: {0}\n\n".format(len(list_of_boards[server][name]))
                    for i, keys in enumerate(list_of_boards[server][name]):
                        final_string += "{0}: {1}\n".format(i + 1, keys)
                    await ctx.send("User: **__{1}__**\n```{0}```".format(final_string, str(ctx.author.name)))
                    write_json(list_of_boards, selected)
                else:
                    await ctx.send("```Empty.```")

            elif func == "check":
                if selected:
                    if value:
                        if list_of_boards.get(server, {}).get(name, {}).get(selected, {}):
                            for value in args[1:]:
                                if is_integer(value):
                                    value = int(value)
                                    if index_in_list(list_of_boards[server][name][selected], value - 1):
                                        if not value > len(list_of_boards[server][name][selected].keys()) and not value <= 0:
                                            key_list = list(list_of_boards[server][name][selected].keys())
                                            list_of_boards[server][name][selected][key_list[value - 1]] = True
                                            await ctx.send("```{0} is checked.```".format(key_list[value - 1]))
                                        else:
                                            await ctx.send("```The task list is empty.```")
                                    else:
                                        await ctx.send("```Index does not exist!```")
                                else:
                                    await ctx.send("```{0} is not a number.```".format(value))
                                write_json(list_of_boards, selected)
                        else:
                            await ctx.send("```The task list is empty.```")
                else:
                    await ctx.send("```A list is not selected.```")

            elif func == "uncheck":
                if selected:
                    if value:
                        if list_of_boards.get(server, {}).get(name, {}):
                            if list_of_boards.get(server, {}).get(name, {}).get(selected, {}):
                                for value in args[1:]:
                                    if is_integer(value):
                                        value = int(value)
                                        if index_in_list(list_of_boards[server][name][selected], value - 1):
                                            if not value > len(list_of_boards[server][name][selected].keys()) and not value <= 0:
                                                key_list = list(list_of_boards[server][name][selected].keys())
                                                list_of_boards[server][name][selected][key_list[value - 1]] = False
                                                await ctx.send("```{0} is unchecked.```".format(key_list[value - 1]))
                                            else:
                                                await ctx.send("```The task list is empty.```")
                                        else:
                                            await ctx.send("```Index does not exist!```")
                                    else:
                                        await ctx.send("```{0} is not a number.```".format(value))
                                    write_json(list_of_boards, selected)
                            else:
                                await ctx.send("```The task list is empty.```")
                else:
                    await ctx.send("```A list is not selected.```")
            
            elif func == "pop":
                if selected:
                    if value:
                        if list_of_boards.get(server, {}).get(name, {}):
                            if list_of_boards.get(server, {}).get(name, {}).get(selected, {}):
                                for value in args[1:]:
                                    if is_integer(value):
                                        value = int(value)
                                        if index_in_list(list_of_boards[server][name][selected], value - 1):
                                            if not value > len(list_of_boards[server][name][selected].keys()) and not value <= 0:
                                                key_list = list(list_of_boards[server][name][selected].keys())
                                                list_of_boards[server][name][selected].pop(key_list[value - 1])
                                                await ctx.send("```{0} is poped.```".format(key_list[value - 1]))
                                            else:
                                                await ctx.send("```The task list is empty.```")
                                        else:
                                            await ctx.send("```Index does not exist!```")
                                    else:
                                        await ctx.send("```{0} is not a number.```".format(value))
                                    write_json(list_of_boards, selected)
                else:
                    await ctx.send("```A list is not selected.```")

            elif func == "list":
                if list_of_boards.get(server, {}).get(name, {}):
                    title = "**__{0}__**".format(selected) + "\n"

                    if len(list_of_boards[server][name][selected].keys()) != 0:
                        final_string = ""
                        for key in list_of_boards[server][name][selected]:
                            response = '{0} {1}'
                            check = "[ ]"
                            if list_of_boards.get(server, {}).get(name, {})[selected][key]:
                                check = "[X]"
                            final_string += response.format(check, key) + " \n"
                        final_string = '```' + final_string + '```'
                        await ctx.send(title + final_string)
                        write_json(list_of_boards, selected)
                    else:
                        await ctx.send(title + "```The task list is empty.```")

                else:
                    await ctx.send("```The board list is empty!```")

            else:
                await ctx.send("```Invalid command!```")

        else:
            await ctx.send("```Need a command. I'm not a magician!```")

    else:
        await ctx.send("```You're not my master!```")

bot.run(TOKEN)