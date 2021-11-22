from discord.message import Message
import importlib

async def commandHandling(msg: Message, client):
    command = importlib.import_module("commands."+msg.content.split(' ')[0].replace(".", ""))
    await command.execute(msg, client);