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
        if key is 'gatherings':
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
                                                     'Tradeable' if jd['is_tradable'] else 'Untradable',
                                                     'Desynth' if jd['is_desynthesizable'] else 'No_Desynth',
                                                     'Dyeable' if jd['is_dyeable'] else 'Undyeable', jd['url_xivdb'])
        return message

    def parsequest(self, name):
        url = self.apiurl + "/quest/" + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        message = "{0}\n".format(jd['name'])
        if jd['classjob_category_1']['name'] in self.shortnames:
            message += "Related Class: {0}\n".format(shortnames[jd['classjob_category_1']['name']])
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
        return "This doesn't seem to be in the api currently."

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
        return "Eveb if an enemy is parsed, since the change to XIVDB version 2 all the position data on enemies went away."

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
        types = []
        for key in jd.keys():
            if jd[key]['total'] > 0:
                types.append(key)
        if len(types) > 1:
            return "Matched several items. Please narrow down your search. Perhaps search by ID?"
        elif len(types) == 1:
            if types[0] == 'items':
            elif types[0] == 'gathering':
            elif types[0] == 'quests':
            else:
                return "We found your match, but it's a type that doesn't currently have location data on XIVDB."
        else:
            return "No matches for that search."