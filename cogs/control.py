from os import name
import discord
from discord.ext import commands


class Controlling(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(brief='shutdown the bot client')
    async def close(self, ctx):
        await ctx.message.reply(f"> destroy bot client", mention_author=False)

        await self.bot.close()
    
    @commands.command(name="update")
    async def update(self, ctx):
        await self.bot.change_presence(status=discord.Status.do_not_disturb)
        await ctx.message.reply("presence updated ✅", mention_author=False)

def setup(client: commands.Bot):
    client.add_cog(Controlling(client))