import aiohttp
import json


class GithubApi:
    def __init__(self, redis):
        self.apiurl = "https://api.github.com"
        self.pools = redis

    async def get_oauth(self, id):
        # Return the oauth token for getting user data or raise NotRegistered to indicate the need to initiate oauth flow
        pass
        
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
        