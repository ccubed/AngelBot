import aiohttp

class OWAPI:
    def __init__(self, pool):
        self.apiurl = "https://owapi.net/api/v2/u/"
        self.apiurlheroes = "https://owapi.net/api/v1/u/"  # Use this until heroes is built into v2
        # Map Numbers to names
        self.index = {1: 'Roadhog', 2: 'Junkrat', 3: 'Lucio', 4: 'Soldier: 76', 5: 'Zarya', 6: 'McCree', 7: 'Tracer', 8: 'Reaper',
                      9: 'Widowmaker', 10: 'Winston', 11: 'Pharah', 12: 'Reinhardt', 13: 'Symmetra', 14: 'Torbjorn', 15: 'Bastion',
                      16: 'Hanzo', 17: 'Mercy', 18: 'Zenyatta', 20: 'Mei', 21: 'Genji', 22: 'D.Va'}
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

    async def ow(self, message):
        name = " ".join(message.content.split(" ")[1:])
        with aiohttp.ClientSession() as session:
            async with session.get(self.apiurl + "{}/stats".format(name), headers=self.header) as response:
                if response.status == 404:
                    return "Battletag not found."
                elif response.status == 500:
                    return "Server under heavy load. Please try again later."
                else:
                    jsd = await response.json()
                    messages = []
                    message = "{}'s General Stats\n```xl\n".format(jsd['battletag'])
                    message += "Damage Done: {}    Deaths: {}\n".format(jsd['game_stats']['damage_done'], jsd['game_stats']['deaths'])
                    message += "Eliminations: {}    Final Blows: {}\n".format(jsd['game_stats']['eliminations'], jsd['game_stats']['final_blows'])
                    message += "Games Played: {}    Games Won: {}\n".format(jsd['game_stats']['games_played'], jsd['game_stats']['games_won'])
                    message += "Win Percentage: {}%\n```".format(jsd['overall_stats']['win_rate'])
                    messages.append(message)
                    message = "{}'s Kill Stats\n```xl\n".format(jsd['battletag'])
                    message += "Solo Kills: {}    Objective Kills: {}\n".format(jsd['game_stats']['solo_kills'], jsd['game_stats']['objective_kills'])
                    message += "Offensive Assists: {}    Defensive Assists: {}\n".format(jsd['game_stats']['offensive_assists'], jsd['game_stats']['defensive_assists'])
                    message += "Recon Assists: {}\n```".format(jsd['game_stats']['recon_assists'])
                    messages.append(message)
                    message = "{}'s Medal Stats\n```xl\n".format(jsd['battletag'])
                    message += "Total Medals: {}\nGold Medals: {}\nSilver Medals: {}\nBronze Medals: {}\nTotal Time Played: {}\n```".format(jsd['game_stats']['medals'],
                                                                                                                                            jsd['game_stats']['medals_gold'],
                                                                                                                                            jsd['game_stats']['medals_silver'],
                                                                                                                                            jsd['game_stats']['medals_bronze'],
                                                                                                                                            jsd['game_stats']['time_played'])
                    messages.append(message)
                    return messages

    async def owheroes(self, message):
        name = " ".join(message.content.split(" ")[1:])
        with aiohttp.ClientSession() as session:
            async with session.get(self.apiurlheroes + "{}/heroes".format(name), headers=self.header) as response:
                if response.status == 404:
                    return "Battletag not found."
                elif response.status == 500:
                    return "Server under heavy load. Please try again later."
                else:
                    jsd = await response.json()
                    message = "{}'s top 5 played heroes.\n```xl\n".format(jsd['battletag'])
                    for hero in jsd['heroes']:
                        message += "{}\n    KPD: {}\n    Games: {}\n    Win %: {}\n".format(hero['name'], hero['kpd'],
                                                                                            hero['games'], hero['winrate'])
                    return message + '```'

    async def owhero(self, message):
        name = " ".join(message.content.split(" ")[1:]).split(":")[0]
        hname = " ".join(message.content.split(" ")[1:]).split(":")[1]
        hid = 0
        if hname.isdigit():
            if hname not in self.index:
                return "That's not a valid hero id."
            else:
                hid = hname
        else:
            for hero in self.characters:
                if hname.lower() in hero['names']:
                    hid = hero['id']
            if hid == 0:
                return "Couldn't find a hero with that name."
        with aiohttp.ClientSession() as session:
            async with session.get(self.apiurlheroes + "{}/heroes/{}".format(name, hid), headers=self.header, params={'region': 'us'}) as response:
                if response.status == 404:
                    return "Couldn't find that battletag."
                elif response.status == 500:
                    return "Server under heavy load. Please try again later."
                else:
                    jsd = await response.json()
                    messages = []
                    message = "{}'s stats for {}\n".format(name, self.index[hid])
                    messages.append(message)
                    for type in jsd['stats']:
                        message = '{}\n```xl\n'.format(type['name'])
                        for stat in type['stats']:
                            message += '{}: {}\n'.format(stat['name'], stat['value'])
                        messages.append(message + "```")
                    return messages
