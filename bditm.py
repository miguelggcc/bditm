import asyncio
import locale
import discord
from discord.ext import commands
from sydney import SydneyClient
import re
from check_live import check_live
from random_line import random_line

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Hello")
    channel = discord.utils.get(bot.get_all_channels(), name="general")
    await channel.send("Hello I'm BDITMbot")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")
    
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down")
    await bot.close()

@bot.command()
@commands.is_owner()
async def is_live(ctx, c):
    await ctx.send(check_live(c))

from datetime import date
locale.setlocale(locale.LC_TIME, 'es_ES')
date = date.today().strftime("%d de %B")

def get_prompt(screenplay, extra):
    text = open(screenplay, "r", encoding='utf-8').read()
    return text.replace('$', date) + " " + random_line((open(extra, "r", encoding='utf-8')))

@bot.command()
async def ask(ctx):
    async with SydneyClient(style="creative") as sydney:
        await sydney.start_conversation()
    
        prompt = get_prompt("cancelanos.txt", "inicio.txt")
        print(prompt)
        bd_response = ""
        async for response in sydney.ask_stream(prompt):
            bd_response = bd_response+response
        print(bd_response)
        await ctx.send(re.sub('\[\^\d\^\]', '', bd_response))
        
        prompt2 = get_prompt("dias_int.txt", "refes.txt")
        print(prompt2)
        ids_response = ""
        async for response2 in sydney.ask_stream(prompt2):
             ids_response = ids_response+response2
        print(ids_response)
        await ctx.send(re.sub('\[\^\d\^\]', '', ids_response))
    
        await sydney.close_conversation()

import os  
if __name__ == "__main__":
        token = os.getenv("TOKEN_BDITM")
        bot.run(token)
