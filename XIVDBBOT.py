import aiohttp

class DBParser:
    def __init__(self, redis):
        self.apiurl = "https://api.xivdb.com"
        self.shortnames = {'ARC': 'Archer', 'GLA': 'Gladiator', 'LNC': 'Lancer', 'MRD': 'Marauder', 'PGL': 'Pugilist',
                           'ACN': 'Arcanist', 'CNJ': 'Conjurer', 'THM': 'Thaumaturge', 'ROG': 'Rogue',
                           'BRD': 'Bard', 'DRG': 'Dragoon', 'MNK': 'Monk', 'PLD': 'Paladin', 'WAR': 'Warrior',
                           'BLM': 'Black Mage', 'WHM': 'White Mage', 'SCH': 'Scholar', 'SMN': 'Summoner',
                           'NIN': 'Ninja', 'AST': 'Astrologian', 'DRK': 'Dark Knight', 'MCH': 'Machinist',
                           'ALC': 'Alchemist', 'ARM': 'Armorer', 'BSM': 'Blacksmith', 'CRP': 'Carpenter',
                           'CUL': 'Culinerian', 'GSM': 'Goldsmith', 'LTW': 'Leatherworker', 'WVR': 'Weaver',
                           'BTN': 'Botanist', 'FSH': 'Fisher', 'MIN': 'Miner'}
        self.commands = [['search', self.searchall], ['item', self.searchitem], ['quest', self.searchquest],
                         ['recipe', self.searchrecipe], ['action', self.searchaction],
                         ['mats', self.searchmats], ['npc', self.searchnpc], ['effect', self.searchstatus],
                         ['minion', self.searchminion], ['achievement', self.searchachievement],
                         ['hdim', self.parsehdim], ['wdif', self.parsewdif]]

    async def searchall(self, message):
        data = {'string': message.content[7:]}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data) as response:
                jsd = await response.json()
                msg = "Matched...\n"
                for key in jsd:
                    if jsd[key]['total'] > 0:
                        msg += "{0} {1}\n".format(jsd[key]['total'], key)
                msg += "Ask for a specific category or add more words."
                return msg

    async def searchid(self, name):
        data = {'string': name}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data) as response:
                jsd = await response.json()
                return jsd

    async def searchitem(self, message):
        data = {'string': message.content[6:], 'one': 'items'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data) as response:
                jsd = await response.json()
                if jsd['items']['total'] == 0:
                    return "No results for {0} in items.".format(message.content[6:])
                elif jsd['items']['total'] == 1:
                    return await self.parseitem(str(jsd['items']['results'][0]['id']))
                elif jsd['items']['total'] <= 5:
                    message = "Matched more than one item. Try searching by ID.\n"
                    for items in jsd['items']['results']:
                        message += "{0} (ID: {1})\n".format(items['name'], items['id'])
                    return message
                else:
                    return "Returned {0} results. Add more words to search.".format(jsd['items']['total'])

    async def searchquest(self, message):
        data = {'string': message.content[7:], 'one': 'quests'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data) as response:
                jsd = await response.json()
                if jsd['quests']['total'] == 0:
                    return "No results for {0} in quests.".format(message.content[7:])
                elif jsd['quests']['total'] == 1:
                    return await self.parsequest(str(jsd['quests']['results'][0]['id']))
                elif jsd['quests']['total'] <= 5:
                    message = "Matched more than one quest. Try searching by ID.\n"
                    for quests in jsd['quests']['results']:
                        message += "{0} (ID: {1})\n".format(quests['name'], quests['id'])
                    return message
                else:
                    return "Returned {0} results. Add more words to search.".format(jsd['quests']['total'])

    async def searchrecipe(self, message):
        data = {'string': message.content[8:], 'one': 'recipes'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data) as response:
                jsd = await response.json()
                if jsd['recipes']['total'] == 0:
                    return "No results for {0} in recipes.".format(message.content[8:])
                elif jsd['recipes']['total'] == 1:
                    return await self.parserecipe(str(jsd['recipes']['results'][0]['id']))
                elif jsd['recipes']['total'] <= 5:
                    message = "Matched more than one recipe. Try searching by ID.\n"
                    for recipes in jsd['recipes']['results']:
                        message += "{0} (ID: {1})\n".format(recipes['name'], recipes['id'])
                    return message
                else:
                    return "Returned {0} results. Add more words to search.".format(jsd['recipes']['total'])

    async def searchaction(self, message):
        data = {'string': message.content[8:], 'one': 'actions'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data) as response:
                jsd = await response.json()
                if jsd['actions']['total'] == 0:
                    return "No results for {0} in actions.".format(message.content[8:])
                elif jsd['actions']['total'] == 1:
                    return await self.parseaction(str(jsd['actions']['results'][0]['id']))
                elif jsd['actions']['total'] <= 5:
                    message = "Matched more than one action. Try searching by ID.\n"
                    for actions in jsd['actions']['results']:
                        message += "{0} (ID: {1})\n".format(actions['name'], actions['id'])
                    return message
                else:
                    return "Returned {0} results. Add more words to search.".format(jsd['actions']['total'])

    async def searchmats(self, message):
        data = {'string': message.content[6:], 'one': 'gathering'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data) as response:
                jsd = await response.json()
                if jsd['gathering']['total'] == 0:
                    return "No results for {0} in gathering.".format(message.content[8:])
                elif jsd['gathering']['total'] == 1:
                    return await self.parsegather(str(jsd['gathering']['results'][0]['id']))
                elif jsd['gathering']['total'] <= 5:
                    message = "Matched more than one material. Try searching by ID.\n"
                    for gathering in jsd['gathering']['results']:
                        message += "{0} (ID: {1})\n".format(gathering['name'], gathering['id'])
                    return message
                else:
                    return "Returned {0} results. Add more words to search.".format(jsd['gathering']['total'])

    async def searchnpc(self, message):
        data = {'string': message.content[5:], 'one': 'npcs'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data) as response:
                jsd = response.json()
                if jsd['npcs']['total'] == 0:
                    return "No results for {0} in npcs.".format(message.content[5:])
                elif jsd['npcs']['total'] == 1:
                    return await self.parsenpc(str(jsd['npcs']['results'][0]['id']))
                elif jsd['npcs']['total'] <= 5:
                    message = "Matched more than one npc. Try searching by ID.\n"
                    for npcs in jsd['npcs']['results']:
                        message += "{0} (ID: {1})\n".format(npcs['name'], npcs['id'])
                    return message
                else:
                    return "Returned {0} results. Add more words to search.".format(jsd['npcs']['total'])

    async def searchstatus(self, message):
        data = {'string': message.content[8:], 'one': 'status'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data) as response:
                jsd = response.json()
                if jsd['status']['total'] == 0:
                    return "No results for {0} in status.".format(message.content[8:])
                elif jsd['status']['total'] == 1:
                    return await self.parsestatus(str(jsd['status']['results'][0]['id']))
                elif jsd['status']['total'] <= 5:
                    message = "Matched more than one status effect. Try searching by ID.\n"
                    for status in jsd['status']['results']:
                        message += "{0} (ID: {1})\n".format(status['name'], status['id'])
                    return message
                else:
                    return "Returned {0} results. Add more words to search.".format(jsd['status']['total'])

    async def searchminion(self, message):
        data = {'string': message.content[8:], 'one': 'minions'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data) as response:
                jsd = response.json()
                if jsd['minions']['total'] == 0:
                    return "No results for {0} in minions.".format(message.content[8:])
                elif jsd['minions']['total'] == 1:
                    return await self.parseminion(str(jsd['minions']['results'][0]['id']))
                elif jsd['minions']['total'] <= 5:
                    message = "Matched more than one minion. Try searching by ID.\n"
                    for minions in jsd['minions']['results']:
                        message += "{0} (ID: {1})\n".format(minions['name'], minions['id'])
                    return message
                else:
                    return "Returned {0} results. Add more words to search.".format(jsd['minion']['total'])

    async def searchachievement(self, message):
        data = {'string': message.content[13:], 'one': 'achievements'}
        url = self.apiurl + '/search'
        with aiohttp.ClientSession() as session:
            async with session.get(url, params=data) as response:
                jsd = await response.json()
                if jsd['achievements']['total'] == 0:
                    return "No results for {0} in achievements.".format(message.content[13:])
                elif jsd['achievements']['total'] == 1:
                    return await self.parserecipe(str(jsd['achievements']['results'][0]['id']))
                elif jsd['achievements']['total'] <= 5:
                    message = "Matched more than one achievement. Try searching by ID.\n"
                    for achievements in jsd['achievements']['results']:
                        message += "{0} (ID: {1})\n".format(achievements['name'], achievements['id'])
                    return message
                else:
                    return "Returned {0} results. Add more words to search.".format(jsd['achievements']['total'])

    async def parseitem(self, name):
        url = self.apiurl + '/item/' + name
        with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jd = await response.json()
                message = "{0}\n{1} {2} {3} {4}\n{5}".format(jd['name'], 'Unique' if jd['is_unique'] else 'Common',
                                                             'Tradeable' if 'is_tradable' in jd else 'Untradable',
                                                             'Desynth' if 'is_desynthesizable' in jd else 'No_Desynth',
                                                             'Dyeable' if 'is_dyable' in jd else 'Undyeable', jd['url_xivdb'])
                return message

    async def parsequest(self, name):
        url = self.apiurl + "/quest/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jd = await response.json()
                message = "{0}\n".format(jd['name'])
                if jd['classjob_category_1']['name'] in self.shortnames:
                    message += "Related Class: {0}\n".format(self.shortnames[jd['classjob_category_1']['name']])
                message += "Start this quest with {0} in {1} at {2}x {3}y\n".format(jd['npc_start']['name'],
                                                                                    jd['npc_start']['placename']['name'],
                                                                                    jd['npc_start']['position']['x'] if
                                                                                    jd['npc_start']['position'] != '' else '0',
                                                                                    jd['npc_start']['position']['y'] if
                                                                                    jd['npc_start']['position'] != '' else '0')
                if 'pre_quest' in jd:
                    message += "Prerequisite Quests ->\n"
                    for item in jd['pre_quest']:
                        message += "{0} (ID: {1})\n".format(item['name'], item['id'])
                message += jd['url_xivdb']
                return message

    async def parserecipe(self, name):
        url = self.apiurl + "/recipe/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jd = await response.json()
                message = "{0}\nClass: {1} Recipe Level: {2}\n".format(jd['name'], jd['classjob']['name'], jd['level'])
                message += "Materials Required:\n"
                for item in jd['_tree']:
                    message += "   {0} {1} (ID:{2})\n".format(item['quantity'], item['name'], item['id'])
                message += jd['url_xivdb']
                return message

    async def parseaction(self, name):
        url = self.apiurl + "/action/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jd = await response.json()
                return "{0}\nClass: {1} Level: {2}\n{3}\n{4}".format(jd['name'], jd['classjob']['name'], jd['level'],
                                                                     jd['help'], jd['url_xivdb'])

    async def parseshop(self, name):
        url = self.apiurl + "/shop/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
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
                    message += "   {0} - {1} - {2}\n".format(node['region']['name'], node['zone']['name'],
                                                             node['placename']['name'])
                return message

    async def parsenpc(self, name):
        url = self.apiurl + "/npc/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jd = await response.json()
                message = "{0} is located in {1} at {2}x {3}y".format(jd['name'], jd['placename']['name'],
                                                                      jd['coordinates']['x'], jd['coordinates']['y'])
                return message

    async def parseenemy(self, name):
        url = self.apiurl + "/enemy/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jd = await response.json()
                message = "{0}\n".format(jd['name'])
                if 'region_name' in jd:
                    message += "Region: {0}\n".format(jd['region_name'])
                else:
                    message += "Region: No data\n"
                if 'placename' in jd:
                    message += "Found near: {0}".format(jd['placename']['name'])
                else:
                    message += "Found near: No location data"
                return message

    async def parsestatus(self, name):
        url = self.apiurl + "/status/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jd = await response.json()
                return "Name: {0}\n{1}".format(jd['name'], jd['help'])

    async def parseminion(self, name):
        url = self.apiurl + "/minion/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jd = await response.json()
                message = "{0}\n   Minion Action: {1}\n   {2}".format(jd['name'], jd['action'], jd['help'])
                return message

    async def parseachievement(self, name):
        url = self.apiurl + "/achievement/" + name
        with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                jd = await response.json()
                return "{0} ({1} - {2})\n{3}".format(jd['name'], jd['category_name'], jd['kind_name'], jd['help'])

    async def parsehdim(self, name):
        if name.content[6:].isnumeric():
            return await self.parserecipe(str(name.content[6:]))
        else:
            jd = await self.searchid(name.content[6:])
            if jd['recipes']['total'] > 1:
                return "{0} matched more than 1 recipe. Maybe try finding the ID first with search?".format(name)
            elif jd['recipes']['total'] == 0:
                return "{0} didn't match a recipe.".format(name)
            else:
                return await self.parserecipe(str(jd['recipes']['results'][0]['id']))

    async def parsewdif(self, name):
        jd = await self.searchid(name)
        if 'items' in jd:
            achievements = []
            if 'achievements' in jd:
                if jd['achievements']['total']:
                    for item in jd['achievements']['results']:
                        achievements.append([item['name'], item['id']])
            instances = []
            if 'instances' in jd:
                if jd['instances']['total']:
                    for item in jd['instances']['results']:
                        instances.append(item['name'])
            quests = []
            if 'quests' in jd:
                if jd['quests']['total']:
                    for item in jd['quests']['results']:
                        quests.append([item['name'], item['id']])
            shops = []
            if 'shops' in jd:
                if jd['shops']['total']:
                    for item in jd['shops']['results']:
                        for npc in item['npcs']:
                            shops.append(
                                [npc['name'], npc['placename']['name'], npc['position']['x'], npc['position']['y']])
            craftable = []
            if 'craftable' in jd:
                if jd['craftable']['total']:
                    for item in jd['craftable']['results']:
                        craftable.append([item['name'], item['id'], item['classjob']['name'], item['level']])
            enemies = []
            if 'enemies' in jd:
                if jd['enemies']['total']:
                    for item in jd['enemies']['results']:
                        temp = [item['name'], item['id']]
                        if 'zones' in item:
                            for zone in item['zones']:
                                if 'region' in zone:
                                    temp.append(zone['region']['name'])
                                if 'placename' in zone:
                                    temp.append(zone['placename']['name'])
                        enemies.append(temp)
            gathering = []
            if 'gathering' in jd:
                if jd['gathering']['total']:
                    for item in jd['gathering']['results']:
                        gathering.append(
                            '{0} Lv.{1} (Node ID: {2})'.format(item['type_name'], item['level'], item['id']))
            message = ""
            if len(achievements):
                message += "Obtained from Achievements ->\n"
                for item in achievements:
                    message += "   {0} (ID: {1})\n".format(item[0], item[1])
            if len(instances):
                message += "Obtained from Dungeons ->\n"
                for item in instances:
                    message += "   {0}\n".format(item)
            if len(quests):
                message += "Obtained from Quests ->\n"
                for item in quests:
                    message += "   {0} (ID: {1})\n".format(item[0], item[1])
            if len(shops):
                message += "Obtained from Shops ->\n"
                for item in shops:
                    message += "   {0} in {1} at {2}x {3}y\n".format(item[0], item[1], item[2], item[3])
            if len(craftable):
                message += "Can be Crafted ->\n"
                for item in craftable:
                    message += "   {0} (ID: {1}) {2} Lv.{3}\n".format(item[0], item[1], item[2], item[3])
            if len(enemies):
                message += "Dropped from Enemies ->\n"
                for item in enemies:
                    message += "{0} (ID: {1}) in {2}{3}".format(item[0], item[1], item[2] if len(item) > 2 else "",
                                                                item[3] if len(item) > 3 else "")
            if len(gathering):
                message += "Can be Gathered ->\n"
                for item in gathering:
                    message += item + "\n"
            if len(message):
                return message
            else:
                return "Item found but no location information is recorded."
        else:
            return "No match found."
