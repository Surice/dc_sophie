import discord
from discord.ext import commands


async def fetchUser(client: commands.Bot, user: discord.User or str = None) -> discord.User:
    if(user == None):
            user = client.user

    else:
        try:
            user = await client.fetch_user(user)
        except:
            user = user

    return user


async def pretRes(msg: commands.Context, content: str, color: str= 0x000000) -> None:
    perms = msg.author.permissions_in(msg.channel).embed_links
    if(perms == True):
        embed = discord.Embed(description=content, color=color)
        await msg.reply(embed=embed)
    else:
        await msg.reply(content, mention_author=False)