import os
import discord
from discord.ext import commands
from secrets import randbelow
import random
import requests
import json

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=['!', "$", '@'], intents=intents)


def quote_generator():
    response = requests.get('https://zenquotes.io/api/random')
    data = json.loads(response.content)
    quote = data[0]['q'] + ' ~ ' + data[0]['a']
    return quote


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def hello(ctx):
    """Greets the User"""
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command()
async def contact(ctx):
    """Returns Contact details"""
    embed = discord.Embed(title="Contact Details: ")
    embed.add_field(name="Github", value="[GITHUB]"
                                         "(https://github.com/Iamhuzaifasabahuddin/Python-Personal-Projects)"
                    , inline=False)
    embed.add_field(name="LinkedIn", value="[LinkedIn](https://www.linkedin.com/in/huzaifa-sabah-uddin/",
                    inline=False)
    embed.add_field(name="Email", value="Huzaifasabah@gmail.com", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def inspired(ctx):
    """Generates a random quote for the user"""
    quote = quote_generator()
    await ctx.send(f"Quote for {ctx.author.mention}\n{quote}")


@bot.command()
async def random_(ctx, start: int = None, end: int = None):
    """Generates a random number from user provided range"""
    if start is not None and end is not None:
        random_generated = random.randrange(start, end + 1)
        await ctx.send(f"Random generated number is: {random_generated}!")
    elif start is None or end is None:
        await ctx.send(f"Enter a range to generate random number!")


@bot.command()
async def getrecipe(ctx, query, number):
    """Searches for desired number of recipes of any given product"""
    url = f"https://api.edamam.com/search"

    params = {
        "app_id": os.environ["APP_ID"],
        "app_key": os.environ["API_KEY"],
        "q": query,
        "to": number
    }
    response = requests.get(url, params=params)
    data = response.json()

    for recipe in data['hits']:
        recipe = recipe['recipe']
        embed = discord.Embed(title=recipe['label'], url=recipe['url'])
        embed.add_field(name="Calories", value=recipe['calories'])
        embed.add_field(name="Diet Labels", value=", ".join(recipe['dietLabels']))
        embed.add_field(name="Health Labels", value=", ".join(recipe['healthLabels']))
        ingredients = "\n".join(recipe['ingredientLines'])
        embed.add_field(name="Ingredients", value=ingredients, inline=False)
        await ctx.send(embed=embed)


bot.run(os.environ["DISCORD_TOKEN"])
