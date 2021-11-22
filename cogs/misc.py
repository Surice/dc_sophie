from distutils.sysconfig import PREFIX
import discord
import time
import random
import platform, psutil, os, sys

from discord.ext import commands
from datetime import datetime
from pytz import timezone 
from colour import Color

from cogs.utils.checks import embed_perms, get_guild, get_user

class Miscellaneous(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(brief='Zeigt die gelöschte Nachricht an')
    async def snipe(self, ctx):
        channel = ctx.channel
        try:
            embed = discord.Embed(description = self.bot.snipe_message_content[channel.id], color=0xF04848)
            embed.set_author(name=self.bot.snipe_message_author[channel.id], icon_url=self.bot.snipe_message_author[channel.id].avatar_url)
            message = f"{self.bot.snipe_message_author[channel.id]} \n> {self.bot.snipe_message_content[channel.id]}"
            if embed_perms(ctx.message):
                await ctx.message.reply(embed=embed, mention_author=False)
            else:
                await ctx.message.reply(message, mention_author=False)
        except:
            await ctx.message.reply(f"> Es gibt keine kürzlich gelöschten Nachrichten in {channel.mention}", mention_author=False)
    
    @commands.command(brief='Zeigt die Uptime vom Bot an')
    async def uptime(self, ctx):
        timeUp = time.time() - self.bot.startTime
        hoursUp = timeUp / 3600
        minutesUp = (timeUp / 60) % 60
        secondsUp = timeUp % 60
        await ctx.message.reply("> Uptime: {0:.0f} Stunden, {1:.0f} Minuten und {2:.0f} Sekunden".format(hoursUp, minutesUp, secondsUp), mention_author=False)
    
    @commands.command(brief='Zeigt den Bot Ping an')
    async def ping(self, ctx):
        ping = ctx.message
        pong = await ctx.message.reply("> Berechne Ping", mention_author=False)
        delta = pong.created_at - ping.created_at
        delta = int(delta.total_seconds() * 1000)
        await pong.edit(content=f'> Ping: {delta} ms', mention_author=False, allowed_mentions=discord.AllowedMentions(replied_user=False))
    
    @commands.command(aliases=['a'], brief='Sendet den Avatar Link vom User')
    async def avatar(self, ctx, args = None):
        user = get_user(ctx.message, args)
        if user == None:
            await ctx.message.reply(f"> {self.bot.user.avatar_url}", mention_author=False)
        else:
            await ctx.message.reply(f"> {user.avatar_url}", mention_author=False)
    
    @commands.command(aliases=['whois', "look"], brief='Zeigt Infos über User oder Server')
    async def lookup(self, ctx, element, *, query = None):
        if element == "user" or element == "guild":
            if element == "user":
                user = get_user(ctx.message, query) if query is not None else self.bot.user
                message = ""
                try:
                    user = await self.bot.fetch_user(user.id)
                    profile = await user.profile()
                    createdTimestamp = f"<t:{int(datetime.timestamp(user.created_at.astimezone(timezone('Europe/Berlin'))))}>"
                    descr = f"Name: {user.mention or 'Unknown'}\nID: {user.id or 'Unknown'}\nErstellt am: {createdTimestamp}"
                    if profile.premium:
                        nitroTimestamp = f"<t:{int(datetime.timestamp(profile.premium_since.astimezone(timezone('Europe/Berlin'))))}>"
                        descr += f"\nNitro seit: {nitroTimestamp}"
                    embed = discord.Embed(description=descr)
                    embed.set_author(name=user, icon_url=user.avatar_url)
                    embed.set_thumbnail(url=user.avatar_url)
                    message = f"{user}\n{descr}"

                    connections = profile.connected_accounts
                    if not str(connections) == "[]":
                        socials = ""
                        for x in range(len(connections)):
                            current = connections[x]
                            if current["type"] == "github":
                                socials += f"<:github:887614116892651550> [{current['name']}](https://github.com/{current['name']})\n"
                            if current["type"] == "reddit":
                                socials += f"<:reddit:887614117081403422> [{current['name']}](https://www.reddit.com/user/{current['name']})\n"
                            if current["type"] == "spotify":
                                socials += f"<:spotify:887614116628398081> [{current['name']}](https://open.spotify.com/user/{current['id']})\n"
                            if current["type"] == "steam":
                                socials += f"<:steam:887614116980740147> [{current['name']}](https://steamcommunity.com/profiles/{current['id']})\n"
                            if current["type"] == "twitch":
                                socials += f"<:twitch:887614117098168380> [{current['name']}](https://twitch.tv/{current['name']})\n"
                            if current["type"] == "youtube":
                                socials += f"<:youtube:887614116980748328> [{current['name']}](https://youtube.com/channel/{current['id']})\n"
                            if current["type"] == "twitter":
                                socials += f"<:twitter:887614116829724693> [{current['name']}](https://twitter.com/{current['name']})\n"
                            if current["type"] == "facebook":
                                socials += f"<:facebook:887614116771008522> [{current['name']}](https://www.facebook.com/{current['id']})\n"
                            if current["type"] == "xbox":
                                socials += f"<:xbox:887614117421137942> {current['name']}\n"
                            if current["type"] == "battlenet":
                                socials += f"<:battlenet:887614116888477716> {current['name']}\n"
                            if current["type"] == "leagueoflegends":
                                socials += f"<:lol:887614117161086976> {current['name']}\n"
                        embed.add_field(name="Socials", value=socials)
                        
                    badges = ""
                    if user.public_flags.staff:
                        badges += "<:staff:887614042150162432> "
                    # if user.public_flags.discord_certified_moderator:
                    #     badges += "<:moderator:887614041936244746> "
                    if user.public_flags.partner:
                        badges += "<:partner:887614042456350730> "
                    if user.public_flags.hypesquad:
                        badges += "<:hypesquad_events:887614042057900042> "
                    if user.public_flags.hypesquad_bravery:
                        badges += "<:hypesquad_bravery:887614041667813377> "
                    if user.public_flags.hypesquad_brilliance:
                        badges += "<:hypesquad_brilliance:887614042070474752> "
                    if user.public_flags.hypesquad_balance:
                        badges += "<:hypesquad_balance:887614041831374888> "
                    if user.public_flags.bug_hunter:
                        badges += "<:bug_hunter:887614041453916160> "
                    if user.public_flags.bug_hunter_level_2:
                        badges += "<:bug_hunter_gold:887614041676214283> "
                    if user.public_flags.verified_bot_developer:
                        badges += "<:verified_developer:887614042980630578> "
                    if user.public_flags.early_supporter:
                        badges += "<:early_supporter:887614041646837791> "
                    if profile.premium:
                        badges += "<:nitro:887614042217263114> "
                    if not badges == "": 
                        embed.add_field(name="Badges", value=badges)

                    if embed_perms(ctx.message):
                        await ctx.message.reply(embed=embed, mention_author=False)
                    else:
                        await ctx.message.reply(message.replace('\n', '\n> '), mention_author=False, allowed_mentions=discord.AllowedMentions(users=False))
                except:
                    await ctx.message.reply("> User nicht gefunden", mention_author=False)
                
            elif element == "guild":
                guild = get_guild(self, query) if query is not None else ctx.guild
                message = ""
                try:
                    owner = await self.bot.fetch_user(guild.owner_id)
                    createdTimestamp = f"<t:{int(datetime.timestamp(guild.created_at.astimezone(timezone('Europe/Berlin'))))}>"
                    desc = f"Server Owner: {owner.mention or 'Unknown'}\nErstellt am: {createdTimestamp}\nRegion: {guild.region  or 'Unknown'}\nSprache: {guild.preferred_locale  or 'Unknown'}"
                    embed = discord.Embed(description=desc)
                    embed.set_author(name=guild, icon_url=guild.icon_url)
                    embed.set_thumbnail(url=guild.icon_url)
                    message = f"{guild}\n{desc}"

                    if guild.description:
                        embed.add_field(name="Beschreibung", value=guild.description, inline=False)
                        message += f"\nBeschreibung:\n{guild.description}"

                    if 'VANITY_URL' in guild.features:
                        embed.add_field(name="Vanity Url", value=await guild.vanity_invite())
                        message += f"\nVanity Url: {await guild.vanity_invite()}"

                    embed.add_field(name="Verification Level", value=guild.verification_level)
                    message += f"\nVerification Level: {guild.verification_level}"

                    embed.add_field(name="Explicit Content Filter", value=guild.explicit_content_filter)
                    message += f"\nExplicit Content Filter: {guild.explicit_content_filter}"

                    embed.add_field(name="Server Boost Level", value=f"Level {guild.premium_tier}")
                    message += f"\nServer Boost Level: Level {guild.premium_tier}"

                    embed.add_field(name="Server Booster", value=f"{guild.premium_subscription_count} Booster")
                    message += f"\nServer Booster: {guild.premium_subscription_count} Booster"

                    if guild.features:
                        embed.add_field(name="Features", value=", ".join(guild.features), inline=False)
                        message += "\nFeatures:\n" + ", ".join(guild.features)

                    if embed_perms(ctx.message):
                        await ctx.message.reply(embed=embed, mention_author=False)
                    else:
                        await ctx.message.reply(message.replace('\n', '\n> '), mention_author=False, allowed_mentions=discord.AllowedMentions(users=False))
                except:
                    await ctx.message.reply("> Server nicht gefunden", mention_author=False)
        else:
            await ctx.message.reply("> Falsche Syntax. Nutze {PREFIX}whois <user|guild> [User/Guild]", mention_author=False)
    
    @commands.command(aliases=['colour'])
    async def color(self, ctx, *, colour: str = None):
        """Convert Color from HEX to RGB or simply search for webcolors."""
        msg = ctx.message
        try:
            if colour is None:
                roleColor = msg.author.top_role.color
                color = Color(str(roleColor))
            else:
                color = Color(colour)
        except:
            color = None
        if color:
            value = color.hex_l.strip('#')
            rgb = tuple(int(value[i:i + len(value) // 3], 16) for i in range(0, len(value), len(value) // 3))
            e = discord.Embed(title=color.web.title(), colour=int((value), 16))
            e.url = f'http://www.colorhexa.com/{value}'
            e.add_field(name='HEX', value=color.hex_l, inline=False)
            e.add_field(name='RGB', value=rgb, inline=False)
            e.set_thumbnail(url=f'http://www.colorhexa.com/{value}.png')

            message = f"{color.web.title()}\n"
            if embed_perms(ctx.message):
                await ctx.message.reply(embed=e, mention_author=False)
            else:
                await ctx.message.reply(message.replace('\n', '\n> '), mention_author=False)
        else:
            await ctx.message.reply("> Farbe nicht gefunden", mention_author=False)
    
    @commands.command(brief='Zeigt Infos zum Prozess an')
    async def sysinfo(self, ctx):
        prosys = psutil.cpu_percent()
        process = psutil.Process(os.getpid())
        memory_usage = psutil.virtual_memory().used / 1024**2
        avai = psutil.virtual_memory().total / 1024**2
        if os.name == 'nt':
            system = '%s %s (%s)' % (platform.system(), platform.version(), sys.platform)
        else:
            syst = '%s %s' % (platform.linux_distribution(full_distribution_name=1)[0].title(), platform.linux_distribution(full_distribution_name=1)[1])
            system = f"{platform.system()}, {', '.join(map(str, (syst, platform.release())))}"
        
        cpu = '{:.2f}%'.format(prosys)
        bot_cpu = '{:.2f}%'.format(process.cpu_percent(interval=0.1) / psutil.cpu_count())
        memory = '{:.2f} MiB / {:.2f} MiB ({:.2f}%)'.format(memory_usage, avai, psutil.virtual_memory()[2])
        bot_memory = '{:.2f} MiB ({:.2f}%)'.format(process.memory_info().rss / 1024 ** 2, process.memory_percent())

        embed = discord.Embed(title='System Info', description=f"System: {system}\nCPU: {cpu}\nBot CPU Usage: {bot_cpu}\nMemory: {memory}\nBot Memory Usage: {bot_memory}")
        if embed_perms(ctx.message):
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            await ctx.message.reply(f"> System: {system}\nCPU: {cpu}\nBot CPU Usage: {bot_cpu}\nMemory: {memory}\nBot Memory Usage: {bot_memory}".replace('\n', '\n> '), mention_author=False)
    
    @commands.command(aliases=['e'], brief='Editiert deine letze Nachricht')
    async def edit(self, ctx, *, text):
        replacements = {
                "shrug": "\xaf\_(\u30c4)_/\xaf",
                "lenny": "( \u0361\u00b0 \u035c\u0296 \u0361\u00b0)",
                "tableflip": "(\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b",
                "unflip": "\u252c\u2500\u252c\ufeff \u30ce( \u309c-\u309c\u30ce)",
                "time": time.strftime("%H:%M:%S"),
                "date": time.strftime("%d. %B %Y"),
                "timestamp": time.strftime("%d. %B %Y at %H:%M:%S"),
                "year": time.strftime("%Y"),
                "month": time.strftime("%B"),
                "mon": time.strftime("%b"),
                "weekday": time.strftime("%A"),
                "wday": time.strftime("%a"),
                "day": time.strftime("%d"),
                "timezone": time.strftime("%Z")
                }
        for key, val in replacements.items():
            text = text.replace("{"+key+"}", val)
        text = text.replace('@me', self.bot.user.mention)

        content = text.replace(self.bot.http.token, "Not my Token")
        if text != self.bot.lastmsg.content:
            await self.bot.lastmsg.edit(content=content)
        await ctx.message.delete()
    
    @commands.command(brief='Schlägt einen User')
    async def slap(self, ctx, user: discord.User):
        embed = discord.Embed(description=f"{self.bot.user.mention} hat {user.mention} geschlagen")
        if embed_perms(ctx.message):
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            await ctx.message.reply(f"> {self.bot.user.mention} hat {user.mention} geschlagen".replace('\n', '\n> '), mention_author=False)
    
    @commands.command(brief='Umarmt einen User')
    async def hug(self, ctx, user: discord.User):
        embed = discord.Embed(description=f"{self.bot.user.mention} hat {user.mention} umarmt c:")
        if embed_perms(ctx.message):
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            await ctx.message.reply(f"> {self.bot.user.mention} hat {user.mention} umarmt c:".replace('\n', '\n> '), mention_author=False)
    
    @commands.command(brief='Hat einen User ganz dolle lieb')
    async def love(self, ctx, user: discord.User):
        embed = discord.Embed(description=f"{self.bot.user.mention} hat {user.mention} ganz dolle lieb ❤️")
        if embed_perms(ctx.message):
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            await ctx.message.reply(f"> {self.bot.user.mention} hat {user.mention} ganz dolle lieb ❤️".replace('\n', '\n> '), mention_author=False)
    
    @commands.command(brief='Erlaubt es Leute zu markieren ohne sie zu pingen')
    async def fakeping(self, ctx, *, msg: str):
        await ctx.message.edit(content=msg, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
    
    @commands.command(brief='Sendet einen Ghostping mit Text')
    async def ghostping(self, ctx, hidden, *, msg: str = ""):
        msg = f"{msg}||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| _ _ _ _ {hidden}"
        await ctx.message.edit(content=f'{msg}')

def setup(bot: commands.Bot):
    bot.add_cog(Miscellaneous(bot))