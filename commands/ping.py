from discord.client import Client
from discord.message import Message


async def execute(msg: Message, client: Client):
    await msg.reply("pong")