import aiohttp


class TwitchTV:
    def __init__(self, redis):
        self.apiurl = "https://api.twitch.tv/kraken"
        self.mime_types = {'requests': 'application/vnd.twitchtv.v3+json', 'returns': 'application/json'}
        self.pools = redis
