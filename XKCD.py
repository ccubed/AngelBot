import aiohttp


class XKCD:
    def __init__(self, redis):
        self.apiurl = "http://xkcd.com/"
        self.commands = [['xkcd', self.getxkcd]]

    async def getxkcd(self, message):
        if len(message.content.strip()) == 5:
            url = self.apiurl + "info.0.json"
            with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    jsd = await response.json()
                    return "{0}\nAlt: {1}\n{2}".format(jsd['safe_title'], jsd['alt'],
                                                       jsd['img'])
        else:
            id = message.content[6:]
            url = self.apiurl + id + "/info.0.json"
            with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    jsd = await response.json()
                    return "{0}\nAlt: {1}\n{2}".format(jsd['safe_title'], jsd['alt'],
                                                       jsd['img'])
