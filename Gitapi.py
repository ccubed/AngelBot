import aiohttp
import json
from secret import *
import encryption


class GithubApi:
    def __init__(self, redis):
        self.apiurl = "https://api.github.com"
        self.pools = redis
        self.header = {'Accept': 'application/vnd.github.v3+json', 'User-Agent': 'AngelBot (Github User CCubed)'}
        self.crypt = encryption.AESCipher(cryptokey)
        self.commands = [['gitinfo', self.get_user_info]]
        self.auth_limit = 5000

    async def get_oauth(self, id):
        # Return the oauth token for getting user data or pm the oauth link and instructions
        async with self.pools.get() as dbp:
            if await dbp.hexists(id, "Github_Token"):
                base = dbp.hget(id, "Github_Token")
                final = self.crypt.decrypt(base)
                return final
            else:
                return 0

    async def get_ids(self):
        async with self.pools.get() as dbp:
            a = await dbp.hget("Github", "ClientID")
            b = await dbp.hget("Github", "ClientSecret")
            return {'client_id': a, 'client_secret': b}

    # Todo: Rewrite this a third time.
    async def get_user_info(self, message):
        async with self.pools.get() as dbp:
            jsd = 0
            headers = self.header
            if len(message.content) > 8:
                name = message.content[9:0]
                test = await dbp.hget("GIT" + name, "etag")
                params = await self.get_ids()
                if test is not None and test != 0: #TODO: We have an etag, we can make a If-None-Match query
                    headers['If-None-Match'] = test
                else:  # TODO: No etag, we have to do a poll of the api and get initial data
            else: #TODO: No name passed, use user's oauth id
                key = await self.get_oauth(message.author.id)
                if key == 0:
                    return "You need to authenticate your account with Github and allow AngelBot access. PM AngelBot about Oauth to start."
                else: #TODO: Valid authorization key, use it
                    headers['Authorization'] = 'token {0}'.format(key)
                    test = await dbp.hget("GIT" + message.author.id, "etag")
                    if test is not None and test != 0: #TODO: We have an etag, we can make a If-None-Match query
                        headers['If-None-Match'] = test
                    else: #TODO: No etag, we have to do a poll of the api and get initial data

    async def list_gists(self, message):
        # Return gist info. Requires Oauth.
        pass

    async def get_gist(self, message):
        # Return a gist. If the gist is truncated, will return a link to that gist. If not, returns the code of that gist in a discord code block. Oauth required.
        pass

    async def repo_info(self, message):
        # Return info on a repo. Can be done without oauth.
        pass

    async def create_issue(self, message):
        # Create an issue on a repo. Needs Oauth.
        pass

    async def search_code(self, message):
        # Find instance of thing in code. Requires Oauth
        pass
