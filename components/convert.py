import discord
from discord.ext import commands


async def fetchUser(client: commands.Bot, user: discord.User or str = None) -> discord.User:
    if(user == None):
            user = client.user

    else:
        try:
            user = await client.fetch_user(user)
        except:
            user = await client.fetch_user(user.id)

    return user