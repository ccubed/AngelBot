import requests
import time
import json


class AList:
    def __init__(self):
        self.apiurl = "https://anilist.co/api"
        file = open("Anilist_auths.json", mode="r")
        self.auths = json.load(file)
        file.close()
        file = open("Global_config.json", mode="r")
        self.config = json.load(file)
        file.close()
        if 'readonly' in self.auths and 'expires' in self.auths['readonly']:
            if self.auths['readonly']['expires'] < time.time():
                self.auths['readonly'] = self.get_readonly()
        else:
            self.auths['readonly'] = self.get_readonly()

    def get_readonly(self):
        data = {'grant_type': 'client_credentials', 'client_id': self.config['Anilist']['aniclient'],
                'client_secret': self.config['Anilist']['anisecret']}
        url = self.apiurl + "/auth/access_token"
        response = requests.post(url, data)
        return response.json()

    def waifu(self, name):
        if self.auths['readonly']['expires'] < time.time():
            self.auths['readonly'] = self.get_readonly()
        data = {'access_token': self.auths['readonly']['access_token']}
        url = self.apiurl + "/character/search/" + name.replace(' ', '%20')
        response = requests.get(url, params=data)
        whc = "{0}{1}!\n{2}".format(response.json()[0]['name_first'],
                                    '\b' + response.json()[0]['name_last'] if response.json()[0][
                                                                                  'name_last'] is not None else '',
                                    response.json()[0]['image_url_med'])
        return whc

    def searchcharacter(self, name):
        if self.auths['readonly']['expires'] < time.time():
            self.auths['readonly'] = self.get_readonly()
        data = {'access_token': self.auths['readonly']['access_token']}
        url = self.apiurl + "/character/search/" + name.replace(' ', '%20')
        response = requests.get(url, params=data)
        message = "Found these characters ->\n"
        for i in response.json():
            message += "{0}{1} (ID: {2})\n".format(i['name_first'], i['name_last'], i['id'])
        return message

    def exit(self):
        try:
            file = open("Anilist_auths.json", mode="w")
        except IOError:
            return 0
        else:
            json.dump(obj=self.auths, fp=file, indent=2)
            file.close()
            return 1
