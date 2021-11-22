from cogs.utils.checks import get_user
import discord
import asyncio

from discord.ext import commands
from json import dump, load

class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(brief='Setup')
    async def setup(self, ctx, category = None, arg = None):
        with open('config.json', 'r') as f:
            data = load(f)
        if category in ["prefix", "delay", "twitch", "status"]:
            if category == "prefix":
                arg = arg or "."
                data["prefix"] = arg
                with open("config.json", "w") as f:
                    dump(data, f)
                await ctx.message.reply(f"> Neue Prefix ist `{arg}`", mention_author=False)
            if category == "twitch":
                await ctx.message.edit(suppress=True)
                arg = arg or "https://twitch.tv/twitch"
                data["twitch-url"] = arg
                self.bot.twitch = arg
                with open("config.json", "w") as f:
                    dump(data, f)
                await ctx.message.reply(f"> Neue Streaming Url ist `{arg}`", mention_author=False)
            if category == "status":
                arg = arg or "online"
                data["status"] = arg
                with open("config.json", "w") as f:
                    dump(data, f)
                await ctx.message.reply(f"> Neuer Standard Status ist `{arg}`", mention_author=False)

        else:
            embed=discord.Embed(title="Einstellungen", description=f"• `prefix` **|** Ändert die Bot Prefix. Aktuelle Prefix: `{data['prefix']}`\n• `status` **|** Ändert den Standard Status. Aktueller Standard Status: `{data['status']}`\n• `twitch` **|** Ändert die Streaming Url. Aktuelle Streaming Url: `{data['twitch-url']}`")
            await ctx.message.reply(embed=embed, mention_author=False)
    
    @commands.command(brief='Ändert deinen Status')
    async def status(self, ctx, status):
        if status in ["online", "idle", "dnd", "offline"]:
            if status == "online":
                self.bot.status = discord.Status.online
                await self.bot.change_presence(status=discord.Status.online, activity=self.bot.activity, afk=True)
            if status == "idle":
                self.bot.status = discord.Status.idle
                await self.bot.change_presence(status=discord.Status.idle, activity=self.bot.activity, afk=True)
            if status == "dnd":
                self.bot.status = discord.Status.dnd
                await self.bot.change_presence(status=discord.Status.dnd, activity=self.bot.activity, afk=True)
            if status == "offline":
                self.bot.status = discord.Status.offline
                await self.bot.change_presence(status=discord.Status.offline, activity=self.bot.activity, afk=True)

            await ctx.message.reply(f"> Status erfolgreich auf `{status}` gesetzt", mention_author=False)
        else:
            await ctx.message.reply(f"> Status nicht gefunden", mention_author=False)
    
    @commands.command(brief='Ändert deinen Activity Status')
    async def activity(self, ctx, game, *, title = None):
        if game == "clear":
            self.bot.activity = None
            await self.bot.change_presence(status=self.bot.status, activity=None, afk=True)
            await ctx.message.reply("> Aktivität entfernt", mention_author=False)
        
        elif 'game' == game or 'stream' == game or 'watch' == game or 'listening' == game or 'competing' == game:
            if not title == None:
                if game == "game":
                    self.bot.activity = discord.Activity(type=discord.ActivityType.playing, name=title)
                    await self.bot.change_presence(status=self.bot.status, activity=discord.Activity(type=discord.ActivityType.playing, name=title), afk=True)
                    await ctx.message.reply("> Aktivität auf `Playing` aktualisiert", mention_author=False)
                elif game == "stream":
                    self.bot.activity = discord.Streaming(name=title, url=self.bot.twitch)
                    await self.bot.change_presence(status=self.bot.status, activity=discord.Streaming(name=title, url=self.bot.twitch), afk=True)
                    await ctx.message.reply("> Aktivität auf `Streaming` aktualisiert", mention_author=False)
                elif game == "watch":
                    self.bot.activity = discord.Activity(type=discord.ActivityType.watching, name=title)
                    await self.bot.change_presence(status=self.bot.status, activity=discord.Activity(type=discord.ActivityType.watching, name=title), afk=True)
                    await ctx.message.reply("> Aktivität auf `Watching` aktualisiert", mention_author=False)
                elif game == "listening":
                    self.bot.activity = discord.Activity(type=discord.ActivityType.listening, name=title)
                    await self.bot.change_presence(status=self.bot.status, activity=discord.Activity(type=discord.ActivityType.listening, name=title), afk=True)
                    await ctx.message.reply("> Aktivität auf `Listening` aktualisiert", mention_author=False)
                elif game == "competing":
                    self.bot.activity = discord.Activity(type=discord.ActivityType.competing, name=title)
                    await self.bot.change_presence(status=self.bot.status, activity=discord.Activity(type=discord.ActivityType.competing, name=title), afk=True)
                    await ctx.message.reply("> Aktivität auf `Competing` aktualisiert", mention_author=False)
        else:
            await ctx.message.reply(f"> Aktivität `{game}` existiert nicht", mention_author=False)

    @commands.command(aliases=['kill'], brief='Beendet den Bot')
    async def quit(self, ctx):
        message = "> Bot beenden?"
        msg = await ctx.message.reply(message.replace('\n', '\n> '), mention_author=False)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        
        def check(reaction, user):
            return user == ctx.message.author

        try:
            reaction = await self.bot.wait_for('reaction_remove', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await msg.edit(content="> Zeit abgelaufen. Bot wird nicht beendet", allowed_mentions=discord.AllowedMentions(replied_user=False))
            await msg.remove_reaction("✅", self.bot.user)
            await msg.remove_reaction("❌", self.bot.user)
        else:
            if str(reaction.emoji) == '✅':
                await msg.edit(content="> Bot wird beendet", allowed_mentions=discord.AllowedMentions(replied_user=False))
                await msg.remove_reaction("❌", self.bot.user)
                await self.bot.close()
            if str(reaction.emoji) == '❌':
                await msg.edit(content="> Bot wird nicht beendet", allowed_mentions=discord.AllowedMentions(replied_user=False))
                await msg.remove_reaction("✅", self.bot.user)
            
def setup(bot: commands.Bot):
    bot.add_cog(Setup(bot))