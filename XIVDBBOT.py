import urllib.request
import urllib.parse
import json


class DBParser:
    def __init__(self):
        self.apiurl = "https://api.xivdb.com"
        self.shortnames = {'ARC': 'Archer', 'GLA': 'Gladiator', 'LNC': 'Lancer', 'MRD': 'Marauder', 'PGL': 'Pugilist',
                           'ACN': 'Arcanist', 'CNJ': 'Conjurer', 'THM': 'Thaumaturge', 'ROG': 'Rogue',
                           'BRD': 'Bard', 'DRG': 'Dragoon', 'MNK': 'Monk', 'PLD': 'Paladin', 'WAR': 'Warrior',
                           'BLM': 'Black Mage', 'WHM': 'White Mage', 'SCH': 'Scholar', 'SMN': 'Summoner',
                           'NIN': 'Ninja', 'AST': 'Astrologian', 'DRK': 'Dark Knight', 'MCH': 'Machinist',
                           'ALC': 'Alchemist', 'ARM': 'Armorer', 'BSM': 'Blacksmith', 'CRP': 'Carpenter',
                           'CUL': 'Culinerian', 'GSM': 'Goldsmith', 'LTW': 'Leatherworker', 'WVR': 'Weaver',
                           'BTN': 'Botanist', 'FSH': 'Fisher', 'MIN': 'Miner'}
        self.commands = [['$search', self.searchall, 0], ['$item', self.searchitem, 0], ['$quest', self.searchquest, 0],
                         ['$recipe', self.searchrecipe, 0], ['$action', self.searchaction, 0],
                         ['$mats', self.searchmats, 0], ['$npc', self.searchnpc, 0], ['$effect', self.searchstatus, 0],
                         ['$minion', self.searchminion, 0], ['$achievement', self.searchachievement, 0],
                         ['$hdim', self.parsehdim, 0], ['$wdif', self.parsewdif, 1]]

    def searchall(self, name):
        data = {'string': name}
        data = urllib.parse.urlencode(data)
        url = self.apiurl + '/search?' + data
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        message = "Matched...\n"
        for key in jd.keys():
            if jd[key]['total'] > 0:
                message += "{0} {1}\n".format(jd[key]['total'], key)
        message += "Ask for a specific category or add more words."
        return message

    def searchid(self, name):
        data = {'string': name}
        data = urllib.parse.urlencode(data)
        url = self.apiurl + '/search?' + data
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        return jd

    def searchitem(self, name):
        data = {'string': name, 'one': 'items'}
        url = self.apiurl + '/search?' + urllib.parse.urlencode(data)
        response = urllib.request.urlopen(url)
        jd = json.loads(response.read().decode('utf-8'))
        if jd['items']['total'] == 0:
            return "No results for {0} in items.".format(name)
        elif jd['items']['total'] == 1:
            return self.parseitem(str(jd['items']['results'][0]['id']))
        elif jd['items']['total'] <= 5:
            message = "Matched more than one item. Try searching by ID.\n"
            for items in jd['items']['results']:
                message += "{0} (ID: {1})\n".format(items['name'], items['id'])
            return message
        else:
            return "Returned {0} results. Add more words to search.".format(jd['items']['total'])

    def searchquest(self, name):
        data = {'string': name, 'one': 'quests'}
        url = self.apiurl + '/search?' + urllib.parse.urlencode(data)
        response = urllib.request.urlopen(url)
        jd = json.loads(response.read().decode('utf-8'))
        if jd['quests']['total'] == 0:
            return "No results for {0} in quests.".format(name)
        elif jd['quests']['total'] == 1:
            return self.parsequest(str(jd['quests']['results'][0]['id']))
        elif jd['quests']['total'] <= 5:
            message = "Matched more than one quest. Try searching by ID.\n"
            for quests in jd['quests']['results']:
                message += "{0} (ID: {1})\n".format(quests['name'], quests['id'])
            return message
        else:
            return "Returned {0} results. Add more words to search.".format(jd['quests']['total'])

    def searchrecipe(self, name):
        data = {'string': name, 'one': 'recipes'}
        url = self.apiurl + '/search?' + urllib.parse.urlencode(data)
        response = urllib.request.urlopen(url)
        jd = json.loads(response.read().decode('utf-8'))
        if jd['recipes']['total'] == 0:
            return "No results for {0} in recipes.".format(name)
        elif jd['recipes']['total'] == 1:
            return self.parserecipe(str(jd['recipes']['results'][0]['id']))
        elif jd['recipes']['total'] <= 5:
            message = "Matched more than one recipe. Try searching by ID.\n"
            for recipes in jd['recipes']['results']:
                message += "{0} (ID: {1})\n".format(recipes['name'], recipes['id'])
            return message
        else:
            return "Returned {0} results. Add more words to search.".format(jd['recipes']['total'])

    def searchaction(self, name):
        data = {'string': name, 'one': 'actions'}
        url = self.apiurl + '/search?' + urllib.parse.urlencode(data)
        response = urllib.request.urlopen(url)
        jd = json.loads(response.read().decode('utf-8'))
        if jd['actions']['total'] == 0:
            return "No results for {0} in actions.".format(name)
        elif jd['actions']['total'] == 1:
            return self.parseaction(str(jd['actions']['results'][0]['id']))
        elif jd['actions']['total'] <= 5:
            message = "Matched more than one action. Try searching by ID.\n"
            for actions in jd['actions']['results']:
                message += "{0} (ID: {1})\n".format(actions['name'], actions['id'])
            return message
        else:
            return "Returned {0} results. Add more words to search.".format(jd['actions']['total'])

    def searchmats(self, name):
        data = {'string': name, 'one': 'gathering'}
        url = self.apiurl + '/search?' + urllib.parse.urlencode(data)
        response = urllib.request.urlopen(url)
        jd = json.loads(response.read().decode('utf-8'))
        if jd['gathering']['total'] == 0:
            return "No results for {0} in gathering.".format(name)
        elif jd['gathering']['total'] == 1:
            return self.parsegather(str(jd['gathering']['results'][0]['id']))
        elif jd['gathering']['total'] <= 5:
            message = "Matched more than one material. Try searching by ID.\n"
            for gathering in jd['gathering']['results']:
                message += "{0} (ID: {1})\n".format(gathering['name'], gathering['id'])
            return message
        else:
            return "Returned {0} results. Add more words to search.".format(jd['gathering']['total'])

    def searchnpc(self, name):
        data = {'string': name, 'one': 'npcs'}
        url = self.apiurl + '/search?' + urllib.parse.urlencode(data)
        response = urllib.request.urlopen(url)
        jd = json.loads(response.read().decode('utf-8'))
        if jd['npcs']['total'] == 0:
            return "No results for {0} in npcs.".format(name)
        elif jd['npcs']['total'] == 1:
            return self.parsenpc(str(jd['npcs']['results'][0]['id']))
        elif jd['npcs']['total'] <= 5:
            message = "Matched more than one npc. Try searching by ID.\n"
            for npcs in jd['npcs']['results']:
                message += "{0} (ID: {1})\n".format(npcs['name'], npcs['id'])
            return message
        else:
            return "Returned {0} results. Add more words to search.".format(jd['npcs']['total'])

    def searchstatus(self, name):
        data = {'string': name, 'one': 'status'}
        url = self.apiurl + '/search?' + urllib.parse.urlencode(data)
        response = urllib.request.urlopen(url)
        jd = json.loads(response.read().decode('utf-8'))
        if jd['status']['total'] == 0:
            return "No results for {0} in status.".format(name)
        elif jd['status']['total'] == 1:
            return self.parsestatus(str(jd['status']['results'][0]['id']))
        elif jd['status']['total'] <= 5:
            message = "Matched more than one status effect. Try searching by ID.\n"
            for status in jd['status']['results']:
                message += "{0} (ID: {1})\n".format(status['name'], status['id'])
            return message
        else:
            return "Returned {0} results. Add more words to search.".format(jd['status']['total'])

    def searchminion(self, name):
        data = {'string': name, 'one': 'minions'}
        url = self.apiurl + '/search?' + urllib.parse.urlencode(data)
        response = urllib.request.urlopen(url)
        jd = json.loads(response.read().decode('utf-8'))
        if jd['minions']['total'] == 0:
            return "No results for {0} in minions.".format(name)
        elif jd['minions']['total'] == 1:
            return self.parseminion(str(jd['minions']['results'][0]['id']))
        elif jd['minions']['total'] <= 5:
            message = "Matched more than one minion. Try searching by ID.\n"
            for minions in jd['minions']['results']:
                message += "{0} (ID: {1})\n".format(minions['name'], minions['id'])
            return message
        else:
            return "Returned {0} results. Add more words to search.".format(jd['minion']['total'])

    def searchachievement(self, name):
        data = {'string': name, 'one': 'achievements'}
        url = self.apiurl + '/search?' + urllib.parse.urlencode(data)
        response = urllib.request.urlopen(url)
        jd = json.loads(response.read().decode('utf-8'))
        if jd['achievements']['total'] == 0:
            return "No results for {0} in achievements.".format(name)
        elif jd['achievements']['total'] == 1:
            return self.parserecipe(str(jd['achievements']['results'][0]['id']))
        elif jd['achievements']['total'] <= 5:
            message = "Matched more than one achievement. Try searching by ID.\n"
            for achievements in jd['achievements']['results']:
                message += "{0} (ID: {1})\n".format(achievements['name'], achievements['id'])
            return message
        else:
            return "Returned {0} results. Add more words to search.".format(jd['achievements']['total'])

    def parseitem(self, name):
        url = self.apiurl + '/item/' + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        message = "{0}\n{1} {2} {3} {4}\n{5}".format(jd['name'], 'Unique' if jd['is_unique'] else 'Common',
                                                     'Tradeable' if 'is_tradable' in jd else 'Untradable',
                                                     'Desynth' if 'is_desynthesizable' in jd else 'No_Desynth',
                                                     'Dyeable' if 'is_dyable' in jd else 'Undyeable', jd['url_xivdb'])
        return message

    def parsequest(self, name):
        url = self.apiurl + "/quest/" + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
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

    def parserecipe(self, name):
        url = self.apiurl + "/recipe/" + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        message = "{0}\nClass: {1} Recipe Level: {2}\n".format(jd['name'], jd['classjob']['name'], jd['level'])
        message += "Materials Required:\n"
        for item in jd['_tree']:
            message += "   {0} {1} (ID:{2})\n".format(item['quantity'], item['name'], item['id'])
        message += jd['url_xivdb']
        return message

    def parseinstance(self, name):
        return "I don't parse dungeons. There isn't really any useful information on XIVDB about dungeons."

    def parseaction(self, name):
        url = self.apiurl + "/action/" + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        return "{0}\nClass: {1} Level: {2}\n{3}\n{4}".format(jd['name'], jd['classjob']['name'], jd['level'],
                                                             jd['help'], jd['url_xivdb'])

    def parseplace(self, name):
        return "I don't parse places. There isn't really any useful information on XIVDB about places."

    def parseshop(self, name):
        url = self.apiurl + "/shop/" + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        message = "{0} (ID: {1})\nThis shops sells ->\n".format(jd['npc_name'], jd['id'])
        for item in jd['items']:
            message += "   {0} (ID: {1}) for {2}gil\n".format(item['item']['name'], item['item']['id'],
                                                              item['item']['price_mid'])
        return message

    def parsegather(self, name):
        url = self.apiurl + "/gathering/" + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        message = "{0}\nGathered from:\n".format(jd['name'])
        for node in jd['nodes']:
            message += "   {0} - {1} - {2}\n".format(node['region']['name'], node['zone']['name'],
                                                     node['placename']['name'])
        return message

    def parsenpc(self, name):
        url = self.apiurl + "/npc/" + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        message = "{0} is located in {1} at {2}x {3}y".format(jd['name'], jd['placename']['name'],
                                                              jd['coordinates']['x'], jd['coordinates']['y'])
        return message

    def parseenemy(self, name):
        url = self.apiurl + "/enemy/" + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
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

    def parseemote(self, name):
        return "I don't parse emotes. There isn't really any useful information on XIVDB about emotes."

    def parsestatus(self, name):
        url = self.apiurl + "/status/" + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        return "Name: {0}\n{1}".format(jd['name'], jd['help'])

    def parsetitle(self, name):
        return "I don't parse titles. There isn't really any useful information on XIVDB about titles."

    def parseminion(self, name):
        url = self.apiurl + "/minion/" + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        message = "{0}\n   Minion Action: {1}\n   {2}".format(jd['name'], jd['action'], jd['help'])
        return message

    def parsemount(self, name):
        return "I don't parse mounts. There isn't really any useful information on XIVDB about mounts."

    def parseachievement(self, name):
        url = self.apiurl + "/achievement/" + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        return "{0} ({1} - {2})\n{3}".format(jd['name'], jd['category_name'], jd['kind_name'], jd['help'])

    def parsehdim(self, name):
        if name.isnumeric():
            return self.parserecipe(str(name))
        else:
            jd = self.searchid(name)
            if jd['recipes']['total'] > 1:
                return "{0} matched more than 1 recipe. Maybe try finding the ID first with search?".format(name)
            elif jd['recipes']['total'] == 0:
                return "{0} didn't match a recipe.".format(name)
            else:
                return self.parserecipe(str(jd['recipes']['results'][0]['id']))

    def parsewdif(self, name):
        jd = self.searchid(name)
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
            return ["No match found."]
