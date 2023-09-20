import os
import discord
from discord.ext import commands
from secrets import randbelow
import random
import requests
import json

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=['!', "$"], intents=intents)


def quote_generator():
    response = requests.get('https://zenquotes.io/api/random')
    data = json.loads(response.content)
    quote = data[0]['q'] + '~' + data[0]['a']
    return quote


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def inspired(ctx):
    quote = quote_generator()
    await ctx.send(f"Quote for {ctx.author.mention} is {quote}")


@bot.command()
async def random_(ctx, start: int, end: int):
    random_generated = random.randrange(start, end + 1)
    await ctx.send(f"Random Number Generated is: {random_generated}!")


bot.run(os.environ["DISCORD_TOKEN"])
