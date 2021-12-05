print("loading imports...")

from components.config import getConfig
import discord
import os
from discord.ext import commands

print("loading config...")
config = getConfig()

print("initializing bot")
client: commands.Bot = commands.Bot(command_prefix=config['prefix'], self_bot=True)

def getClient():
    return client

#for filename in os.listdir('./cogs'):
for filename in ["automation.py", "control.py", "tools.py"]:
    if(not filename.endswith(".py")):
        break
    print("loading:", filename)
    client.load_extension(f'cogs.{filename[:-3]}')


client.run(config['token'])