# DO YOU KNOW YOUR ANIMES!?
import requests
import time
from AnilistGlobals import *


class Animes:
    def __init__(self):
        self.authorizations = {}
        self.apiurl = "https://anilist.co/api"
        self.readonly = self.get_readonly()

    def get_readonly(self):
        data = {'grant_type': 'client_credentials', 'client_id': aniclient, 'client_secret': anisecret}
        url = self.apiurl + "/auth/access_token"
        response = requests.post(url, data)
        return response.json()

    def waifu(self, name):
        if self.readonly['expires'] < time.time():
            self.readonly = self.get_readonly()
        data = {'access_token': self.readonly['access_token']}
        url = self.apiurl + "/character/search/" + name.replace(' ', '%20')
        response = requests.get(url, params=data)
        whc = "{0}{1}!\n{2}".format(response.json()[0]['name_first'],
                                    '\b' + response.json()[0]['name_last'] if response.json()[0][
                                                                                  'name_last'] is not None else '',
                                    response.json()[0]['image_url_med'])
        return whc

    def searchcharacter(self, name):
        if self.readonly['expires'] < time.time():
            self.readonly = self.get_readonly()
        data = {'access_token': self.readonly['access_token']}
        url = self.apiurl + "/character/search/" + name.replace(' ', '%20')
        response = requests.get(url, params=data)
        jd = response.json()
        message = "Found these characters ->\n"
        for i in jd:
            message += "{0}{1} (ID: {2})\n".format(i['name_first'], i['name_last'], i['id'])
        return message
