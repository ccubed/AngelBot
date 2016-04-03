import urllib.request
import urllib.parse
import json


class DBParser:
    def __init__(self):
        self.apiurl = "http://api.xivdb.com"
        self.shortnames = {'ARC':'Archer', 'GLA':'Gladiator', 'LNC':'Lancer', 'MRD':'Marauder', 'PGL':'Pugilist', 'ACN':'Arcanist', 'CNJ':'Conjurer', 'THM':'Thaumaturge', 'ROG':'Rogue',
                           'BRD':'Bard', 'DRG':'Dragoon', 'MNK':'Monk', 'PLD':'Paladin', 'WAR':'Warrior', 'BLM':'Black Mage', 'WHM':'White Mage', 'SCH':'Scholar', 'SMN':'Summoner',
                           'NIN':'Ninja', 'AST':'Astrologian', 'DRK':'Dark Knight', 'MCH':'Machinist', 'ALC':'Alchemist', 'ARM':'Armorer', 'BSM':'Blacksmith', 'CRP':'Carpenter',
                           'CUL':'Culinerian', 'GSM':'Goldsmith', 'LTW':'Leatherworker', 'WVR':'Weaver', 'BTN':'Botanist', 'FSH':'Fisher', 'MIN':'Miner'}

    def searchall(self, name):
        data = {'string': name}
        data = urllib.parse.urlencode(data)
        url = self.apiurl + '/search?' + data
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        message = "Matched..."
        for key in jd.keys():
            if jd[key]['total'] > 0:
                message += "{0} {1}".format(jd[key]['total'], key)
        message += "Ask for a specific category or add more words."
        return message

    def searchone(self, name, itype):
        key = itype.lower() if itype.endswith('s') else itype.lower() + 's'
        if key is 'gatherings':
            key = 'gathering'
        data = {'string': name, 'one': key }
        data = urllib.parse.urlencode(data)
        url = self.apiurl + '/search?' + data
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        if jd[key]['total'] == 0:
            return "No results for {0} within {1}.".format(name,key)
        elif jd[key]['total'] == 1:
            if key is 'items':
                return self.parseitem(jd[key]['results'][0]['id'])
            elif key is 'quests':
                return self.parsequest(jd[key]['results'][0]['id'])
            elif key is 'achievements':
                return self.parseachievement(jd[key]['results'][0]['id'])
            elif key is 'recipes':
                return self.parserecipe(jd[key]['results'][0]['id'])
            elif key is 'instances':
                return self.parseinstance(jd[key]['results'][0]['id'])
            elif key is 'actions':
                return self.parseaction(jd[key]['results'][0]['id'])
            elif key is 'places':
                return self.parseplace(jd[key]['results'][0]['id'])
            elif key is 'shops':
                return self.parseshop(jd[key]['results'][0]['id'])
            elif key is 'gathering':
                return self.parsegather(jd[key]['results'][0]['id'])
            elif key is 'npcs':
                return self.parsenpc(jd[key]['results'][0]['id'])
            elif key is 'enemies':
                return self.parseenemy(jd[key]['results'][0]['id'])
            elif key is 'emotes':
                return self.parseemote(jd[key]['results'][0]['id'])
            elif key is 'status':
                return self.parsestatus(jd[key]['results'][0]['id'])
            elif key is 'titles':
                return self.parsetitle(jd[key]['results'][0]['id'])
            elif key is 'minions':
                return self.parseminion(jd[key]['results'][0]['id'])
            elif key is 'mounts':
                return self.parsemount(jd[key]['results'][0]['id'])
        elif jd[key]['total'] <= 5:
            message = "Matched more than one result. Try searching by ID.\n"
            for items in jd[key]['results']:
                message += "{0} (ID: {1})\n".format(items['name'],items['id'])
            return message
        else:
            return "Returned {0} results. Add more words to search.".format(jd[key]['total'])

    def parseitem(self, name):
        url = self.apiurl + '/item/' + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        message = "{0}\n{1} {2} {3} {4}\n{5}".format(jd['name'], 'Unique' if jd['is_unique'] else 'Common', 'Tradeable' if jd['is_tradable'] else 'Untradable', 'Desynth' if jd['is_desynthesizable'] or 'No_Desynth', 'Dyeable' if jd['is_dyeable'] or 'Undyeable', jd['url_xivdb'])
        return message

    def parsequest(self, name):
        url = self.apiurl + "/quest/" + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)
        message = "{0}\n".format(jd['name'])
        if jd['classjob_category_1']['name'] in self.shortnames:
            message += "Related Class: {0}\n".format(shortnames[jd['classjob_category_1']['name']])
        message += "Start this quest with {0} in {1} at {2}x {3}y\n".format(jd['npc_start']['name'], jd['npc_start']['placename']['name'], jd['npc_start']['position']['x'], jd['npc_start']['position']['y'])
        message += jd['url_xivdb']
        return message

    def parserecipe(self, name):
        url = self.apiurl + "/quest/" + name
        response = urllib.request.urlopen(url)
        jd = response.read().decode('utf-8')
        jd = json.loads(jd)

    def parseinstance(self, name):
        pass

    def parseaction(self, name):
        pass

    def parseplace(self, name):
        pass

    def parseshop(self, name):
        pass

    def parsegather(self, name):
        pass

    def parsenpc(self, name):
        pass

    def parseenemy(self, name):
        pass

    def parseemote(self, name):
        pass

    def parsestatus(self, name):
        pass

    def parsetitle(self, name):
        pass

    def parseminion(self, name):
        pass

    def parsemount(self, name):
        pass

    def parsehdim(self, name):
        pass

    def parseachievement(self, name):
        pass

    def parsewdif(self, name):
        pass
