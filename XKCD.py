import aiohttp


class XKCD:
    def __init__(self, client):
        self.apiurl = "http://xkcd.com/"
        self.commands = [['xkcd', self.getxkcd]]
        self.bot = client

    async def getxkcd(self, message):
        if len(message.content.strip()) == 5:
            url = self.apiurl + "info.0.json"
            with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    jsd = await response.json()
                    await self.bot.send_message(message.channel, "{0}\nAlt: {1}\n{2}".format(jsd['safe_title'], jsd['alt'], jsd['img']))
        else:
            id = message.content[6:]
            url = self.apiurl + id + "/info.0.json"
            with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    jsd = await response.json()
                    await self.bot.send_message(message.channel, "{0}\nAlt: {1}\n{2}".format(jsd['safe_title'], jsd['alt'], jsd['img']))
