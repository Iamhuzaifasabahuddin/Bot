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
    """Sends a message to the server that the bot is ready!"""
    print(f"Logged in as {bot.user.name}")
    guild_id = int(os.environ['SERVER_ID'])
    guild = bot.get_guild(guild_id)
    responses = ["HEY HEY HEY", "LETS GET THE PARTY STARTED PEOPLE", "GUESS WHOSE BACK"]
    selected = random.choice(responses)
    if guild is not None:
        channel = guild.get_channel(int(os.environ["CHANNEL_ID"]))
        if channel is not None:
            await channel.send(f"@everyone {selected}")
        admin_id = int(os.environ['ADMIN_ID'])
        admin = await bot.fetch_user(admin_id)
        if admin is not None:
            await admin.send("Bot is fully functional!")
        else:
            print(f"Invalid admin ID: {admin_id}")
    else:
        print(f"GUILD with ID {guild_id} not found!")


@bot.command()
async def hello(ctx):
    """Greets the User"""
    responses = ["HI THERE", "HOLA", "HIYA", "HELLO", "HEY", "HEY THERE", "GREAT TO SEE YOU"]
    selected = random.choice(responses)
    await ctx.send(f"{selected} {ctx.author.mention}!")


@bot.command()
async def contact(ctx):
    """Returns Contact details"""
    embed = discord.Embed(title="Contact Details: ")
    embed.add_field(name="Github Repository", value="[GITHUB]"
                                                    "(https://github.com/Iamhuzaifasabahuddin/Python-Personal-Projects)"
                    , inline=False)
    embed.add_field(name="LinkedIn Profile", value="[LinkedIn](https://www.linkedin.com/in/huzaifa-sabah-uddin/)",
                    inline=False)
    embed.add_field(name="Email Address", value="Huzaifasabah@gmail.com", inline=False)
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
async def getrecipe(ctx, *, query_and_nums: str):
    """Searches for the desired number of recipes for a given product"""

    query = " ".join(query_and_nums.split()[:-1])
    nums = query_and_nums.split()[-1] if query_and_nums.split()[-1].isdigit() else 5
    if not any(c.isalpha() for c in query):
        await ctx.send("Please provide a more descriptive recipe query with at least one word.")
        return
    url = f"https://api.edamam.com/search"
    params = {
        "app_id": os.environ["APP_ID"],
        "app_key": os.environ["API_KEY"],
        "q": query,
        "to": nums
    }
    response = requests.get(url, params=params)
    data = response.json()

    for recipe in data['hits']:
        recipe = recipe['recipe']
        embed = discord.Embed(title=f"_{recipe['label']}_", url=recipe['url'])
        embed.add_field(name="_Calories_", value=round(recipe['calories'], 2))
        embed.add_field(name="_Diet Labels_", value=", ".join(recipe['dietLabels']))
        embed.add_field(name="_Health Labels_", value=", ".join(recipe['healthLabels']))
        ingredients = recipe['ingredientLines']

        # embed.add_field(name="_Ingredients List_: ", value="")
        # for i, ingredient in enumerate(ingredients, start=1):
        #     embed.add_field(name=f"{i}) {ingredient}", value="\u200b", inline=False)

        ingredients_list = ", ".join([f"{i}) {ingredient}" for i, ingredient in enumerate(ingredients, start=1)])
        embed.add_field(name="_Ingredients List_:", value=ingredients_list, inline=False)

        await ctx.send(embed=embed)


# @bot.command()
# async def ily(ctx):
#     await ctx.author.send(f" <@{1154756034473234492}> I LOVE YOU BABY!")

@bot.command()
async def ily(ctx):
    try:
        love_reponses = ["LOVE YOU BABES", "LOVE YOU WIFEY", "TE QUEIRO ESPOSA", "LOVE YOU MY LOVELIEST",
                         "LOVE YAAA DARLING"]
        selected = random.choice(love_reponses)
        target_user = await ctx.guild.fetch_member(int(os.environ["REEVAS_ID"]))
        await target_user.send(f"<@{int(os.environ['REEVAS_ID'])}> {selected}!")
    except discord.errors.NotFound:
        await ctx.send("Target user not found.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


if __name__ == '__main__':
    bot.run(os.environ["DISCORD_TOKEN"])
