print("loading imports...")

import discord
from json import load
import time

from events.on_member_update import onMemberUpdate
from events.on_message import onMessage

print("loading config...")
def getConfig():
    with open("config.json") as configFile:
        return load(configFile)


config = getConfig()

print("initializing bot")
client = discord.Client(command_prefix=config['prefix'], self_bot=True)

def getClient():
    return client


@client.event
async def on_connect():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.do_not_disturb)

@client.event
async def on_member_update(oldState, newState):
    await onMemberUpdate(oldState, newState, client)
    
@client.event
async def on_message(msg):
    await onMessage(msg, config, client)


client.run(config['token'])