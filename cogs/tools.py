import discord
import time
import os
import string
import random
from discord import message

from discord.ext import commands
from math import sqrt


class Tools(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(brief='Startet den Selfbot neu')
    async def restart(self, ctx, delay: int = 5):
        await ctx.message.reply(f"> Bot wird in {delay} Sekunden neugestartet", mention_author=False)
        time.sleep(delay)
        await self.bot.change_presence(status=discord.Status.invisible)
        os.popen("sudo -S %s" % ("service selfbot restart"), 'w').write('PASSWORD')

    def is_me(self, m):
        return m.author == self.bot.user

    @commands.command(aliases=['del', 'd'], brief='Löscht deine letze Nachricht')
    async def delete(self, ctx, limit: int = None):
        if limit == None:
            await self.bot.lastmsg.delete()
            await ctx.message.delete()
        else:
            await ctx.message.delete()
            try:
                await ctx.channel.purge(limit=limit, check=self.is_me)
            except:
                try:
                    async for message in ctx.channel.history(limit=limit):
                        if message.author == self.bot.user:
                            await message.delete()
                except:
                    await ctx.message.reply("> Kann die Nachrichten nicht löschen", mention_author=False)

    @commands.command(brief='Spammt den Chat')
    async def spam(self, ctx, limit: int, *, text=None):
        message = ctx.message
        await ctx.message.delete()
        if text == None:
            for _ in range(limit):
                txt = "".join(random.choices(
                    string.ascii_uppercase + string.digits, k=random.randrange(12, 24)))
                if message.reference is not None:
                    await message.reference.reply(txt)
                else:
                    await message.channel.send(txt)
        else:
            for _ in range(limit):
                if message.reference is not None:
                    await message.reference.reply(text)
                else:
                    await message.channel.send(text)

    @commands.command(aliases=['nick'], brief='Ändert deinen Nickname')
    async def nickname(self, ctx, *, txt=None):
        try:
            await ctx.message.author.edit(nick=txt)
            await ctx.message.reply("> Nickname aktualisiert", mention_author=False)
        except discord.Forbidden:
            await ctx.message.reply("> Du kannst deinen Nickname nicht ändern", mention_author=False)

    @commands.command(brief='Markiert Server als gelesen')
    async def read(self, ctx, id: int = None):
        if id == None:
            for guild in self.bot.guilds:
                await guild.ack()
            await ctx.message.reply("> Alle Server als gelesen markiert", mention_author=False)
        else:
            guild = self.bot.get_guild(id)
            if guild:
                await guild.ack()
                await ctx.message.reply(f"> {guild.name} als gelesen markiert", mention_author=False)
            else:
                await ctx.message.reply("> Server nicht gefunden", mention_author=False)

    @commands.command()
    async def calc(self, ctx, *, msg):
        """Simple calculator. Ex: calc 2+2"""
        equation = msg.strip().replace('^', '**').replace('x', '*')
        try:
            if '=' in equation:
                left = eval(equation.split('=')[0], {
                            "__builtins__": None}, {"sqrt": sqrt})
                right = eval(equation.split('=')[1], {
                             "__builtins__": None}, {"sqrt": sqrt})
                answer = str(left == right)
            else:
                answer = str(
                    eval(equation, {"__builtins__": None}, {"sqrt": sqrt}))
        except TypeError:
            await ctx.message.reply("> Ungültige Zeichen gefunden", mention_author=False)
        await ctx.message.reply(f"> {msg.replace('**', '^').replace('x', '*')} = {answer}", mention_author=False)

def setup(bot: commands.Bot):
    bot.add_cog(Tools(bot))
