import discord
import aiohttp
import requests
import random

from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from cogs.utils.checks import embed_perms

class Google(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def translate(self, ctx, to_language, *, msg):
        async with aiohttp.ClientSession().get("https://gist.githubusercontent.com/astronautlevel2/93a19379bd52b351dbc6eef269efa0bc/raw/18d55123bc85e2ef8f54e09007489ceff9b3ba51/langs.json") as resp:
            lang_codes = await resp.json(content_type='text/plain')
        real_language = False
        to_language = to_language.lower()
        for entry in lang_codes:
            if to_language in lang_codes[entry]["name"].replace(";", "").replace(",", "").lower().split():
                language = lang_codes[entry]["name"].replace(";", "").replace(",", "").split()[0]
                to_language = entry
                real_language = True
        if real_language:
            async with aiohttp.ClientSession().get("https://translate.google.com/m",
                                        params={"hl": to_language, "sl": "auto", "q": msg}) as resp:
                translate = await resp.text()
            result = str(translate).split('<div class="result-container">')[1].split("</div>")[0]
            embed = discord.Embed(color=0x4B8DF5)
            embed.set_author(name="Google Translate", icon_url="https://is5-ssl.mzstatic.com/image/thumb/Purple115/v4/dc/c5/af/dcc5afc7-a810-c5a7-d851-3556ee9573ba/logo_translate_color-0-0-1x_U007emarketing-0-0-0-6-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/492x0w.png")
            embed.add_field(name="Original", value=msg, inline=False)
            embed.add_field(name=language, value=result.replace("&amp;", "&"), inline=False)
            message = f"**Google Translate**\nOriginal:\n{msg}\n{language}:\n{result.replace('&amp;', '&')}"
            if result == msg:
                embed.add_field(name="Warnung", value="Diese Sprache wird möglicherweise nicht unterstützt")
                message += "\nWarnung:\nDiese Sprache wird möglicherweise nicht unterstützt"
            if embed_perms(ctx.message):
                await ctx.message.reply(embed=embed, mention_author=False)
            else:
                await ctx.message.reply(message.replace('\n', '\n> '), mention_author=False)
        else:
            await ctx.message.reply("> Sprache nicht gefunden", mention_author=False)
    
    @commands.command(aliases=["google"], description="Will search the internet from a given search term and return the top 5 web results")
    async def search(self, ctx, *, query):

        searchResults = []

        url = 'https://www.google.com/search?q={}&num={}'.format(query.replace(" ", "+"), 10)
        usr_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        response = requests.get(url, headers=usr_agent)
        response.raise_for_status()
        resp = response.text
        soup = BeautifulSoup(resp, "html.parser")
        results = soup.find_all('div', attrs={'class': 'g'})
        resultID = 1
        for result in results:
            link = result.find('a', href=True)
            title = result.find('h3')
            if link and title:
                url = urlparse(link['href'])
                if url.hostname is None: link['href'] = f"https://www.google.com{link['href']}"
                url = f"{url.hostname}{url.path}"
                duplicate = False
                for value in range(len(searchResults)):
                    if url in searchResults[value]["link"]:
                        duplicate = True
                if not duplicate:
                    searchResults.append({"title": title.text, "link": link['href']})
                    resultID += 1

        results = ""
        resultID = 0
        if searchResults != []:
            for result in searchResults:
                results += f"\n**{resultID+1}.** [{searchResults[resultID]['title']}]({searchResults[resultID]['link']})"
                resultID += 1
        else:
            results = "Keine Ergebnisse"

        embed=discord.Embed(title="Google Search: {}".format(query), url="https://www.google.com/search?q={}".format(query.replace(" ", "+")), description=results, color=random.choice([0x4285F4, 0xDB4437, 0xF4B400, 0x0F9D58]))
        if embed_perms(ctx.message):
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            await ctx.message.reply("Keine Rechte um Embeds zu senden".replace('\n', '\n> '), mention_author=False)

def setup(bot: commands.Bot):
    bot.add_cog(Google(bot))