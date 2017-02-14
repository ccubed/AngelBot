import aiohttp
from discord import embeds

class OWAPI:
    def __init__(self, client):
        self.apiurl = "https://owapi.net/api/v3/u/"
        self.commands = [['ow', self.ow], ['owheroes', self.owheroes]]
        self.header = {'User-Agent': "AngelBot AioHttp Python3.5"}
        self.bot = client

    async def ow(self, message):
        name = " ".join(message.content.split(" ")[1:]).replace('#', '-')
        with aiohttp.ClientSession() as session:
            async with session.get(self.apiurl + "{}/stats".format(name), headers=self.header) as response:
                if response.status == 404:
                    return "Battletag not found."
                elif response.status == 500:
                    return "Server under heavy load. Please try again later."
                else:
                    jsd = await response.json()
                    region = "us" if jsd['us'] is not None else "eu" if jsd['eu'] is not None else "kr"
                    embed = embeds.Embed(description="Overwatch Stat Summary")
                    embed.title = name.replace("-", "#")
                    if jsd[region]['stats']['quickplay']['overall_stats']['avatar']:
                        embed.set_thumbnail(url=jsd[region]['stats']['quickplay']['overall_stats']['avatar'])
                    embed.add_field(name="Rank and Level", value="**Level:** {}\n**Rank:** {}\n".format(jsd[region]['stats']['quickplay']['overall_stats']['level'], jsd[region]['stats']['quickplay']['overall_stats']['comprank'] or 0))
                    embed.add_field(name="Pain Caused", value="**{}**".format(jsd[region]['stats']['quickplay']['game_stats']['damage_done']))
                    embed.add_field(name="Sad Endings", value="**{}**".format(jsd[region]['stats']['quickplay']['game_stats']['deaths']))
                    embed.add_field(name="Eliminations", value="**{}**".format(jsd[region]['stats']['quickplay']['game_stats']['eliminations']))
                    embed.add_field(name="Killshots", value="**{}**".format(jsd[region]['stats']['quickplay']['game_stats']['final_blows']))
                    await self.bot.send_message(message.channel, embed=embed)

    async def owheroes(self, message):
        name = " ".join(message.content.split(" ")[1:]).replace('#', '-')
        with aiohttp.ClientSession() as session:
            async with session.get(self.apiurl + "{}/heroes".format(name), headers=self.header) as response:
                if response.status == 404:
                    await self.bot.send_message(message.channel, "Battletag not found.")
                elif response.status == 500:
                    await self.bot.send_message(message.channel, "Server under heavy load. Please try again later.")
                else:
                    jsd = await response.json()
                    region = "us" if jsd['us'] is not None else "eu" if jsd['eu'] is not None else "kr"
                    embed = embeds.Embed(description="Hero Playtime Summary")
                    embed.title = name.replace("-", "#")
                    for hero in [x for x in jsd[region]['heroes']['playtime']['quickplay'] if jsd[region]['heroes']['playtime']['quickplay'][x] > 0]:
                        embed.add_field(name=hero, value=round(jsd[region]['heroes']['playtime']['quickplay'][hero], 2))
                    await self.bot.send_message(message.channel, embed=embed)
