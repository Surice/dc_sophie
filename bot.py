import discord
from discord.ext import commands
from json import load
import logging
import time

#logging.basicConfig(level=logging.INFO)

with open('config.json') as f:
    conf = load(f)
    token = conf["token"]
    status = conf["status"]
    twitch = conf["twitch-url"]

async def getPrefix(bot, msg):
    with open('config.json') as f:
        conf = load(f)
        prefix = conf["prefix"]
    return prefix

bot = commands.Bot(command_prefix=getPrefix, self_bot=True, status=discord.Status.offline, afk=True)
bot.startTime = time.time()
bot.status = discord.Status.online if status == "online" else discord.Status.idle if status == "idle" else discord.Status.dnd if status == "dnd" else discord.Status.offline
bot.activity = None
bot.twitch = twitch
bot.snipe_messge_author = {}
bot.snipe_message_content = {}
bot.lastmsg = None

for cog in ["cogs.utils.events", "cogs.debugger", "cogs.google", "cogs.misc", "cogs.mod", "cogs.nitrosniper", "cogs.setup", "cogs.tools"]:
    bot.load_extension(cog)

bot.run(token)