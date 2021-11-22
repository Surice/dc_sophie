import discord
import time, asyncio
import random

from discord.ext import commands
from cogs.utils.checks import get_user





# class mod(commands.Cog):
#     def __init__(self, bot: commands.Bot) -> None:
#         self.bot = bot
    
#     @commands.Cog.listener()
#     async def on_ready(self):
#         await self.bot.change_presence(status=self.bot.status, activity=self.bot.activity, afk=True)
#         print(f'User: {self.bot.user}')
#         print(f'discord.py Version: {discord.__version__}')

#     @commands.Cog.listener()
#     async def on_command_error(self, ctx: commands.Context, error):
#         if (isinstance(error, commands.CommandNotFound) or isinstance(error, discord.errors.NotFound) or isinstance(error, discord.NotFound)):
#             return
#         print("[ERROR]", str(error))
    
#     @commands.Cog.listener(name="on_message")
#     async def on_message(self, msg):
#         if msg.author.id == self.bot.user.id:
#             content = msg.content
#             replacements = {
#                 "shrug": "\xaf\_(\u30c4)_/\xaf",
#                 "lenny": "( \u0361\u00b0 \u035c\u0296 \u0361\u00b0)",
#                 "tableflip": "(\u256f\u00b0\u25a1\u00b0\uff09\u256f\ufe35 \u253b\u2501\u253b",
#                 "unflip": "\u252c\u2500\u252c\ufeff \u30ce( \u309c-\u309c\u30ce)",
#                 "time": time.strftime("%H:%M:%S"),
#                 "date": time.strftime("%d. %B %Y"),
#                 "timestamp": time.strftime("%d %B %Y at %H:%M:%S"),
#                 "year": time.strftime("%Y"),
#                 "month": time.strftime("%B"),
#                 "mon": time.strftime("%b"),
#                 "weekday": time.strftime("%A"),
#                 "wday": time.strftime("%a"),
#                 "day": time.strftime("%d"),
#                 "timezone": time.strftime("%Z")
#                 }
#             for key, val in replacements.items():
#                 content = content.replace("{"+key+"}", val)
#             content = content.replace('@me', self.bot.user.mention)
#             content = content.replace(self.bot.http.token, "Not my Token")
#             if content != msg.content:
#                 await msg.edit(content=content)
#                 msg.content = content
#             self.bot.lastmsg = msg
    
#     @commands.Cog.listener(name="on_message_delete")
#     async def on_message_delete(self, message):
#         self.bot.snipe_message_author[message.channel.id] = message.author
#         self.bot.snipe_message_content[message.channel.id] = message.content
#         await asyncio.sleep(300)
#         try:
#             del self.bot.snipe_message_author[message.channel.id]
#             del self.bot.snipe_message_content[message.channel.id]
#         except KeyError:
#             pass

# def setup(bot: commands.Bot):
#     bot.add_cog(mod(bot))