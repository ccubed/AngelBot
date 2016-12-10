import aiohttp
from discord import embeds

class OWAPI:
    def __init__(self, client):
        self.apiurl = "https://owapi.net/api/v2/u/"
        # Map Numbers to names
        self.index = {1: 'roadhog', 2: 'junkrat', 3: 'lucio', 4: 'soldier76', 5: 'zarya', 6: 'mccree', 7: 'tracer', 8: 'reaper',
                      9: 'widowmaker', 10: 'winston', 11: 'pharah', 12: 'reinhardt', 13: 'symmetra', 14: 'torbjorn', 15: 'bastion',
                      16: 'hanzo', 17: 'mercy', 18: 'zenyatta', 20: 'mei', 21: 'genji', 22: 'dva'}
        # Map names to Numbers
        self.characters = [{'names': ['roadhog', 'birdie'], 'id': 1}, {'names': ['junkrat', 'crocodile dun dee'], 'id': 2},
                           {'names': ['lucio', 'lúcio', 'drop the beats'], 'id': 3}, {'names': ['soldier: 76', 'cod', 'blops'], 'id': 4},
                           {'names': ['zarya', 'i must break you'], 'id': 5}, {'names': ['mccree', 'robo dead redemption'], 'id': 6},
                           {'names': ['tracer', 'booty', 'bootiful'], 'id': 7}, {'names': ['reaper', 'edgelord'], 'id': 8},
                           {'names': ['widowmaker', 'boo berry', 'boobs'], 'id': 9}, {'names': ['winston', 'dr zaius', 'caesar'], 'id': 10},
                           {'names': ['pharah', 'gundam wing'], 'id': 11}, {'names': ['reinhardt', 'the iron giant', 'fell off the map'], 'id': 12},
                           {'names': ['symmetra', 'chellmetra'], 'id': 13}, {'names': ['torbjorn', 'torbjörn', 'tim the turret man taylor', 'engineer'], 'id': 14},
                           {'names': ['bastion', 'git gud'], 'id': 15}, {'names': ['hanzo', 'ryuu ga teki no'], 'id': 16},
                           {'names': ['mercy', 'the medic', 'mother mercy'], 'id': 17}, {'names': ['zenyatta', 'android krillin'], 'id': 18},
                           {'names': ['mei', 'bae', 'waifu'], 'id': 20}, {'names': ['genji', 'animu'], 'id': 21},
                           {'names': ['D.Va', 'twitch streamer', 'gamer girl'], 'id': 22}]
        self.commands = [['ow', self.ow], ['owheroes', self.owheroes], ['owhero', self.owhero]]
        self.header = {'User-Agent': "AngelBot AioHttp Python3.5"}
        self.bot = client

    async def ow(self, message):
        name = " ".join(message.content.split(" ")[1:]).replace('#', '-')
        with aiohttp.ClientSession() as session:
            async with session.get(self.apiurl + "{}/stats/general".format(name), headers=self.header) as response:
                if response.status == 404:
                    return "Battletag not found."
                elif response.status == 500:
                    return "Server under heavy load. Please try again later."
                else:
                    jsd = await response.json()
                    embed = embeds.Embed(description="Overwatch Stat Summary".format(jsd['battletag']))
                    embed.title = jsd['battletag']
                    if jsd['overall_stats']['avatar']:
                        embed.set_thumbnail(url=jsd['overall_stats']['avatar'])
                    embed.add_field(name="Rank and Level", value="**Level:** {}\n**Rank:** {}\n".format(jsd['overall_stats']['level'], jsd['overall_stats']['comprank'] or 0))
                    embed.add_field(name="Pain Caused", value="**{}**".format(jsd['game_stats']['damage_done']))
                    embed.add_field(name="Sad Endings", value="**{}**".format(jsd['game_stats']['deaths']))
                    embed.add_field(name="Eliminations", value="**{}**".format(jsd['game_stats']['eliminations']))
                    embed.add_field(name="Killshots", value="**{}**".format(jsd['game_stats']['final_blows']))
                    await self.bot.send_message(message.channel, embed=embed)

    async def owheroes(self, message):
        name = " ".join(message.content.split(" ")[1:]).replace('#', '-')
        with aiohttp.ClientSession() as session:
            async with session.get(self.apiurl + "{}/heroes/general".format(name), headers=self.header) as response:
                if response.status == 404:
                    await self.bot.send_message(message.channel, "Battletag not found.")
                elif response.status == 500:
                    await self.bot.send_message(message.channel, "Server under heavy load. Please try again later.")
                else:
                    jsd = await response.json()
                    message = "{}'s Heroes.\n```xl\n".format(jsd['battletag'])
                    for hero in [x for x in jsd['heroes'] if jsd['heroes'][x] > 0]:
                        message += "{} - Time Played(Hrs): {}\n".format(hero, round(jsd['heroes'][hero], 2))
                    await self.bot.send_message(message.channel, message + '```')

    async def owhero(self, message):
        name = " ".join(message.content.split(" ")[1:]).split(":")[0].replace('#', '-')
        hname = " ".join(message.content.split(" ")[1:]).split(":")[1]
        if hname.isdigit():
            if hname not in self.index:
                await self.bot.send_message(message.channel, "That's not a valid hero id.")
            else:
                hname = self.index[hname]
        else:
            found = False
            for hero in self.characters:
                if hname.lower() in hero['names']:
                    hname = self.index[hero['id']]
                    found = True
                    break
            if not found:
                await self.bot.send_message(message.channel, "Couldn't find a hero with that name.")
        with aiohttp.ClientSession() as session:
            async with session.get(self.apiurl + "{}/heroes/{}".format(name, hname), headers=self.header) as response:
                if response.status == 404:
                    await self.bot.send_message(message.channel, "Couldn't find that battletag.")
                elif response.status == 500:
                    await self.bot.send_message(message.channel, "Server under heavy load. Please try again later.")
                else:
                    jsd = await response.json()
                    messages = []
                    message = "{}'s stats for {}\n".format(name, hname)
                    messages.append(message)
                    msg = "General Stats\n"
                    for stat in [x for x in jsd['general_stats'] if 'guid' not in x]:
                        msg += "   {}: {}\n".format(stat, jsd['general_stats'][stat])
                    messages.append(msg)
                    msg = "Hero Specific Stats\n"
                    for stat in [x for x in jsd['hero_stats'] if 'guid' not in x]:
                        msg += "   {}: {}\n".format(stat, jsd['hero_stats'][stat])
                    messages.append(msg)
                    await self.bot.send_message(message.channel, "\n".join(messages))
