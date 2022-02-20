from math import fabs
from components.convert import fetchUser, pretRes
from components.config import getConfig
import discord
from discord import mentions
from discord.ext import commands
from datetime import datetime
from pytz import timezone
from discord.ext.commands import context

from discord.ext.commands.core import command


class Tools(commands.Cog):
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.config = getConfig()

    @commands.command(aliases=[])
    async def ping(self, msg: commands.Context):
        ping = msg.message
        pong = await msg.message.reply("> checking...")
        delta = pong.created_at - ping.created_at
        delta = int(delta.total_seconds() * 1000)
        await pong.edit(content=f'> Ping: {delta} ms')

    @commands.command(aliases=["whois", "ui", "user"])
    async def userinfo(self, msg: commands.Context, user: discord.User or str = None):
        user: discord.User = await fetchUser(self.client, user)
        message = f"**Tag:** {user} \n**Mention:** <@{user.id}> \n**ID:** {user.id} \n**Avatar:** {user.avatar_url_as(format='gif')}\n\n"


        createdTimestamp = f"<t:{int(datetime.timestamp(user.created_at.astimezone(timezone('Europe/Berlin'))))}>"
        message += f"**Created at:** {createdTimestamp}\n";

        if(msg.guild != None):
            member: discord.Member = await msg.guild.fetch_member(user.id)
            joinedTimestamp = f"<t:{int(datetime.timestamp(member.joined_at.astimezone(timezone('Europe/Berlin'))))}>"
            message += f"**Joined at:** {joinedTimestamp}\n";
            
        
        profile = await user.profile()
        if profile.premium:
            nitroTimestamp = f"<t:{int(datetime.timestamp(profile.premium_since.astimezone(timezone('Europe/Berlin'))))}>"
            message += f"**Nitro since:** {nitroTimestamp}\n";


        message += "\n";
        connections = profile.connected_accounts
        if not str(connections) == "[]":
            socials = ""
            for x in range(len(connections)):
                current = connections[x]
                if current["type"] == "github":
                    socials += f"https://github.com/{current['name']}, "
                if current["type"] == "reddit":
                    socials += f"https://www.reddit.com/user/{current['name']}, "
                if current["type"] == "spotify":
                    socials += f"https://open.spotify.com/user/{current['id']}, "
                if current["type"] == "steam":
                    socials += f"https://steamcommunity.com/profiles/{current['id']}, "
                if current["type"] == "twitch":
                    socials += f"https://twitch.tv/{current['name']}, "
                if current["type"] == "youtube":
                    socials += f"https://youtube.com/channel/{current['id']}, "
                if current["type"] == "twitter":
                    socials += f"https://twitter.com/{current['name']}, "
                if current["type"] == "facebook":
                    socials += f"https://www.facebook.com/{current['id']}, "
                if current["type"] == "xbox":
                    socials += f"{current['name']}, "
                if current["type"] == "battlenet":
                    socials += f"{current['name']}, "
                if current["type"] == "leagueoflegends":
                    socials += f"{current['name']}"
                
            message += f"**Connections:** {socials}\n";
            
            
        badges = ""
        if user.public_flags.staff:
            badges += "<Staff, "
        # if user.public_flags.:
        #      badges += "Moderator, "
        if user.public_flags.partner:
            badges += "Partner "
        if user.public_flags.hypesquad:
            badges += "Hypesquad_events, "
        if user.public_flags.hypesquad_bravery:
            badges += "Hypesquad_bravery, "
        if user.public_flags.hypesquad_brilliance:
            badges += "Hypesquad_brilliance, "
        if user.public_flags.hypesquad_balance:
            badges += "Hypesquad_balance, "
        if user.public_flags.bug_hunter:
            badges += "Bug_hunter, "
        if user.public_flags.bug_hunter_level_2:
            badges += "Bug_hunter_gold, "
        if user.public_flags.verified_bot_developer:
            badges += "Verified_developer, "
        if user.public_flags.early_supporter:
            badges += "Early_supporter, "
        if profile.premium:
            badges += "Nitro, "
        if not badges == "":
            message += f"**Badges:** {badges}"
            

        await msg.reply(content=message);

    @commands.command(aliases=["pb"])
    async def avatar(self, msg: commands.Context, user: discord.User or str = None):
        user = await fetchUser(self.client, user)

        await msg.reply(user.avatar_url)
                


    @commands.command(aliases=["perms"])
    async def permissions(self, msg: commands.Context, user: discord.User or str = None):
        user = await fetchUser(self.client, user)
        member: discord.Member = await msg.guild.fetch_member(user.id)
        userpermissions = ""

        for permission in member.guild_permissions:
            if(permission[1] == True):
                userpermissions += f"{permission[0]}, "

        await pretRes(msg, userpermissions, 0x00FF00)


    @commands.command(aliases=["guild", "gi"])
    async def guildinfo(self, msg: commands.Context, guild: discord.Guild or str = None):
        if(guild == None):
            guild = msg.guild

        else:
            try:
                guild = await self.client.fetch_guild(guild)
            except:
                guild = guild

        try:
            guildBans = len(await guild.bans())
        except:
            guildBans = "Unknown"

        if(guild.mfa_level == 1):
            guildMfa = "Active"
        else:
            guildMfa = "Disabled"

        GuildIconFormat = 'png';
        if(guild.is_icon_animated()):
            GuildIconFormat = 'gif';

        message = f"**Name:** {guild.name} \n**ID:** {guild.id} \n**Owner:** <@{guild.owner_id}> ({guild.owner}) \n**Icon:** {guild.icon_url_as(format=GuildIconFormat, size=1024)}  \n**Banner:** {guild.banner_url_as(format='png', size=1024)}\n**Description:** `{guild.description}`\n";

        guildCreatedAt = f"<t:{int(datetime.timestamp(guild.created_at.astimezone(timezone('Europe/Berlin'))))}>";
        message += f"**Created at:** {guildCreatedAt} \n\n";

        message += f"**Member:** Total: {guild.member_count} \nBanned: {guildBans} \n**Security:** Mfa: {guildMfa} \nVerfication: {guild.verification_level} \nFilter: {guild.explicit_content_filter} \n**Boosting:** Boost Tier: {guild.premium_tier} \nBooster: {len(guild.premium_subscribers)} \n**Statistics:** Text Channel: {len(guild.text_channels)} \nVoice Channel: {len(guild.voice_channels)} \nCategories: {len(guild.categories)} \n Emojis: {len(guild.emojis)}";
        

        await msg.reply(content=message);


    @commands.command()
    async def snipe(self, msg: commands.Context):
        try:
            author = [self.client.snipe_message_author[msg.channel.id].id, f"{self.client.snipe_message_author[msg.channel.id].name}#{self.client.snipe_message_author[msg.channel.id].discriminator}"];
            message = f"{self.client.snipe_message_content[msg.channel.id]}";

            message = f"**<@{author[0]}> ({author[1]})** \n> {message}";
            await msg.message.reply(content=message, mention_author=False);
        except:
            await msg.message.reply(f"> Es gibt keine kürzlich gelöschten Nachrichten in {msg.channel.mention}", mention_author=False);


    @commands.command()
    async def spam(self, msg: commands.Context):
        await msg.message.delete()

        rounds = 6

        content = msg.message.content.split(' ')
        content.pop(0)
        content = ' '.join(content)

        while(rounds > 0):
            rounds = rounds -1
            await msg.channel.send(content)
        


    @commands.command(pass_context=True)
    async def debug(self, msg: commands.Context):

        await msg.reply(self.client.snipe_message_author)
        

def setup(client: commands.Bot) -> None:
    client.add_cog(Tools(client))
    