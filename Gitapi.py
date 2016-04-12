import requests
import json


class GithubApi:
    def __init__(self):
        self.apiurl = "https://api.github.com"
        file = open("Global_config.json", mode="r")
        self.config = json.load(file)
        file.close()

    def createissue(self, title, body):
        url = self.apiurl + "/repos/ccubed/AngelBot/issues"
        payload = {'title': title, 'body': body, lables: ['AngelBot']}
        headers = {'Authorization': 'token ' + self.config['GitToken']}
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 201:
            return response.json()['url']
        else:
            return 0

    def exit(self):
        return 1
