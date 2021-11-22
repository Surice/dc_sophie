from components.commandhandling import commandHandling
from components.nitrosniper import nitroSniper
import discord




async def onMessage(msg: discord.Message, config, client):
    nitroSniper(msg.content, config)

    if(msg.content.startswith(config['prefix']) and msg.author.id == client.user.id):
        await commandHandling(msg, client)