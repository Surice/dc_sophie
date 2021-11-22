import discord

from discord.ext import commands
from cogs.utils.checks import embed_perms, get_user

class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(brief='Kickt den User')
    async def kick(self, ctx, user: discord.Member, *, reason=""):
        message = ""
        try:
            await user.kick(reason=reason)
            msg = f"{user.mention} wurde vom Server gekickt"
            if reason:
                msg += f"\nGrund: `{reason}`"
            embed = discord.Embed(description=msg, color=0x4FA87E)
            message = msg
        except discord.Forbidden:
            embed = discord.Embed(description="Keine Berechtigung um User zu kicken", color=0xED4245)
            message = "Keine Berechtigung um User zu kicken"
        except discord.NotFound:
            embed = discord.Embed(description="User nicht gefunden", color=0xED4245)
            message = "User nicht gefunden"
        if embed_perms(ctx.message):
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            await ctx.message.reply("> " + message, mention_author=False)
    
    @commands.command(brief='Bannt den User')
    async def ban(self, ctx, user: discord.User, *, reason=""):
        message = ""
        try:
            await ctx.guild.ban(discord.Object(id=user.id), reason=reason)
            msg = f"{user.mention} wurde vom Server gebannt"
            if reason:
                msg += f"\nGrund: `{reason}`"
            embed = discord.Embed(description=msg, color=0x4FA87E)
            message = msg
        except discord.Forbidden:
            embed = discord.Embed(description="Keine Berechtigung um User zu bannen", color=0xED4245)
            message = "Keine Berechtigung um User zu bannen"
        except discord.NotFound:
            embed = discord.Embed(description="User nicht gefunden", color=0xED4245)
            message = "User nicht gefunden"
        if embed_perms(ctx.message):
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            await ctx.message.reply("> " + message, mention_author=False)
    
    @commands.command(brief='Entbannt den User')
    async def unban(self, ctx, user: discord.User):
        message = ""
        try:
            user = await self.bot.fetch_user(user.id)
            await ctx.guild.unban(user)
            embed = discord.Embed(description=f"{user.mention} wurde entbannt", color=0x4FA87E)
            message = f"{user.mention} wurde entbannt"
        except discord.Forbidden:
            embed = discord.Embed(description="Keine Berechtigung um User zu entbannen", color=0xED4245)
            message = "Keine Berechtigung um User zu entbannen"
        except discord.NotFound:
            try:
                embed = discord.Embed(description=f"{user.mention} ist nicht gebannt", color=0xED4245)
                message = f"{user.mention} ist nicht gebannt"
            except: 
                embed = discord.Embed(description="User nicht gefunden", color=0xED4245)
                message = "User nicht gefunden"
        if embed_perms(ctx.message):
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            await ctx.message.reply("> " + message, mention_author=False)
    
    @commands.command(aliases=['sban'], brief='Softbannt den User')
    async def softban(self, ctx, user, *, reason=""):
        message = ""
        user = user.replace("<", "").replace(">", "").replace("!", "").replace("@", "")
        try:
            user = get_user(ctx.message, user) or await self.bot.fetch_user(user)
            await user.ban(reason=reason)
            await ctx.guild.unban(user)
            msg = f"{user.mention} wurde vom Server gebannt und wieder entbannt"
            if reason:
                msg += f"\nGrund: `{reason}`"
            embed = discord.Embed(description=msg, color=0x4FA87E)
            message = msg
        except discord.Forbidden:
            embed = discord.Embed(description="Keine Berechtigung um User zu bannen", color=0xED4245)
            message = "Keine Berechtigung um User zu bannen"
        except discord.NotFound:
            embed = discord.Embed(description="User nicht gefunden", color=0xED4245)
            message = "User nicht gefunden"
        except:
            embed = discord.Embed(description=f"{user.mention} ist nicht auf dem Server", color=0xED4245)
            message = f"{user.mention} ist nicht auf dem Server"
        if embed_perms(ctx.message):
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            await ctx.message.reply("> " + message, mention_author=False)
    
    @commands.command(brief='Löscht die letzen X Nachrichten')
    async def purge(self, ctx, limit: int):
        try:
            await ctx.message.delete()
            await ctx.channel.purge(limit=limit)
        except discord.Forbidden:
            embed = discord.Embed(description="Keine Berechtigung um Nachrichten zu löschen", color=0xED4245)
            if embed_perms(ctx.message):
                await ctx.message.reply(embed=embed, mention_author=False)
            else:
                await ctx.message.reply("> Keine Berechtigung um Nachrichten zu löschen", mention_author=False)

def setup(bot: commands.Bot):
    bot.add_cog(Mod(bot))