import asyncio
import logging
import importlib
import inspect
import sys
import json
import aiohttp
import aioredis
import discord
import time
from datetime import timedelta
from types import ModuleType



class AngelBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.uptime = time.time()
        self.commands = 0
        self.redis = None
        self.btoken = None
        self.creator = None
        self.references = {}
        self.testing = False
        self.token_bucket = {}

    async def setup(self):
        self.redis = await aioredis.create_pool(('localhost', 6379), db=1, minsize=1, maxsize=10, encoding="utf-8")
        async with self.redis.get() as dbp:
            modules = await dbp.lrange("BotModules", 0, -1)
            self.btoken = await dbp.get("BotToken")
            self.creator = await dbp.get("Creator")
            for mod in modules:
                globals()[mod] = importlib.import_module(mod)
            for mod in modules:
                self.references[mod] = inspect.getmembers(globals()[mod], inspect.isclass)[0][1](self.redis)
            for mod in self.references:
                if 'events' in self.references[mod].__dict__:
                    for event in self.references[mod].events:
                        if event[1] == 0:
                            self.loop.call_soon_threadsafe(event[0], self.loop)
                        else:
                            self.loop.call_later(event[1], event[0], self.loop)
            if not self.testing:
                self.loop.call_soon_threadsafe(self.update_stats)
                self.loop.call_soon_threadsafe(self.update_carbon)
                self.loop.call_soon_threadsafe(self.update_tokens)

    async def on_message(self, message):
        self.commands += 1
        if message.author.id == self.user.id or message.author.bot:
            return
        elif message.content.lower() == "owlkill" and message.author.id == self.creator:
            await self.redis.clear()
            await self.logout()
        elif self.user in message.mentions:
            if 'info' in message.content:
                await self.send_message(message.channel,
                                        "```AngelBot\nVersion: 2.0\nLibrary: Discord.py\nURL: https://angelbot.vertinext.com\nOwner: 66257033204080640\nHelp: http://angelbot.rtfd.org\nServer: https://discord.gg/0wjevYU2RBlo7JpF```")
            elif 'help' in message.content:
                await self.send_message(message.channel,
                                        "```Usage: @AngelBot [category]\n\nCategory - Description\nconfig   - Help with setting angelbot up\nxivdb    - Help for searching XIVDB\nxkcd     - Help for grabbing XKCD Comics\nanilist  - Help with Anilist Commands\nriot  - Help with the Riot Games commands\n\nAlso see our documentation at: http://angelbot.rtfd.io```")
            elif 'config' in message.content:
                await self.send_message(message.channel,
                                        "```ardserver prefix:[value] - set this server's command prefix to [value]. The default is $\n\nardserver admin:[list of mentions] - Set the admin to the people mentioned. This is a symmetric difference. That means that if a person is already an admin this will remove them.\n\nardserver modules:[module][=[channels]] - Load a module for your server. Optionally, restrict its commands to the channels specified in the space separated list. If you want it available to all channels leave out that part. For a current list of modules see http://angelbot.readthedocs.io/en/latest/APIs.html```")
            elif 'xivdb' in message.content:
                await self.send_message(message.channel,
                                        '```Remember to put your server prefix before these commands. The default is $.\n\nsearch [term] - Search for term across all categories.\nitem [name or id] - Search for an item by term or item id\nquest [name or id] - Search for a quest by name or id\nrecipe [name or id] - Search for a recipe by name or id\naction [name or id] - Search for an action (Skill) by name or id\nmats [name or id] - Search for a material you gather by name or id\nnpc [name or id] - Search for npc by name or id. I do not recommend this as there is one NPC entry for every position they ever take in the game.\neffect [name or id] - Search for a status effect by name or id\nminion [name or id] - Search for a minion by name or id\nachievement [name or id] - Search for an achievement by name or id\nhdim [name or id] - How do I make thing. Really the same as recipe\nwdif [name or id] - Gives all possible ways of obtaining thing known to xivdb```')
            elif 'xkcd' in message.content:
                await self.send_message(message.channel,
                                        '```Remember to put your server prefix before these commands. The default is $.\n\nxkcd - Grab the latest XKCD comic\nxkcd [number] - Pull a specific XKCD comic```')
            elif 'anilist' in message.content:
                await self.send_message(message.channel,
                                        '```Remember to put your server prefix before these commands. The default is $.\n\naanime [name or id] - Search for an anime. If there is only one result will pull details.\n\nacharacter [name or id] - Search for a character. If there is only one result it will pull details.\n\namanga [name or id] - Search for a manga. If there is only one result it will pull details.\n\nacurrent - Return the top ten most popular currently airing anime\n\nawaifu [name or id] - Declare your love for your waifu. Gonna be honest, due to how search works with anilist works better with id.\n\nahusbando [name or id] - Declare your love for your husbando. Gonna be honest, due to how search works with anilist works better with id.\n\nauser - Requires Oauth. PM the bot about Anilist to do that. Pulls your user details.\n\nauser [name] - Pull another users details.\n\nanotifications - Requires oauth. Pull up to 10 of your pending notifications.\n\napeople [term] - Search for users that match term\n\nafollow [id or name] - oauth required. Follows a user.\n\nanilist [id or name] - Pulls 20 random anime from a persons completed list. If there are 20 or less, pull the entire list.\n\namangalist [id or name] - Pull 20 random manga from a persons completed list. If there are 20 or less, pull the whole list.\n\nawatch [id or name] - Oauth required. Marks an anime as plan to watch in your list.\n\naread [id or name] - oauth required. Marks a manga as plan to read in your list.\n\nanext [a or m]:[id or name] - oauth required. First parameter is a for anime or m for manga. Next is the id or name of what show or manga we are updating. This will mark you up one episode watched. It also handles marking things completed.\n\nawatching [id or name] - pulls 20 random currently watching anime from a users list. If 20 or less its the entire list.\n\nareading [id or name] - pulls 20 random manga from the currently reading list for the user. If 20 or less, its the whole list.```')
            elif 'riot' in message.content:
                await self.send_message(message.channel,
                                        '```Remember to put your server prefix before these commands. The default is $.\n\nislolup - Check the status of the LoL servers in all regions\nlolstatus [region] - Check the status of a specific region. Region should be one of na1, jp1, la1, la2, oc1, eu or eun1.\nlolfree - Display current free rotation\nlolfeatures - Display current featured games\nlolrecent [summoner] - Display a summoners recent games. Summoner can be a name or id. NA only.\nlolstats [summoner] - Display a summary of stats for a summoner. Summoner can be a name or id. NA only.```')
        elif message.server is None:
            if 'oauth' in message.content.lower():
                await self.send_message(message.author, "Angelbot can use an Oauth flow to connect to your logins on other platforms. This allows Angelbot to take actions it may not otherwise be able to. If you'd like to begin this process, please respond with one of the following providers: github")
            elif 'github' in message.content.lower():
                await self.send_message(message.author, "To begin this process visit the following link:\nhttps://angelbot.vertinext.com/oauth/Github/{0}".format(message.author.id))
            elif 'anilist' in message.content.lower():
                await self.send_message(message.author, "To begin this process visit the following link:\nhttps://angelbot.vertinext.com/oauth/AniList/{0}".format(message.author.id))
            else:
                async with self.redis.get() as dbp:
                    cid = dbp.get("DiscordCID")
                    await self.send_message(message.author, "Assuming you want a join link: https://discordapp.com/oauth2/authorize?client_id={0}&scope=bot&permissions=0".format(cid))
        elif message.content.startswith("owl") and message.author.id == self.creator:
            if message.content.lower().startswith("owldebug"):
                    # Rewrite this whole thing to be able to await things seriously
                    await self.send_message(message.channel, eval(message.content[9:]))
            elif message.content.lower().startswith("owlhotload"):
                ret = self.references['Code'].hotload(message)
                if isinstance(ret, str):
                    await self.send_message(message.channel, ret)
                elif isinstance(ret, ModuleType):
                    self.references[message.content[11:]] = inspect.getmembers(ret, inspect.isclass)[0][1]()
                    await self.send_message(message.channel, "Hotloaded Module {0}.".format(message.content[11:]))
                else:
                    await self.send_message(message.channel, "Lol what?")
            elif message.content.lower().startswith("owlstats"):
                up = str(timedelta(seconds=(time.time() - self.uptime))).split(".")[0]
                await self.send_message(message.channel,
                                        "```AngelBot Statistics\n{} Servers\n{} Users\nUptime: {}\n{} commands total\n{:.1f} commands a second```".format(
                                            len(self.servers), sum(x.member_count for x in self.servers), str(up), self.commands, self.commands/up.total_seconds()))
            elif message.content.lower().startswith("owlavatar"):
                file = message.content[10:]
                try:
                    fstream = open(file, 'rb')
                except IOError:
                    await self.send_message(message.channel, "File not found.")
                    return
                else:
                    imgbd = fstream.read()
                    fstream.close()
                    await self.edit_profile(avatar=imgbd)
            elif message.content.lower().startswith("owlgame"):
                await self.change_status(game=discord.Game(name=" ".join(message.content.split(" ")[1:])))
        elif message.content.startswith("ard"):
            async with self.redis.get() as dbp:
                admin = await dbp.hget(message.server.id, "Admin")
                if admin != "None":
                    if message.author.id in admin.split("|") or message.channel.permissions_for(message.author).manage_server:
                        for command in self.references['Admin'].commands:
                            if message.content.lower().startswith("ard" + command[0]):
                                ret = await command[1](message)
                                await self.send_message(message.channel, ret)
                                return
                elif message.channel.permissions_for(message.author).manage_server:
                    # Well they can manage the server so they can manage the bot, deal with it
                    for command in self.references['Admin'].commands:
                        if message.content.lower().startswith("ard" + command[0]):
                            ret = await command[1](message)
                            await self.send_message(message.channel, ret)
                            return
        else:
            prefix = "$"
            async with self.redis.get() as dbp:
                test = await dbp.hexists(message.server.id, "Prefix")
                if test:
                    prefix = await dbp.hget(message.server.id, "Prefix")
                mods = await dbp.hgetall(message.server.id+"_Modules")
                for item in mods.keys():
                    if mods[item] == "None" or message.channel.name in mods[item].split("|"):
                        check = message.content.split(" ")[0].lower()
                        for command in self.references[item].commands:
                            if check == prefix + command[0]:
                                ret = await command[1](message)
                                if isinstance(ret, dict):
                                    if ret['module'] in self.token_bucket:
                                        await self.token_bucket[ret['module']]['commands'].put([ret['command'], ret['message']])
                                        self.token_bucket[ret['module']]['servers'][ret['message'].server.id] = True
                                        if self.token_bucket[ret['module']]['time_to_retry'] > ret['time_to_retry']:
                                            self.token_bucket[ret['module']]['time_to_retry'] = ret['time_to_retry']
                                        await self.send_message(ret['message'].server.id, "Oh no, we done got ratelimited! Please wait {}. Messages will automatically process then.".format(timedelta(seconds=self.token_bucket[ret['module']]['time_to_rety'])))
                                    else:
                                        self.token_bucket[ret['module']] = {'servers': {ret['message'].server.id: True},
                                                                            'time_to_retry': ret['time_to_retry']}
                                        self.token_bucket[ret['module']]['commands'] = asyncio.Queue(loop=self.loop)
                                        await self.token_bucket[ret['module']]['commands'].put([ret['command'], ret['message']])
                                        await self.send_message(ret['message'].server.id, "Oh no, we done got ratelimited! Please wait {}. Messages will automatically process then.".format(timedelta(seconds=ret['time_to_rety'])))
                                elif isinstance(ret, list):
                                    for retstring in ret:
                                        if len(retstring) > 2000:
                                            logger.warning("Item was more than 2000 characters. Skipped.")
                                            return
                                        else:
                                            await self.send_message(message.channel, retstring)
                                else:
                                    if len(ret) > 2000:
                                        logger.warning("Item was more than 2000 characters. Skipped.")
                                        return
                                    else:
                                        await self.send_message(message.channel, ret)

    # We need to clean settings and Oauth on server remove for security
    async def on_server_remove(self, server):
        await self.references['Admin'].cleanconfig(server.name)

    async def on_server_join(self, server):
        async with self.redis.get() as dbp:
            await self.references["Admin"].createnewserver(server.id, dbp)

    async def on_ready(self):
        return

    def update_carbon(self):
        self.loop.create_task(self._update_carbon())
        self.loop.call_later(3000, self.update_carbon)

    async def _update_carbon(self):
        async with self.redis.get() as dbp:
            ckey = await dbp.get("CarbonKey")
            data = {'key': ckey, 'servercount': len(self.servers)}
            with aiohttp.ClientSession() as session:
                async with session.post("https://www.carbonitex.net/discord/data/botdata.php", data=json.dumps(data)) as resp:
                    await resp.release()

    def update_stats(self):
        stats = {}
        stats['uptime'] = time.time() - self.uptime
        stats['users'] = sum(x.member_count for x in self.servers)
        stats['servers'] = len(self.servers)
        stats['cmdssec'] = '{:.1f}'.format(self.commands/stats['uptime'])
        stats['totalcmds'] = self.commands
        self.loop.create_task(self._update_stats(stats))
        self.loop.call_later(900, self.update_stats)

    async def _update_stats(self, stats):
        async with self.redis.get() as dbp:
            await dbp.hset('stats', 'uptime', stats['uptime'])
            await dbp.hset('stats', 'users', stats['users'])
            await dbp.hset('stats', 'servers', stats['servers'])
            await dbp.hset('stats', 'cmdssec', stats['cmdssec'])
            await dbp.hset('stats', 'totalcmds', stats['totalcmds'])

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
                    for x in range(0,4):  #  5 at a time or b1nzy will send me angry pms
                        this_task = await self.token_bucket[module]['commands'].get()
                        ret = await this_task[0](this_task[1])
                        if isinstance(ret, str):
                            await self.send_message(this_task[1].channel, ret)
                        elif isinstance(ret, list):
                            for x in ret:
                                await self.send_message(this_task[1].channel, x)
                        elif isinstance(ret, dict):
                            #  anoooother 429.
                            logger.critical("Got another 429 while processing command {} after ratelimit wait.".format(this_task[1].content))
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

    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='/home/gizmo/AngelBot/GExitLogs/{0}'.format(time.time()), encoding="utf-8", mode="w")
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    bot.loop.run_until_complete(bot.setup())

    # Run the bot.
    bot.run(bot.btoken)
