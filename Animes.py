# DO YOU KNOW YOUR ANIMES!?
import urllib.request
import urllib.parse
import json
import time
from AnilistGlobals import *


class Animes:
    def __init__(self):
        self.pins = {}
        self.authorizations = {}
        self.apiurl = "https://anilist.co/api"
        self.readonly = self.get_readonly()

    def get_readonly(self):
        data = {'grant_type': 'client_credentials', 'client_id': aniclient, 'client_secret': anisecret}
        url = self.apiurl + "/auth/access_token" + urllib.parse.urlencode(data)
        response = urllib.request.urlopen(url)
        jd = json.loads(response.read().decode('utf-8'))
        return jd

    def waifu(self, name):
        if self.readonly['expires'] < time.time():
            self.readonly = self.get_readonly()
        data = {'access_token': self.readonly['access_token']}
        url = self.apiurl + "/character/search/" + name.replace('\b', '%20') + urllib.parse.urlencode(data)



