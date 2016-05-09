import aiohttp
import json
from secret import *
from encryption import *


class GithubApi:
    def __init__(self, redis):
        self.apiurl = "https://api.github.com"
        self.pools = redis
        self.header = {'Accept': 'application/vnd.github.v3+json'}
        self.crypt = AESCipher(cryptokey)

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
        # Return number of repos and language statistics. Can be done without oauth.
        pass
        
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
        