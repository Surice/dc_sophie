import discord
import aiohttp

def embed_perms(message):
    try:
        check = message.author.permissions_in(message.channel).embed_links
    except:
        check = True
    return check

def attach_perms(message):
    return message.author.permissions_in(message.channel).attach_files

def get_user(message, user):
    member = None
    try:
        member = message.mentions[0]
    except:
        if str(message.channel.type) == "text": # Guild
            member = discord.utils.find(lambda m: m.name == user, message.channel.guild.members)
        elif str(message.channel.type) == "private": # DM Channel
            if user == message.channel.recipient.name:
                member = message.channel.recipient
        elif str(message.channel.type) == "group": # Group
            member = discord.utils.find(lambda m: m.name == user, message.channel.recipients)       
    if not member:
        try:
            if str(message.channel.type) == "text": # Guild
                member = message.guild.get_member(int(user))
            elif str(message.channel.type) == "private": # DM Channel
                if int(user) == message.channel.recipient.id:
                    member = message.channel.recipient
            elif str(message.channel.type) == "group": # Group
                member = discord.utils.find(lambda m: m.id == int(user), message.channel.recipients)
        except ValueError:
            pass
    if not member:
        return None
    return member

def get_guild(self, param):
    guild = None
    try:
        guild = discord.utils.find(lambda g: g.name == param, self.bot.guilds)
    except:
        try:
            guild = self.bot.get_guild(int(param))
        except ValueError:
            pass
    if not guild:
        return None
    return guild

def find_channel(channel_list, text):
    if text.isdigit():
        found_channel = discord.utils.get(channel_list, id=int(text))
    elif text.startswith("<#") and text.endswith(">"):
        found_channel = discord.utils.get(channel_list, id=text.replace("<", "").replace(">", "").replace("#", ""))
    else:
        found_channel = discord.utils.get(channel_list, name=text)
    return found_channel

async def hastebin(content, session=None):
    if not session:
        session = aiohttp.ClientSession()
    async with session.post("https://hastebin.com/documents", data=content.encode('utf-8')) as resp:
        if resp.status == 200:
            result = await resp.json()
            return "https://hastebin.com/" + result["key"]
        else:
            return "Error with creating Hastebin. Status: %s" % resp.status