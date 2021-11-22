import re, requests

def nitroSniper(content, config):
    if 'discord.gift/' in content or 'discord.com/gifts/' in content or 'discordapp.com/gifts/' in content:
            if "discord.gift/" in content:
                code = re.findall("discord[.]gift/(\w+)", content)
            if "discordapp.com/gifts/" in content:
                code = re.findall("discordapp[.]com/gifts/(\w+)", content)
            if 'discord.com/gifts/' in content:
                code = re.findall("discord[.]com/gifts/(\w+)", content)

            for code in code:
                requests.post(f'https://discordapp.com/api/v9/entitlements/gift-codes/{code}/redeem', headers={'Authorization': config['token']})