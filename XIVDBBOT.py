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

    def searchone(self, name, itype):
        key = itype.lower() if itype.endswith('s') else itype.lower() + 's'
        if key == 'gatherings':
            key = 'gathering'
        data = {'string': name, 'one': key}
        data = urllib.parse.urlencode(data)
        url = self.apiurl + '/search?' + data
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        if jd[key]['total'] == 0:
            return "No results for {0} within {1}.".format(name, key)
        elif jd[key]['total'] == 1:
            if key == 'items':
                return self.parseitem(str(jd[key]['results'][0]['id']))
            elif key == 'quests':
                return self.parsequest(str(jd[key]['results'][0]['id']))
            elif key == 'achievements':
                return self.parseachievement(str(jd[key]['results'][0]['id']))
            elif key == 'recipes':
                return self.parserecipe(str(jd[key]['results'][0]['id']))
            elif key == 'instances':
                return self.parseinstance(str(jd[key]['results'][0]['id']))
            elif key == 'actions':
                return self.parseaction(str(jd[key]['results'][0]['id']))
            elif key == 'places':
                return self.parseplace(str(jd[key]['results'][0]['id']))
            elif key == 'shops':
                return self.parseshop(str(jd[key]['results'][0]['id']))
            elif key == 'gathering':
                return self.parsegather(str(jd[key]['results'][0]['id']))
            elif key == 'npcs':
                return self.parsenpc(str(jd[key]['results'][0]['id']))
            elif key == 'enemies':
                return self.parseenemy(str(jd[key]['results'][0]['id']))
            elif key == 'emotes':
                return self.parseemote(str(jd[key]['results'][0]['id']))
            elif key == 'status':
                return self.parsestatus(str(jd[key]['results'][0]['id']))
            elif key == 'titles':
                return self.parsetitle(str(jd[key]['results'][0]['id']))
            elif key == 'minions':
                return self.parseminion(str(jd[key]['results'][0]['id']))
            elif key == 'mounts':
                return self.parsemount(str(jd[key]['results'][0]['id']))
        elif jd[key]['total'] <= 5:
            message = "Matched more than one result. Try searching by ID.\n"
            for items in jd[key]['results']:
                message += "{0} (ID: {1})\n".format(items['name'], items['id'])
            return message
        else:
            return "Returned {0} results. Add more words to search.".format(jd[key]['total'])

    def searchid(self, name):
        data = {'string': name}
        data = urllib.parse.urlencode(data)
        url = self.apiurl + '/search?' + data
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        return jd

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
                                                                            jd['npc_start']['position']['x'],
                                                                            jd['npc_start']['position']['y'])
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
            message += "   {0} (ID: {1}) for {2}gil\n".format(item['item']['name'], item['item']['id'], item['item']['price_mid'])
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
                        gathering.append('{0} Lv.{1} (Node ID: {2})'.format(item['type_name'], item['level'], item['id']))
            message = []
            if len(achievements):
                message.append("Obtained from Achievements ->\n")
                for item in achievements:
                    message.append("   {0} (ID: {1})\n".format(item[0], item[1]))
            if len(instances):
                message.append("Obtained from Dungeons ->\n")
                for item in instances:
                    message.append("   {0}\n".format(item))
            if len(quests):
                message.append("Obtained from Quests ->\n")
                for item in quests:
                    message.append("   {0} (ID: {1})\n".format(item[0], item[1]))
            if len(shops):
                message.append("Obtained from Shops ->\n")
                for item in shops:
                    message.append("   {0} in {1} at {2}x {3}y\n".format(item[0], item[1], item[2], item[3]))
            if len(craftable):
                message.append("Can be Crafted ->\n")
                for item in craftable:
                    message.append("   {0} (ID: {1}) {2} Lv.{3}\n".format(item[0], item[1], item[2], item[3]))
            if len(enemies):
                message.append("Dropped from Enemies ->\n")
                for item in enemies:
                    message.append(
                        "{0} (ID: {1}) in {2}{3}".format(item[0], item[1], item[2] if len(item) > 2 else "",
                                                         item[3] if len(item) > 3 else ""))
            if len(gathering):
                message.append("Can be Gathered ->\n")
                for item in gathering:
                    message.append(item)
            return message
        else:
            return ["No match found."]
