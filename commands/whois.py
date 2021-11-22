from discord.client import Client
from discord.message import Message


async def execute(msg: Message, client: Client):
    user = await client.fetch_user(msg.content.split(' ')[1])
    await msg.reply(user)