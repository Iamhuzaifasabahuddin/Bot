
import os
import discord
from discord.ext import commands
from secrets import randbelow
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=['!', "$"], intents=intents)


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
async def random_(ctx, start: int, end: int):
    random_generated = random.randrange(start, end+1)
    await ctx.send(f"Random Number Generated is: {random_generated}!")



bot.run(os.environ["DISCORD_TOKEN"])
