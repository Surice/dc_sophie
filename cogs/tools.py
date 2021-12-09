from components.convert import fetchUser
from components.config import getConfig
import discord
from discord.ext import commands

class Tools(commands.Cog):
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.config = getConfig()

    @commands.command(aliases=[])
    async def ping(self, msg: commands.Context):
        ping = msg.message
        pong = await msg.message.reply("> checking...")
        delta = pong.created_at - ping.created_at
        delta = int(delta.total_seconds() * 1000)
        await pong.edit(content=f'> Ping: {delta} ms')

    @commands.command(aliases=["whois"])
    async def userinfo(self, msg: commands.Context, user: discord.User or str = None):
        user = await fetchUser(self.client, user)

        if(msg.author.permissions_in(msg.channel).embed_links):
            embed = discord.Embed(
                title=f"{user.display_name}#{user.discriminator}"
                )

            await msg.reply(embed=embed)
        else:
            content = f"**Name:** {user.display_name}"

            await msg.reply(content=content)

    @commands.command(aliases=["pb"])
    async def avatar(self, msg: commands.Context, user: discord.User or str = None):
        user = await fetchUser(self.client, user)

        await msg.reply(user.avatar_url)
                
            
        

    @commands.command()
    async def love(self, msg: commands.Context, user: discord.User = None):
        user = await fetchUser(self.client, user)

        perms = msg.author.permissions_in(msg.channel).embed_links
        if(perms == True):
            embed = discord.Embed(description=f"{self.client.user.mention} hat {user.mention} ganz dolle lieb ❤️", color=0xFF0000)
            await msg.reply(embed=embed)
        else:
            await msg.reply(f"> {self.client.user.mention} hat {user.mention} ganz dolle lieb ❤️".replace('\n', '\n> '), mention_author=False)

    @commands.command()
    async def arsch(self, msg: commands.Context, user: discord.User = None):
        user = await fetchUser(self.client, user)

        await msg.reply(f"{user.display_name} ist ein Arsch!")


    @commands.command(pass_context=True)
    async def debug(self, msg: commands.Context):
        msg.reply("currently not implemented")
        

def setup(client: commands.Bot) -> None:
    client.add_cog(Tools(client))
    