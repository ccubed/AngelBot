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
                                        "```AngelBot\nVersion: 1.0\nLibrary: Discord.py\nURL: https://angelbot.vertinext.com\nOwner: Rory#6028\nHelp: http://angelbot.rtfd.org```")
            elif 'help' in message.content:
                await self.send_message(message.channel,
                                        "```AngelBot has a lot of modules that interact with a lot of APIs. Having a list of commands in Discord is unrealistic. See:\nhttp://angelbot.rtfd.org```")
        elif message.server is None:
            async with self.redis.get() as dbp:
                did = await dbp.get("DiscordCID")
                await self.send_message(message.author,
                                        "PMs don't trigger commands. Assuming you want an OAuth link to add to a server.\nhttps://discordapp.com/oauth2/authorize?&client_id={0}&scope=bot&permissions=0".format(
                                            did))
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
                delta = datetime.now() - self.uptime
                servers = len(self.servers)
                users = 0
                for item in self.servers:
                    users += len(item.members)
                await self.send_message(message.channel,
                                        "```\nAngelBot has been connected to {0} Servers and {1} Users for {2}\nI've processed {3} commands over that time.```".format(
                                            servers, users, delta, self.commands))
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
                    if str(message.author) in admin.split("|"):
                        for command in self.references['Admin'].commands:
                            if message.content.lower().startswith("ard" + command[0]):
                                ret = await command[1](message)
                                await self.send_message(message.channel, ret)
                                return
                elif message.author == message.server.owner:
                    # Obviously the server owner can manage the bot
                    for command in self.references['Admin'].commands:
                        if message.content.lower().startswith("ard" + command[0]):
                            ret = await command[1](message)
                            await self.send_message(message.channel, ret)
                            return
                elif message.channel.permissions_for(message.author).kick_members:
                    # Well they can manage the server so they can manage the bot, deal with it
                    for command in self.references['Admin'].commands:
                        if message.content.lower().startswith("ard" + command[0]):
                            ret = await command[1](message)
                            await self.send_message(message.channel, ret)
                            return
        else:
            prefix = "$"
            async with self.redis.get() as dbp:
                prefix = await dbp.hget(message.server.id, "Prefix")
                mods = await dbp.hgetall(message.server.id+"_Modules")
                for item in mods.keys():
                    if mods[item] == "None" or message.channel.name in mods[item].split("|"):
                        for command in self.references[item].commands:
                            if message.content.lower().startswith(prefix + command[0]):
                                ret = await command[1](message)
                                await self.send_message(message.channel, ret)
                                return

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