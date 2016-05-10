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
        self.unauth_limit = 60
        self.auth_limit = 5000
        self.events = [[self.update_auths, 3600]]

    def update_auths(self, loop):
        self.unauth_limit = 60
        self.auth_limit = 5000
        loop.call_later(3600, self.update_auths, loop)

    async def get_oauth(self, id):
        # Return the oauth token for getting user data or pm the oauth link and instructions
        async with self.pools.get() as dbp:
            if await dbp.hexists(id, "Github_Token"):
                base = dbp.hget(id, "Github_Token")
                final = self.crypt.decrypt(base)
                return final
            else:
                return 0

    async def get_user_info(self, message):
        name = message.content[9:]
        url = self.apiurl + "/users/{0}".format(name)
        async with self.pools.get() as dbp:
            if await dbp.exists(name):
                jsd = await dbp.get("GIT" + name)
                if jsd == "404":
                    return "User {0} not found on github.".format(name)
                else:
                    jsd = json.loads(jsd)
                    return "Username: {0}\nUrl: {1}\nLocation: {2}\nRepos: {3}\nGists: {4}\nFollowers: {5}\nFollowing: {6}".format(
                        jsd['login'], jsd['html_url'], jsd['location'], jsd['public_repos'], jsd['public_gists'],
                        jsd['followers'], jsd['following'])
            elif self.unauth_limit == 0:
                if self.auth_limit > 1000:
                    cid = await dbp.hget("Github", "ClientID")
                    csec = await dbp.hget("Github", "ClientSecret")
                    with aiohttp.ClientSession() as session:
                        async with session.get(url, params={'client_id': cid, 'client_secret': csec}) as response:
                            if response == "404":
                                await dbp.set("GIT" + name, "404")
                                return "User {0} not found on github.".format(name)
                            else:
                                jsd = await response.json()
                                jsd = json.loads(jsd)
                                await dbp.set("GIT"+name, json.dumps(jsd))
                                await dbp.expire("GIT"+name, 36000)
                                return "Username: {0}\nUrl: {1}\nLocation: {2}\nRepos: {3}\nGists: {4}\nFollowers: {5}\nFollowing: {6}".format(
                                    jsd['login'], jsd['html_url'], jsd['location'], jsd['public_repos'],
                                    jsd['public_gists'], jsd['followers'], jsd['following'])
                else:
                    return "The bot has reached the limit on user requests and didn't find a cached result for this name."
            else:
                self.unauth_limit -= 1
                with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=self.header) as response:
                        if response.status == 404:
                            await dbp.set("GIT" + name, "404")
                            await dbp.expire("GIT" + name, 36000)
                            return "User {0} not found on github.".format(name)
                        else:
                            jsd = await response.json()
                            await dbp.set("GIT" + name, json.dumps(jsd))
                            await dbp.expire("GIT" + name, 36000)
                            return "Username: {0}\nUrl: {1}\nLocation: {2}\nRepos: {3}\nGists: {4}\nFollowers: {5}\nFollowing: {6}".format(
                                jsd['login'], jsd['html_url'], jsd['location'], jsd['public_repos'],
                                jsd['public_gists'], jsd['followers'], jsd['following'])

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
