import discord
from discord.ext import commands

async def findUser(item: str, client: commands.Bot) -> discord.User:
    print(item)
    if(item.startswith('<@')):
        print(item[2: : -1])
        # user = await client.fetch_user(item[2: : -1])
    else:
        user = await client.fetch_user(item)

    return user