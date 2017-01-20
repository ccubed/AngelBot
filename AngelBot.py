import asyncio
import importlib
import inspect
import json
import multiprocessing
import sys
import time
import aiohttp
import aioredis
import discord
import re
from datetime import timedelta


class AngelBot(discord.Client):
    def __init__(self, shard, shards, conn):
        super().__init__(loop=None, shard_id=shard, shard_count=shards)
        self.redis = None
        self.btoken = None
        self.creator = None
        self.references = {}
        self.cid = 0
        self.ipc = conn

    async def setup(self):
        self.redis = await aioredis.create_pool(('localhost', 6379), db=1, minsize=1, maxsize=10, encoding="utf-8")
        async with self.redis.get() as dbp:
            modules = await dbp.lrange("BotModules", 0, -1)
            self.btoken = await dbp.get("BotToken")
            self.creator = await dbp.get("Creator")
            self.cid = await dbp.get("DiscordCID")
            for mod in modules:
                globals()[mod] = importlib.import_module(mod)
            for mod in modules:
                self.references[mod] = inspect.getmembers(globals()[mod], inspect.isclass)[0][1](self)
            self.loop.call_later(1500, self.update_stats)

    async def on_message(self, message):
        if message.author.id == self.user.id or message.author.bot:
            return
        elif message.content.lower() == "owlkill" and message.author.id == self.creator:
            await self.redis.clear()
            await self.logout()
            self.ipc.send("QUIT:{}".format(self.shard_id))
        elif self.user in message.mentions:
            if 'info' in message.content.lower():
                await self.send_message(message.channel,
                                        "```AngelBot\nVersion: 3.0\nLibrary: Discord.py with Bootleg Command Ext\nURL: https://angelbot.vertinext.com\nOwner: 66257033204080640\nHelp: http://angelbot.rtfd.org\nServer: https://discord.gg/7uhFnxk\nReport Problems: https://github.com/ccubed/AngelBot```")
            elif 'help' in message.content.lower():
                await self.send_message(message.channel,
                                        "```Usage: @AngelBot [category]\n\nCategory - Description\nconfig   - Help with setting angelbot up\nxivdb    - Help for searching XIVDB\nxkcd     - Help for grabbing XKCD Comics\nanilist  - Help with Anilist Commands\nriot  - Help with the Riot Games commands\now   - Help with the Overwatch commands\ncurrency   - Help with the currency commands\n\nAlso see our documentation at: http://angelbot.rtfd.io```")
            elif 'config' in message.content.lower():
                await self.send_message(message.channel,
                                        "```ardserver prefix:[value] - set this server's command prefix to [value]. The default is $\n\nardserver admin:[list of mentions] - Set the admin to the people mentioned. This is a symmetric difference. That means that if a person is already an admin this will remove them.\n\nardserver modules:[module][=[channels]] - Load a module for your server. Optionally, restrict its commands to the channels specified in the space separated list. If you want it available to all channels leave out that part. For a current list of modules see http://angelbot.readthedocs.io/en/latest/APIs.html```")
            elif 'xivdb' in message.content.lower():
                await self.send_message(message.channel,
                                        '```Remember to put your server prefix before these commands. The default is $.\n\nitem [name or id] - Search for an item by term or item id\nquest [name or id] - Search for a quest by name or id\nrecipe [name or id] - Search for a recipe by name or id\naction [name or id] - Search for an action (Skill) by name or id\nmats [name or id] - Search for a material you gather by name or id\nnpc [name or id] - Search for npc by name or id. I do not recommend this as there is one NPC entry for every position they ever take in the game.\neffect [name or id] - Search for a status effect by name or id\nminion [name or id] - Search for a minion by name or id\nachievement [name or id] - Search for an achievement by name or id\nhdim [name or id] - How do I make thing. Really the same as recipe\nwdif [name or id] - Gives all possible ways of obtaining thing known to xivdb```')
            elif 'xkcd' in message.content.lower():
                await self.send_message(message.channel,
                                        '```Remember to put your server prefix before these commands. The default is $.\n\nxkcd - Grab the latest XKCD comic\nxkcd [number] - Pull a specific XKCD comic```')
            elif 'anilist' in message.content.lower():
                await self.send_message(message.channel,
                                        '```Remember to put your server prefix before these commands. The default is $.\n\naanime [name or id] - Search for an anime. If there is only one result will pull details.\n\nacharacter [name or id] - Search for a character. If there is only one result it will pull details.\n\namanga [name or id] - Search for a manga. If there is only one result it will pull details.\n\nacurrent - Return the top ten most popular currently airing anime\n\nawaifu [name or id] - Declare your love for your waifu. Gonna be honest, due to how search works with anilist works better with id.\n\nahusbando [name or id] - Declare your love for your husbando. Gonna be honest, due to how search works with anilist works better with id.\n\nauser - Requires Oauth. PM the bot about Anilist to do that. Pulls your user details.\n\nauser [name] - Pull another users details.\n\nanotifications - Requires oauth. Pull up to 10 of your pending notifications.\n\napeople [term] - Search for users that match term\n\nafollow [id or name] - oauth required. Follows a user.\n\nanilist [id or name] - Pulls 20 random anime from a persons completed list. If there are 20 or less, pull the entire list.\n\namangalist [id or name] - Pull 20 random manga from a persons completed list. If there are 20 or less, pull the whole list.\n\nawatch [id or name] - Oauth required. Marks an anime as plan to watch in your list.\n\naread [id or name] - oauth required. Marks a manga as plan to read in your list.\n\nanext [a or m]:[id or name] - oauth required. First parameter is a for anime or m for manga. Next is the id or name of what show or manga we are updating. This will mark you up one episode watched. It also handles marking things completed.\n\nawatching [id or name] - pulls 20 random currently watching anime from a users list. If 20 or less its the entire list.\n\nareading [id or name] - pulls 20 random manga from the currently reading list for the user. If 20 or less, its the whole list.```')
            elif 'riot' in message.content.lower():
                await self.send_message(message.channel,
                                        '```Remember to put your server prefix before these commands. The default is $.\n\nislolup - Check the status of the LoL servers in all regions\nlolstatus [region] - Check the status of a specific region. Region should be one of na1, jp1, la1, la2, oc1, eu or eun1.\nlolfree - Display current free rotation\nlolfeatures - Display current featured games. This now supports the BR region. Simply add BR after lolfeatures.\nlolrecent [summoner] - Display a summoners recent games. Summoner can be a name or id. NA and BR only. For BR add BR after summoner name.\nlolstats [summoner] - Display a summary of stats for a summoner. Summoner can be a name or id. NA and BR only. For BR add BR after summoner name.```')
            elif 'ow' in message.content.lower():
                await self.send_message(message.channel,
                                        '```Remember to put your server prefix before these commands. The default is $.\n\now [battletag] - Pull stats for a battletag. EU or US only.\nowheroes [battletag] - Show hero win statistics for a battletag.\nowhero [battletag]:[hero] - Pull stats for a specific hero for a batteltag. I gave the heroes funny names, see if you can guess them. Has to be a hero name, not id.```')
            elif 'currency' in message.content.lower():
                await self.send_message(message.channel,
                                        '```Remember to put your server prefix before these commands. The default is $.\n\ncurrencies - Show a list of currencies available in the data and their identifiers. When using the functions in this module use the identifiers. IE: USD or GBP.\nrates [currency] - Show a list of the latest exchange rates against a given base currency. If a currency is not provided then Euro is the default.\nconvert [amt] [currency] to [other currency] - Convert an amount of currency into another. Amount must be a number but can be prepended by a symbol. Make sure to type this command exactly, the to is important. Not all currency combinations work for some reason.```')
            elif 'oi cunt' in message.content.lower():
                await self.send_message(message.channel, "{} oi, you 'avin a giggle there mate. I'll bash your fooking head in I will.".format(message.author.mention))
            elif 'misc' in message.content.lower():
                await self.send_message(message.channel,
                                        '```Remember to put your server prefix before these commands. The default is $.\n\nroll <x>d<y> <reason> - Roll x dice with y sides for reason. Reason is optional. You can omit x and it will default to 1. y is not optional.')
        elif message.server is None:
            if 'oauth' in message.content.lower():
                await self.send_message(message.author, "Angelbot can use an Oauth flow to connect to your logins on other platforms. This allows Angelbot to take actions it may not otherwise be able to. If you'd like to begin this process, please respond with one of the following providers: github")
            elif 'github' in message.content.lower():
                await self.send_message(message.author, "To begin this process visit the following link:\nhttps://angelbot.vertinext.com/oauth/Github/{0}".format(message.author.id))
            elif 'anilist' in message.content.lower():
                await self.send_message(message.author, "To begin this process visit the following link:\nhttps://angelbot.vertinext.com/oauth/AniList/{0}".format(message.author.id))
            else:
                await self.send_message(message.author, "Assuming you want a join link: https://discordapp.com/oauth2/authorize?client_id={0}&scope=bot&permissions=0".format(self.cid))
        elif message.content.startswith("owl") and message.author.id == self.creator:
            if message.content.lower().startswith("owlavatar"):
                file = message.content[10:]
                try:
                    fstream = open(file, 'rb')
                except IOError:
                    await self.send_message(message.channel, "File not found.")
                else:
                    imgbd = fstream.read()
                    fstream.close()
                    await self.edit_profile(avatar=imgbd)
            elif message.content.lower().startswith("owlgame"):
                await self.change_status(game=discord.Game(name=" ".join(message.content.split(" ")[1:])))
            elif message.content.lower().startswith("owldebug"):
                gist_data = {"description": "AngelBot Debug ran {}".format(time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())),
                             "public": True}
                codeblock = message.content.split("owldebug")[1].strip()
                if '`' in codeblock:
                    codeblock = re.split(self.codeblock_regex, codeblock)[1]
                result = None
                try:
                    result = eval(codeblock)
                    gist_data['files'] = {
                        "input.py": {
                            "content": codeblock
                        },
                        "result.txt": {
                            "content": str(result)
                        }
                    }
                    gist_url = await self.create_gist(gist_data)
                    await self.send_message(message.channel, "Execution of that code was completed.\nSee {}".format(gist_url))
                except SyntaxError:
                    # Get the real error
                    try:
                        exec(codeblock)
                    except Exception as Ex:
                        gist_data['files'] = {
                            "input.py": {
                                "content": codeblock
                            },
                            "Exception.txt": {
                                "content": str(Ex)
                            }
                        }
                        gist_url = await self.create_gist(gist_data)
                        await self.send_message(message.channel, "Execution of that code encountered an error.\nSee {}".format(gist_url))
        elif message.content.startswith("ard"):
            async with self.redis.get() as dbp:
                admin = await dbp.hget(message.server.id, "Admin")
                if admin != "None":
                    if message.author.id in admin.split("|") or message.channel.permissions_for(message.author).manage_server:
                        for command in self.references['Admin'].commands:
                            if message.content.lower().startswith("ard" + command[0]):
                                await command[1](message)
                elif message.channel.permissions_for(message.author).manage_server:
                    # Well they can manage the server so they can manage the bot, deal with it
                    for command in self.references['Admin'].commands:
                        if message.content.lower().startswith("ard" + command[0]):
                            await command[1](message)
        else:
            prefix = "$"
            async with self.redis.get() as dbp:
                test = await dbp.hexists(message.server.id, "Prefix")
                if test:
                    prefix = await dbp.hget(message.server.id, "Prefix")
                for item in self.references:
                    for command in self.references[item].commands:
                        if message.content.lower().startswith(prefix+command[0]):
                            await command[1](message)

    async def on_server_remove(self, server):
        await self.references['Admin'].cleanconfig(server.name)

    async def on_server_join(self, server):
        async with self.redis.get() as dbp:
            await self.references["Admin"].createnewserver(server.id, dbp)
            
    async def create_gist(self, content):
        headers = {'Accept': 'application/vnd.github.v3+json', 'Content-Type': 'application/json'}
        async with self.redis.get() as dbp:
            token = await dbp.get("GitToken")
            headers['Authorization'] = 'Token {}'.format(token)
            async with aiohttp.ClientSession() as sess:
                async with sess.post('https://api.github.com/gists', data=json.dumps(content), headers=headers) as r:
                    if r.status == 201:
                        jsd = await r.json()
                        return jsd['html_url']
                    else:
                        return None

    def update_stats(self):
        self.ipc.send("STATUS:{}:{}:{}".format(self.shard_id, len(self.servers),
                                               sum(x.member_count for x in self.servers if not x.unavailable)))
        self.loop.call_later(1500, self.update_stats)
