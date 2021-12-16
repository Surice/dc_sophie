from os import name
from components.convert import fetchUser, pretRes
from components.config import getConfig
import discord
from discord.ext import commands
from datetime import datetime
from pytz import timezone


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

    @commands.command(aliases=["whois", "ui"])
    async def userinfo(self, msg: commands.Context, user: discord.User or str = None):
        user: discord.User = await fetchUser(self.client, user)

        profile = await user.profile()
        createdTimestamp = f"<t:{int(datetime.timestamp(user.created_at.astimezone(timezone('Europe/Berlin'))))}>"
        descr = f"Name: {user.mention or 'Unknown'} \nID: {user.id or 'Unknown'} \nCreated at: {createdTimestamp} \n"

        if(msg.guild != None):
            member: discord.Member = await msg.guild.fetch_member(user.id)
            joinedTimestamp = f"<t:{int(datetime.timestamp(member.joined_at.astimezone(timezone('Europe/Berlin'))))}> \n"
            descr += f"Joined at: {joinedTimestamp}"
        

        if profile.premium:
            nitroTimestamp = f"<t:{int(datetime.timestamp(profile.premium_since.astimezone(timezone('Europe/Berlin'))))}>"
            descr += f"Nitro since: {nitroTimestamp}"

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
                    socials += f"[Github](https://github.com/{current['name']})\n"
                if current["type"] == "reddit":
                    socials += f"[Reddit](https://www.reddit.com/user/{current['name']})\n"
                if current["type"] == "spotify":
                    socials += f"[Spotify](https://open.spotify.com/user/{current['id']})\n"
                if current["type"] == "steam":
                    socials += f"[Steam](https://steamcommunity.com/profiles/{current['id']})\n"
                if current["type"] == "twitch":
                    socials += f"[Twitch](https://twitch.tv/{current['name']})\n"
                if current["type"] == "youtube":
                    socials += f"[Youtube](https://youtube.com/channel/{current['id']})\n"
                if current["type"] == "twitter":
                    socials += f"[Twitter](https://twitter.com/{current['name']})\n"
                if current["type"] == "facebook":
                    socials += f"[Facebook](https://www.facebook.com/{current['id']})\n"
                if current["type"] == "xbox":
                    socials += f"Xbox: {current['name']}\n"
                if current["type"] == "battlenet":
                    socials += f"Battle.net: {current['name']}\n"
                if current["type"] == "leagueoflegends":
                    socials += f"League of Legends: {current['name']}\n"
            embed.add_field(name="Connections", value=socials)
            
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
            embed.add_field(name="Badges", value=badges)


        if(msg.author.permissions_in(msg.channel).embed_links):
            await msg.reply(embed=embed)
        else:
            await msg.reply(content=message)

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

        embed = discord.Embed(description=guild.description)
        embed.set_author(
            name = guild.name,
            icon_url = guild.icon_url_as(format="gif", static_format="png", size=1024)
        )
        embed.set_thumbnail(guild.banner_url_as(format="gif", static_format="png", size=1024))
        embed.add_field(name="ID:", value=guild.id, inline=True)
        embed.add_field(name="Owner:", value=f"<@{guild.owner_id}>", inline=True)
        embed.add_field(name="Member:", value=guild.member_count)
        embed.add_field(name="Security:", value=f"Mfa: {guild.mfa_level} \nFilter: {guild.explicit_content_filter}")
        

        if(msg.author.permissions_in(msg.channel).embed_links):
            await msg.reply(embed=embed)            

    @commands.command(pass_context=True)
    async def debug(self, msg: commands.Context):

        msg.reply("currently not implemented")


        await msg.reply("currently not implemented")
        

def setup(client: commands.Bot) -> None:
    client.add_cog(Tools(client))
    