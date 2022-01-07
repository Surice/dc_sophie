from components.config import getConfig
import discord
from discord.ext import commands


class Control(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.config = getConfig()


    @commands.command()
    async def afk(self, msg: commands.Context):
        activity = discord.CustomActivity("currently unavailable", emoji="❌")

        if(msg.args[0]):
            activity = ''.join(msg.args).replace(".", " ")

        await self.client.change_presence(status=discord.Status.idle, activity=activity, afk=True)

    @commands.command()
    async def reset(self, msg: commands.Context):
        await self.client.change_presence(activity=discord.CustomActivity(""), status=discord.Status.do_not_disturb, afk=False)
        
def setup(client: commands.Bot) -> None:
    client.add_cog(Control(client))