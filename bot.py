print("loading imports...")

from components.config import getConfig
from discord.ext import commands

print("loading config...")
config = getConfig()

print("initializing bot")

client: commands.Bot = commands.Bot(command_prefix=config['prefix'], self_bot=True)
client.snipe_message_author = {}
client.snipe_message_content = {}


def getClient():
    return client

#for filename in os.listdir('./cogs'):
for filename in ["automation.py", "control.py", "tools.py", "feelings.py"]:
    if(not filename.endswith(".py")):
        break
    print("loading:", filename)
    client.load_extension(f'cogs.{filename[:-3]}')


client.run(config['token'])