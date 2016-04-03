import urllib.request
import urllib.parse
import json


class DBParser:
    def __init__(self):
        self.apiurl = "http://api.xivdb.com"

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
        pass

    def parseitem(self, name):
        pass

    def parsequest(self, name):
        pass

    def parserecipe(self, name):
        pass

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
