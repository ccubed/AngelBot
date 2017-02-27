import aiohttp
from discord import embeds

class DBParser:
    def __init__(self, client):
        self.apiurl = "https://api.xivdb.com"
        self.shortnames = {'ARC': 'Archer', 'GLA': 'Gladiator', 'LNC': 'Lancer', 'MRD': 'Marauder', 'PGL': 'Pugilist',
                           'ACN': 'Arcanist', 'CNJ': 'Conjurer', 'THM': 'Thaumaturge', 'ROG': 'Rogue',
                           'BRD': 'Bard', 'DRG': 'Dragoon', 'MNK': 'Monk', 'PLD': 'Paladin', 'WAR': 'Warrior',
                           'BLM': 'Black Mage', 'WHM': 'White Mage', 'SCH': 'Scholar', 'SMN': 'Summoner',
                           'NIN': 'Ninja', 'AST': 'Astrologian', 'DRK': 'Dark Knight', 'MCH': 'Machinist',
                           'ALC': 'Alchemist', 'ARM': 'Armorer', 'BSM': 'Blacksmith', 'CRP': 'Carpenter',
                           'CUL': 'Culinerian', 'GSM': 'Goldsmith', 'LTW': 'Leatherworker', 'WVR': 'Weaver',
                           'BTN': 'Botanist', 'FSH': 'Fisher', 'MIN': 'Miner'}
        self.commands = [['item', self.searchitem], ['quest', self.searchquest],
                         ['recipe', self.searchrecipe], ['action', self.searchaction],
                         ['mats', self.searchmats], ['npc', self.searchnpc], ['effect', self.searchstatus],
                         ['minion', self.searchminion], ['achievement', self.searchachievement]]
        self.bot = client

    async def searchid(self, name):
        isid = None
        try:
            int(name)
            isid = True
        except ValueError:
            isid = False
        data = {'string': name}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jsd = await response.json()
                if isid:
                    for x in [x for x in list(jsd.keys()) if jsd[x]['total']]:
                        async with session.get(url, params={'string': jsd[x]['results'][0]['name']}, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                            jsd = await response.json()
                return jsd

    async def searchitem(self, message):
        data = {'string': " ".join(message.content.split(' ')[1:]), 'one': 'items'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jsd = await response.json()
                if jsd['items']['total'] == 0:
                    await self.bot.send_message(message.channel, "No results for {0} in items.".format(" ".join(message.content.split(" ")[1:])))
                elif jsd['items']['total'] == 1:
                    await self.bot.send_message(message.channel, await self.parseitem(str(jsd['items']['results'][0]['id'])))
                else:
                    embed = embeds.Embed(description="Search results for {} in items.".format(" ".join(message.content.split()[1:])))
                    embed.set_thumbnail(url="http://i.imgur.com/zkqe2nw.jpg")
                    msgs = [["", ""], ["", ""], ["", ""]]
                    for idx, item in enumerate(jsd['items']['results']):
                        if len(msgs[idx%3][0]) + len("[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))) < 1024:
                            msgs[idx%3][0] += "[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))
                            msgs[idx%3][1] += "ID: {}\n".format(item['id'])
                    embed.add_field(name="\u200b", value=msgs[0][0])
                    embed.add_field(name="\u200b", value=msgs[0][1])
                    embed.add_field(name="\u200b", value=msgs[1][0])
                    embed.add_field(name="\u200b", value=msgs[1][1])
                    embed.add_field(name="\u200b", value=msgs[2][0])
                    embed.add_field(name="\u200b", value=msgs[2][1])
                    embed.set_footer(text="Some search terms return large result sets. Your results may have been paired down.")
                    await self.bot.send_message(message.channel, embed=embed)


    async def searchquest(self, message):
        data = {'string': " ".join(message.content.split(' ')[1:]), 'one': 'quests'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                if response.status != 200:
                    print(response.status)
                    print(await response.text())
                    return
                jsd = await response.json()
                if jsd['quests']['total'] == 0:
                    await self.bot.send_message(message.channel, "No results for {0} in quests.".format(" ".join(message.content.split(" ")[1:])))
                elif jsd['quests']['total'] == 1:
                    await self.bot.send_message(message.channel, await self.parsequest(str(jsd['quests']['results'][0]['id'])))
                else:
                    out = embeds.Embed(description="Search results for {} in quests.".format(" ".join(message.content.split()[1:])))
                    out.set_thumbnail(url="http://i.imgur.com/zkqe2nw.jpg")
                    msgs = [["", ""], ["", ""], ["", ""]]
                    for idx, item in enumerate(jsd['quests']['results']):
                        if len(msgs[idx % 3][0]) + len("[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))) < 1024:
                            msgs[idx % 3][0] += "[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))
                            msgs[idx % 3][1] += "ID: {}\n".format(item['id'])
                    out.add_field(name="\u200b", value=msgs[0][0])
                    out.add_field(name="\u200b", value=msgs[0][1])
                    out.add_field(name="\u200b", value=msgs[1][0])
                    out.add_field(name="\u200b", value=msgs[1][1])
                    out.add_field(name="\u200b", value=msgs[2][0])
                    out.add_field(name="\u200b", value=msgs[2][1])
                    out.set_footer(text="Some search terms return large result sets. Your results may have been paired down.")
                    print(out.to_dict())
                    await self.bot.send_message(message.channel, embed=out)

    async def searchrecipe(self, message):
        data = {'string': " ".join(message.content.split(' ')[1:]), 'one': 'recipes'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jsd = await response.json()
                if jsd['recipes']['total'] == 0:
                    await self.bot.send_message(message.channel, "No results for {0} in recipes.".format(" ".join(message.content.split(" ")[1:])))
                elif jsd['recipes']['total'] == 1:
                    await self.bot.send_message(message.channel, await self.parserecipe(str(jsd['recipes']['results'][0]['id'])))
                else:
                    embed = embeds.Embed(description="Search results for {} in recipes.".format(" ".join(message.content.split()[1:])))
                    embed.set_thumbnail(url="http://i.imgur.com/zkqe2nw.jpg")
                    msgs = [["", ""], ["", ""], ["", ""]]
                    for idx, item in enumerate(jsd['recipes']['results']):
                        if len(msgs[idx % 3][0]) + len("[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))) < 1024:
                            msgs[idx % 3][0] += "[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))
                            msgs[idx % 3][1] += "ID: {}\n".format(item['id'])
                    embed.add_field(name="\u200b", value=msgs[0][0])
                    embed.add_field(name="\u200b", value=msgs[0][1])
                    embed.add_field(name="\u200b", value=msgs[1][0])
                    embed.add_field(name="\u200b", value=msgs[1][1])
                    embed.add_field(name="\u200b", value=msgs[2][0])
                    embed.add_field(name="\u200b", value=msgs[2][1])
                    embed.set_footer(
                        text="Some search terms return large result sets. Your results may have been paired down.")
                    await self.bot.send_message(message.channel, embed=embed)

    async def searchaction(self, message):
        data = {'string': " ".join(message.content.split(' ')[1:]), 'one': 'actions'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jsd = await response.json()
                if jsd['actions']['total'] == 0:
                    await self.bot.send_message(message.channel, "No results for {0} in actions.".format(" ".join(message.content.split(" ")[1:])))
                elif jsd['actions']['total'] == 1:
                    await self.bot.send_message(message.channel, await self.parseaction(str(jsd['actions']['results'][0]['id'])))
                else:
                    embed = embeds.Embed(description="Search results for {} in actions.".format(" ".join(message.content.split()[1:])))
                    embed.set_thumbnail(url="http://i.imgur.com/zkqe2nw.jpg")
                    msgs = [["", ""], ["", ""], ["", ""]]
                    for idx, item in enumerate(jsd['actions']['results']):
                        if len(msgs[idx % 3][0]) + len("[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))) < 1024:
                            msgs[idx % 3][0] += "[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))
                            msgs[idx % 3][1] += "ID: {}\n".format(item['id'])
                    embed.add_field(name="\u200b", value=msgs[0][0])
                    embed.add_field(name="\u200b", value=msgs[0][1])
                    embed.add_field(name="\u200b", value=msgs[1][0])
                    embed.add_field(name="\u200b", value=msgs[1][1])
                    embed.add_field(name="\u200b", value=msgs[2][0])
                    embed.add_field(name="\u200b", value=msgs[2][1])
                    embed.set_footer(
                        text="Some search terms return large result sets. Your results may have been paired down.")
                    await self.bot.send_message(message.channel, embed=embed)

    async def searchmats(self, message):
        data = {'string': " ".join(message.content.split(' ')[1:]), 'one': 'gathering'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jsd = await response.json()
                if jsd['gathering']['total'] == 0:
                    await self.bot.send_message(message.channel, "No results for {0} in gathering.".format(" ".join(message.content.split(" ")[1:])))
                elif jsd['gathering']['total'] == 1:
                    await self.bot.send_message(message.channel, await self.parsegather(str(jsd['gathering']['results'][0]['id'])))
                else:
                    embed = embeds.Embed(description="Search results for {} in materials.".format(" ".join(message.content.split()[1:])))
                    embed.set_thumbnail(url="http://i.imgur.com/zkqe2nw.jpg")
                    msgs = [["", ""], ["", ""], ["", ""]]
                    for idx, item in enumerate(jsd['gathering']['results']):
                        if len(msgs[idx % 3][0]) + len("[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))) < 1024:
                            msgs[idx % 3][0] += "[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))
                            msgs[idx % 3][1] += "ID: {}\n".format(item['id'])
                    embed.add_field(name="\u200b", value=msgs[0][0])
                    embed.add_field(name="\u200b", value=msgs[0][1])
                    embed.add_field(name="\u200b", value=msgs[1][0])
                    embed.add_field(name="\u200b", value=msgs[1][1])
                    embed.add_field(name="\u200b", value=msgs[2][0])
                    embed.add_field(name="\u200b", value=msgs[2][1])
                    embed.set_footer(text="Some search terms return large result sets. Your results may have been paired down.")
                    await self.bot.send_message(message.channel, embed=embed)

    async def searchnpc(self, message):
        data = {'string': " ".join(message.content.split(' ')[1:]), 'one': 'npcs'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jsd = await response.json()
                if jsd['npcs']['total'] == 0:
                    await self.bot.send_message(message.channel, "No results for {0} in npcs.".format(" ".join(message.content.split(" ")[1:])))
                elif jsd['npcs']['total'] == 1:
                    await self.bot.send_message(message.channel, await self.parsenpc(str(jsd['npcs']['results'][0]['id'])))
                else:
                    embed = embeds.Embed(description="Search results for {} in NPCs.".format(" ".join(message.content.split()[1:])))
                    embed.set_thumbnail(url="http://i.imgur.com/zkqe2nw.jpg")
                    msgs = [["", ""], ["", ""], ["", ""]]
                    for idx, item in enumerate(jsd['npcs']['results']):
                        if len(msgs[idx % 3][0]) + len("[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))) < 1024:
                            msgs[idx % 3][0] += "[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))
                            msgs[idx % 3][1] += "ID: {}\n".format(item['id'])
                    embed.add_field(name="\u200b", value=msgs[0][0])
                    embed.add_field(name="\u200b", value=msgs[0][1])
                    embed.add_field(name="\u200b", value=msgs[1][0])
                    embed.add_field(name="\u200b", value=msgs[1][1])
                    embed.add_field(name="\u200b", value=msgs[2][0])
                    embed.add_field(name="\u200b", value=msgs[2][1])
                    embed.set_footer(text="Some search terms return large result sets. Your results may have been paired down.")
                    await self.bot.send_message(message.channel, embed=embed)

    async def searchstatus(self, message):
        data = {'string': " ".join(message.content.split(' ')[1:]), 'one': 'status'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jsd = await response.json()
                if jsd['status']['total'] == 0:
                    await self.bot.send_message(message.channel, "No results for {0} in status.".format(" ".join(message.content.split(" ")[1:])))
                elif jsd['status']['total'] == 1:
                    await self.bot.send_message(message.channel, await self.parsestatus(str(jsd['status']['results'][0]['id'])))
                else:
                    embed = embeds.Embed(description="Search results for {} in status effects.".format(" ".join(message.content.split()[1:])))
                    embed.set_thumbnail(url="http://i.imgur.com/zkqe2nw.jpg")
                    msgs = [["", ""], ["", ""], ["", ""]]
                    for idx, item in enumerate(jsd['status']['results']):
                        if len(msgs[idx % 3][0]) + len("[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))) < 1024:
                            msgs[idx % 3][0] += "[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))
                            msgs[idx % 3][1] += "ID: {}\n".format(item['id'])
                    embed.add_field(name="\u200b", value=msgs[0][0])
                    embed.add_field(name="\u200b", value=msgs[0][1])
                    embed.add_field(name="\u200b", value=msgs[1][0])
                    embed.add_field(name="\u200b", value=msgs[1][1])
                    embed.add_field(name="\u200b", value=msgs[2][0])
                    embed.add_field(name="\u200b", value=msgs[2][1])
                    embed.set_footer(text="Some search terms return large result sets. Your results may have been paired down.")
                    await self.bot.send_message(message.channel, embed=embed)

    async def searchminion(self, message):
        data = {'string': " ".join(message.content.split(' ')[1:]), 'one': 'minions'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jsd = await response.json()
                if jsd['minions']['total'] == 0:
                    await self.bot.send_message(message.channel, "No results for {0} in minions.".format(" ".join(message.content.split(" ")[1:])))
                elif jsd['minions']['total'] == 1:
                    await self.bot.send_message(message.channel, await self.parseminion(str(jsd['minions']['results'][0]['id'])))
                else:
                    embed = embeds.Embed(description="Search results for {} in minions.".format(" ".join(message.content.split()[1:])))
                    embed.set_thumbnail(url="http://i.imgur.com/zkqe2nw.jpg")
                    msgs = [["", ""], ["", ""], ["", ""]]
                    for idx, item in enumerate(jsd['minions']['results']):
                        if len(msgs[idx % 3][0]) + len("[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))) < 1024:
                            msgs[idx % 3][0] += "[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))
                            msgs[idx % 3][1] += "ID: {}\n".format(item['id'])
                    embed.add_field(name="\u200b", value=msgs[0][0])
                    embed.add_field(name="\u200b", value=msgs[0][1])
                    embed.add_field(name="\u200b", value=msgs[1][0])
                    embed.add_field(name="\u200b", value=msgs[1][1])
                    embed.add_field(name="\u200b", value=msgs[2][0])
                    embed.add_field(name="\u200b", value=msgs[2][1])
                    embed.set_footer(text="Some search terms return large result sets. Your results may have been paired down.")
                    await self.bot.send_message(message.channel, embed=embed)

    async def searchachievement(self, message):
        data = {'string': " ".join(message.content.split(' ')[1:]), 'one': 'achievements'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jsd = await response.json()
                if jsd['achievements']['total'] == 0:
                    await self.bot.send_message(message.channel, "No results for {0} in achievements.".format(" ".join(message.content.split(" ")[1:])))
                elif jsd['achievements']['total'] == 1:
                    await self.bot.send_message(message.channel, await self.parseachievement(str(jsd['achievements']['results'][0]['id'])))
                else:
                    embed = embeds.Embed(description="Search results for {} in achievements.".format(" ".join(message.content.split()[1:])))
                    embed.set_thumbnail(url="http://i.imgur.com/zkqe2nw.jpg")
                    msgs = [["", ""], ["", ""], ["", ""]]
                    for idx, item in enumerate(jsd['achievements']['results']):
                        if len(msgs[idx % 3][0]) + len("[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))) < 1024:
                            msgs[idx % 3][0] += "[{}]({})\n".format(item['name'], "http://www.xivdb.com/{}".format(item['id']))
                            msgs[idx % 3][1] += "ID: {}\n".format(item['id'])
                    embed.add_field(name="\u200b", value=msgs[0][0])
                    embed.add_field(name="\u200b", value=msgs[0][1])
                    embed.add_field(name="\u200b", value=msgs[1][0])
                    embed.add_field(name="\u200b", value=msgs[1][1])
                    embed.add_field(name="\u200b", value=msgs[2][0])
                    embed.add_field(name="\u200b", value=msgs[2][1])
                    embed.set_footer(text="Some search terms return large result sets. Your results may have been paired down.")
                    await self.bot.send_message(message.channel, embed=embed)

    async def parseitem(self, name):
        url = self.apiurl + '/item/' + name
        with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jd = await response.json()
                message = "{0}\n{1} {2} {3} {4}\n{5}".format(jd['name'], 'Unique' if jd['is_unique'] else 'Common',
                                                             'Tradeable' if 'is_tradable' in jd else 'Untradable',
                                                             'Desynth' if 'is_desynthesizable' in jd else 'No_Desynth',
                                                             'Dyeable' if 'is_dyable' in jd else 'Undyeable', jd['url_xivdb'])
                return message

    async def parsequest(self, name):
        url = self.apiurl + "/quest/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jd = await response.json()
                message = "{0}\n".format(jd['name'])
                if jd['classjob_category_1'] in self.shortnames:
                    message += "   Related Class: {0}\n".format(self.shortnames[jd['classjob_category_1']])
                message += "   Start this quest with {0} in {1} at {2}x {3}y\n".format(jd['npc_start']['name'],
                                                                                    jd['npc_start']['placename']['name'],
                                                                                    jd['npc_start']['map_data']['points'][0]['app_position']['ingame']['x'],
                                                                                    jd['npc_start']['map_data']['points'][0]['app_position']['ingame']['y'])
                if 'pre_quests' in jd:
                    message += "Prerequisite Quests ->\n"
                    for item in jd['pre_quests']:
                        message += "   {0} (ID: {1})\n".format(item['name'], item['id'])
                message += jd['url_xivdb']
                return message

    async def parserecipe(self, name):
        url = self.apiurl + "/recipe/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jd = await response.json()
                message = "{0}\nClass: {1} Recipe Level: {2}\n".format(jd['name'], jd['classjob']['name'], jd['level'])
                message += "Materials Required:\n"
                for item in jd['tree']:
                    message += "   {0} {1} (ID:{2})\n".format(item['quantity'], item['name'], item['id'])
                message += jd['url_xivdb']
                return message

    async def parseaction(self, name):
        url = self.apiurl + "/action/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jd = await response.json()
                return "{0}\nClass: {1} Level: {2}\n{3}\n{4}".format(jd['name'], jd['classjob']['name'], jd['level'],
                                                                     jd['help'], jd['url_xivdb'])

    async def parseshop(self, name):
        url = self.apiurl + "/shop/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jd = await response.json()
                message = "{0} (ID: {1})\nThis shops sells ->\n".format(jd['npc_name'], jd['id'])
                for item in jd['items']:
                    message += "   {0} (ID: {1}) for {2}gil\n".format(item['item']['name'], item['item']['id'],
                                                                      item['item']['price_mid'])
                return message

    async def parsegather(self, name):
        url = self.apiurl + "/gathering/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jd = await response.json()
                message = "{0}\nGathered from:\n".format(jd['name'])
                for node in jd['nodes']:
                    message += "   {0} - {1}\n".format(jd['nodes'][node]['region']['name'], jd['nodes'][node]['name'])
                return message

    async def parsenpc(self, name):
        url = self.apiurl + "/npc/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jd = await response.json()
                message = "{0}".format(jd['name'])
                if jd['placename'] is None:
                    message += ' is an NPC from patch {} with no location data.'.format(jd['patch']['number'])
                else:
                    message += ' is an NPC from patch {} located in {} at {}x {}y'.format(jd['patch']['number'], jd['placename']['name'], jd['coordinates']['x'], jd['coordinates']['y'])
                return message

    async def parsestatus(self, name):
        url = self.apiurl + "/status/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jd = await response.json()
                return "Name: {0}\n{1}".format(jd['name'], jd['help'])

    async def parseminion(self, name):
        url = self.apiurl + "/minion/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jd = await response.json()
                message = "{0}\n   Minion Action: {1}\n   {2}".format(jd['name'], jd['action'], jd['help'])
                return message

    async def parseachievement(self, name):
        url = self.apiurl + "/achievement/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'User-Agent': 'AngelBot ( aiohttp 0.26.1 python 3.5.1 )'}) as response:
                jd = await response.json()
                return "{0} ({1} - {2})\n{3}".format(jd['name'], jd['category_name'], jd['kind_name'], jd['help'])

    async def parsehdim(self, name):
        if " ".join(name.content.split(" ")[1:]).isdigit():
            return await self.parserecipe(" ".join(name.content.split(" ")[1:]))
        else:
            jd = await self.searchid(" ".join(name.content.split(" ")[1:]))
            if jd['recipes']['total'] > 1:
                return "{0} matched more than 1 recipe. Maybe try finding the ID first with search?".format(name)
            elif jd['recipes']['total'] == 0:
                return "{0} didn't match a recipe.".format(name)
            else:
                return await self.parserecipe(str(jd['recipes']['results'][0]['id']))
