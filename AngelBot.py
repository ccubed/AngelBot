import asyncio
import importlib
import inspect
import json
import sys
import aiohttp
import discord



class AngelBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.references = {}
        self.testing = False
        self.token_bucket = {}
        self.modules = ['Admin', 'AList', 'Currency', 'Overwatch', 'Riot', 'XIVDBBOT', 'XKCD']
        self.commands = {}

    async def setup(self):
        for mod in self.modules:
            modref = importlib.import_module(mod)
            self.references[mod] = inspect.getmembers(globals()[mod], inspect.isclass)[0][1]()
            for command in self.references[mod].commands:
                self.commands[command[0]] = command[1]
            if not self.testing:
                self.loop.call_later(1500, self.update_carbon)  # It takes time to chunk
                self.loop.call_soon_threadsafe(self.update_tokens)

    async def on_message(self, message):
        self.commands += 1
        if message.author.id == self.user.id or message.author.bot:
            return
        elif message.content.lower() == "owlkill" and message.author.id == 66257033204080640:
            await self.logout()
        elif message.server is None:
            if 'oauth' in message.content.lower():
                await self.send_message(message.author, "Angelbot can use an Oauth flow to connect to your logins on other platforms. This allows Angelbot to take actions it may not otherwise be able to. If you'd like to begin this process, please respond with one of the following providers: github")
            elif 'github' in message.content.lower():
                await self.send_message(message.author, "To begin this process visit the following link:\nhttps://angelbot.vertinext.com/oauth/Github/{0}".format(message.author.id))
            elif 'anilist' in message.content.lower():
                await self.send_message(message.author, "To begin this process visit the following link:\nhttps://angelbot.vertinext.com/oauth/AniList/{0}".format(message.author.id))
        elif message.content.lower("owlgame") and message.author.id == 66257033204080640:
            await self.change_status(game=discord.Game(name=" ".join(message.content.split(" ")[1:])))
        else:
            prefix = "$"

    def update_carbon(self):
        self.loop.create_task(self._update_carbon())
        self.loop.call_later(3000, self.update_carbon)

    async def _update_carbon(self):
        async with self.redis.get() as dbp:
            ckey = await dbp.get("CarbonKey")
            lbk = await dbp.get("ListBoat")
            servc = len(self.servers)
            with aiohttp.ClientSession() as session:
                async with session.post("https://www.carbonitex.net/discord/data/botdata.php",
                                        data=json.dumps({'key': ckey, 'servercount': servc}),
                                        headers={'Content-Type': 'application/json'}) as resp:
                    print("Carbon: {}".format(resp.status))
                    await resp.release()
                async with session.post("https://bots.discord.pw/api/bots/168925517079248896/stats",
                                        data=json.dumps({'server_count': servc}),
                                        headers={'Authorization': lbk, 'Content-Type': 'application/json'}) as resp:
                    await resp.release()

    def update_tokens(self):
        if len(list(self.token_bucket.keys())) > 0:
            #  We got ratelimits
            self.loop.create_task(self._clear_tokens)
        else:
            #  We ain't got no ratelimits, whatever
            self.loop.call_later(300, self.update_tokens)

    async def _clear_tokens(self):
        tokens = False
        for module in self.token_bucket.keys():
            if time.time() > self.token_bucket[module]['time_to_retry']:
                if self.token_bucket[module]['commands'].qsize() > 0:
                    tokens = True
                    for x in range(0, 4):  # 5 at a time or b1nzy will send me angry pms
                        this_task = await self.token_bucket[module]['commands'].get()
                        ret = await this_task[0](this_task[1])
                        if isinstance(ret, str):
                            await self.send_message(this_task[1].channel, ret)
                        elif isinstance(ret, list):
                            for x in ret:
                                await self.send_message(this_task[1].channel, x)
                        elif isinstance(ret, dict):
                            #  anoooother 429.
                            await self.send_message(this_task[1].channel, "I attempted to process a held command for this channel but hit another ratelimit so I cleared the command. Dang man, them ratelimits.")
                            continue
                else:
                    self.token_bucket.pop(module)
        if tokens:  #  We need to come back and keep clearing
            self.loop.call_later(20, self.update_tokens)


if __name__ == "__main__":
    try:
        bot = AngelBot()
    except ImportError:
        sys.exit(65)

    bot.loop.run_until_complete(bot.setup())

    # Run the bot.
    bot.run(bot.btoken)
