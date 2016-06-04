import asyncio
import logging
import importlib
import inspect
import sys
import json
import aiohttp
import aioredis
import discord
from datetime import *
from types import ModuleType


class AngelBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.uptime = datetime.now()
        self.commands = 0
        self.redis = None
        self.btoken = None
        self.creator = None
        self.references = {}
        self.testing = False

    async def setup(self):
        self.redis = await aioredis.create_pool(('localhost', 6379), db=1, minsize=5, maxsize=10, encoding="utf-8")
        async with self.redis.get() as dbp:
            modules = await dbp.lrange("BotModules", 0, -1)
            self.btoken = await dbp.get("BotToken")
            self.creator = await dbp.get("Creator")
            for mod in modules:
                importlib.import_module(mod)
                importlib.invalidate_caches()
            for mod in modules:
                self.references[mod] = inspect.getmembers(sys.modules[mod], inspect.isclass)[0][1](self.redis)
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

    async def on_message(self, message):
        self.commands += 1
        if message.author.id == self.user.id:
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
                                        "```AngelBot has a lot of modules that interact with a lot of APIs. Having a list of commands in Discord is unrealistic. See:\nhttp://angelbot.rtfd.org```")
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
                if "|" in message.content:
                    context = message.content[9:].split("|")[0]
                    code = message.content[9:].split("|")[1]
                    if context not in self.references:
                        return "I couldn't find context {0} in loaded contexts. Perhaps you need to hotload it first?".format(
                            context)
                    else:
                        context_loaded = self.references[context]
                        check = code.split("(")[0]
                        if " " in check:
                            check = check.split(" ")[-1:]
                        for item in context_loaded.commands:
                            if item[0] == check:
                                if '_is_coroutine' in item[1].__dict__:
                                    result = await eval(code, globals(), context_loaded.__dict__)
                        else:
                            result = eval(code, globals(), context_loaded.__dict__)
                        await self.send_message(message.channel, result)
                else:
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
                up = datetime.now() - self.uptime
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
                    fstream = fstream.read()
                    fstream.close()
                    await self.edit_profile(avatar=fstream)
            elif message.content.lower().startswith("owlgame"):
                await self.change_status(game=discord.Game(name=message.content[8:]))
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
                        check = message.content.split(" ")[0]
                        for command in self.references[item].commands:
                            if check == prefix + command[0]:
                                ret = await command[1](message)
                                if isinstance(ret, list):
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
        stats['uptime'] = datetime.now() - self.uptime
        stats['users'] = sum(x.member_count for x in self.servers)
        stats['servers'] = len(self.servers)
        stats['cmdssec'] = '{:.1f}'.format(self.commands/stats['uptime'].total_seconds())
        stats['totalcmds'] = self.commands
        self.loop.create_task(self._update_stats(stats))
        self.loop.call_later(900, self.update_stats)

    async def _update_stats(self, stats):
        async with self.redis.get() as dbp:
            await dbp.hset('stats', 'uptime', stats['uptime'].total_seconds())
            await dbp.hset('stats', 'users', stats['users'])
            await dbp.hset('stats', 'servers', stats['servers'])
            await dbp.hset('stats', 'cmdssec', stats['cmdssec'])
            await dbp.hset('stats', 'totalcmds', stats['totalcmds'])


if __name__ == "__main__":
    try:
        bot = AngelBot()
    except ImportError:
        sys.exit(65)

    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='/home/gizmo/AngelBot/GExitLogs/{0}'.format(str(datetime.now()).replace(" ", "_")), encoding="utf-8", mode="w")
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    bot.loop.run_until_complete(bot.setup())

    # Run the bot.
    bot.run(bot.btoken)