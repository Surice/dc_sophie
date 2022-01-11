from components.config import getConfig
import discord
from discord.ext import commands


class Automation(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.config = getConfig()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Client logged in as {0.user}'.format(self.client))
        await self.client.change_presence(status=discord.Status.do_not_disturb)

    @commands.Cog.listener()
    async def on_member_update(self, oldState, newState):
        if(newState.id != self.client.user.id):
            return

        if(oldState.guild.id != self.config['defaultGuildId']):
            return

        print("value Changed on:", newState.guild.id)
        if(oldState.desktop_status == newState.desktop_status and oldState.mobile_status == newState.mobile_status):
            return
        if(str(newState.desktop_status) != "offline" or str(newState.mobile_status) != "offline"):
            if(str(oldState.desktop_status) == "offline" and str(oldState.mobile_status) == "offline"):
                await self.client.change_presence(activity=discord.CustomActivity(""), status=discord.Status.do_not_disturb, afk=False)

            return

        activity = discord.CustomActivity("currently unavalible", emoji="❌")
        await self.client.change_presence(status=discord.Status.idle, activity=activity, afk=True)


    @commands.Cog.listener(name="on_message_delete")
    async def on_message_delete(self, msg: commands.Context):
        if(msg.author.bot):
            return

        self.client.snipe_message_author[msg.channel.id] = msg.author
        self.client.snipe_message_content[msg.channel.id] = msg.content


def setup(client: commands.Bot) -> None:
    client.add_cog(Automation(client))
    