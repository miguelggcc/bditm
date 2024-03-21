import os
import datetime
from datetime import date
import locale
import discord
from discord.ext import commands, tasks
from sydney import SydneyClient
import re
from check_live import check_live
from random_line import random_line

description = '''Un botapio sustituto para lo que importa: cancelaños y días internacionales'''
bot = commands.Bot(command_prefix="!", description=description,
                   intents=discord.Intents.all())
# Create the time on which the task should always run
trigger_time = datetime.time(hour=11, minute=00, second=0)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You can't do that")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing arguments")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found")
    else:
        raise error


def get_prompt(screenplay, extra, date):
    text = open(screenplay, "r", encoding='utf-8').read()
    return text.replace('$', date) + " " + random_line((open(extra, "r", encoding='utf-8')))

async def message(channel):
    locale.setlocale(locale.LC_TIME, 'es_ES')
    d = date.today().strftime("%d de %B")

    async with SydneyClient(style="creative") as sydney:
        await sydney.start_conversation()

        prompt1 = get_prompt("cancelanos.txt", "inicio.txt", d)
        print(prompt1)
        bd_response = ""
        async for response in sydney.ask_stream(prompt1):
            bd_response = bd_response+response
        print(bd_response)
        await channel.send(re.sub('\[\^\d\^\]', '', bd_response))

        prompt2 = get_prompt("dias_int.txt", "refes.txt", d)
        print(prompt2)
        ids_response = ""
        async for response2 in sydney.ask_stream(prompt2):
            ids_response = ids_response+response2
        print(ids_response)
        await channel.send(re.sub('\[\^\d\^\]', '', ids_response))

        await sydney.close_conversation()
        
@tasks.loop(time=trigger_time)
async def trigger():
    channel = discord.utils.get(bot.get_all_channels(), name="general")
    await message(channel)


@bot.event
async def on_ready():
    if not trigger.is_running():
        trigger.start()  # If the task is not already running, start it.
        print("Loop for task started")


@trigger.before_loop
async def before_trigger():
    print('waiting...')
    await bot.wait_until_ready()

@bot.command()
async def now(ctx):
    await message(ctx.channel)
    
@bot.command()
async def is_running(ctx):
    if trigger.is_running():
        await ctx.send("Task is running")
    else:
        await ctx.send("Task is not running")


@bot.command()
async def change_time(ctx, s):
    ts = re.split(':', s)
    trigger_time = datetime.time(hour=int(ts[0]), minute=int(ts[1]))
    print(trigger_time)
    trigger.change_interval(time=trigger_time)
    trigger.restart()
    trigger.cancel()
    await ctx.send("Changed trigger time to " + trigger_time.isoformat())


@bot.command()
async def get_time(ctx):
    await ctx.send("Current trigger time is " + trigger_time.isoformat())


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down")
    await bot.close()


@bot.command()
async def is_live(ctx, c):
    await ctx.send(check_live(c))

if __name__ == "__main__":
    token = os.getenv("TOKEN_BDITM")
    bot.run(token)
