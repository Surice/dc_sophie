from components.config import getConfig
import discord
from discord.ext import commands


class Control(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.config = getConfig()


    @commands.command()
    async def afk(self, ctx):
        activity = discord.CustomActivity("currently unavailable", emoji="❌")

        if()
        await self.client.change_presence(status=discord.Status.idle, activity=activity, afk=True)

    @commands.command()
    async def reset(self, ctx):
        await self.client.change_presence(activity=discord.CustomActivity(""), status=discord.Status.do_not_disturb, afk=False)
        
def setup(client: commands.Bot) -> None:
    client.add_cog(Control(client))