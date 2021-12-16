from components.config import getConfig
from components.convert import fetchUser, pretRes
import discord
from discord.ext import commands


class Feelings(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.config = getConfig()


    @commands.command()
    async def love(self, msg: commands.Context, user: discord.User = None):
        user = await fetchUser(self.client, user)

        await pretRes(msg, f"{self.client.user.mention} hat {user.mention} ganz dolle lieb ❤️", 0xFF0000)

    @commands.command()
    async def arsch(self, msg: commands.Context, user: discord.User = None):
        user = await fetchUser(self.client, user)

        await pretRes(msg, f"{user.display_name} ist ein Arsch! <:nani:663857832256471084>", 0xFF0000)

    @commands.command()
    async def unimpressed(self, msg: commands.Context, user: discord.User = None):
        user = await fetchUser(self.client, user)
        userPropertie = ""
        if(user != None):
            userPropertie = f"von ${user.mention} "

        await pretRes(msg, f"{self.client.user.mention} ist ${userPropertie}nicht beeindruckt... ")

def setup(client: commands.Bot) -> None:
    client.add_cog(Feelings(client))
