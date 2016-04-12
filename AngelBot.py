import discord
import asyncio
import logging
import json
import importlib
import sys
import inspect
import datetime
from types import ModuleType
from Gitapi import *


class AngelBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.reporting = GithubApi()
        # Load config
        file = open("Global_config.json", mode="r")
        self.config = json.load(file)
        file.close()
        # Import modules
        if 'modules' in self.config:
            for mod in self.config['modules']:
                importlib.import_module(mod)
            importlib.invalidate_caches()
        else:
            raise ImportError("No modules defined in the config.")
        # Create classes. Each module should have exactly one class.
        self.references = {}
        for mod in self.config['modules']:
            self.references[mod] = inspect.getmembers(sys.modules[mod], inspect.isclass)[0][1]()

    async def on_message(self, message):
        if message.author == self.config['Discord']['discord_bot_username']:
            return
        elif message.server is None:
            await self.send_message(message.author,
                                    "PMs don't trigger commands. Assuming you want an OAuth link to add to a server.\nhttps://discordapp.com/oauth2/authorize?&client_id={0}&scope=bot&permissions=0".format(
                                        self.config['Discord']['discord_bot_id']))
        else:
            prefix = "$"
            if message.server in self.config['Servers']:
                if 'Prefix' in self.config['Servers'][message.server]:
                    prefix = self.config['Servers'][message.server]['Prefix']
            if 'Modules' in self.config['Servers'][message.server]:
                for item in self.config['Servers'][message.server]['Modules']:
                    if item['channel_lock'] is None or item['channel_lock'] == message.channel:
                        for command in self.references[item['Name']].commands:
                            if message.content.lower().startswith(prefix + command[0]):
                                if item['Name'] == "Code" and message.author != self.config['Creator']:
                                    await self.send_message(message.author, "Only the coder can hotload code.")
                                    return
                                else:
                                    ret = command[1](message)
                                    if isinstance(ret, str):
                                        await self.send_message(message.channel, ret)
                                    elif isinstance(ret, ModuleType):
                                        self.references[item['Name']] = inspect.getmembers(sys.modules[item['Name']],
                                                                                           inspect.isclass)[0][1]()
                                        await self.send_message(message.channel,
                                                                "Hotloaded module {0}".format(item['Name']))
                                    else:
                                        now = datetime.now()
                                        repret = self.reporting.createissue("Incorrect Type Returned",
                                                                            "Encountered an error at {0} while attempted to run a command in {1} based on the command string {2}.\nType: {3}\nError: Type should be str or module".format(
                                                                                repr(now), item['Name'],
                                                                                message.content,
                                                                                type(ret)))
                                        if repret == 0:
                                            await self.send_message(self.config['Creator'],
                                                                    "I wasn't able to create a github issue for an error at {0}".format(
                                                                        repr(now)))
                                            await self.send_message(message.channel,
                                                                    "I encountered an error. I was unable to automatically log an issue in github for it. I've informed my creator {0} by DM.".format(
                                                                        self.config['Creator']))
                                        else:
                                            await self.send_message(message.channel,
                                                                    "Sorry, I encountered an error. I was able to create an automatic github issue for it though. See it here.\n{0}".format(
                                                                        repret))
            else:
                for item in self.references:
                    for command in item.commands:
                        if message.content.lower().startswith(prefix + command[0]):
                            if item['Name'] == "Code" and message.author != self.config['Creator']:
                                await self.send_message(message.channel, "Only the coder can hotload code.")
                                return
                            else:
                                ret = command[1](message)
                                if isinstance(ret, str):
                                    await self.send_message(message.channel, ret)
                                elif isinstance(ret, ModuleType):
                                    self.references[item['Name']] = inspect.getmembers(sys.modules[item['Name']],
                                                                                       inspect.isclass)[0][1]()
                                    await self.send_message(message.channel,
                                                            "Hotloaded module {0}".format(item['Name']))
                                else:
                                    now = datetime.now()
                                    repret = self.reporting.createissue("Incorrect Type Returned",
                                                                        "Encountered an error at {0} while attempted to run a command in {1} based on the command string {2}.\nType: {3}\nError: Type should be str or module".format(
                                                                            repr(now), item['Name'],
                                                                            message.content,
                                                                            type(ret)))
                                    if repret == 0:
                                        await self.send_message(self.config['Creator'],
                                                                "I wasn't able to create a github issue for an error at {0}".format(
                                                                    repr(now)))
                                        await self.send_message(message.channel,
                                                                "I encountered an error. I was unable to automatically log an issue in github for it. I've informed my creator {0} by DM.".format(
                                                                    self.config['Creator']))
                                    else:
                                        await self.send_message(message.channel,
                                                                "Sorry, I encountered an error. I was able to create an automatic github issue for it though. See it here.\n{0}".format(
                                                                    repret))

    async def on_ready(self):
        return


try:
    bot = AngelBot()
except ImportError:
    sys.exit(65)

# Setup logger
log = logging.getLogger()
log.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="angel.log", encoding="utf-8", mode="a")
log.addHandler(handler)

# Run the bot.
bot.run(bot.config['Discord']['discord_bot_token'])

# Close handlers.
handlers = log.handlers[:]
for item in handlers:
    item.close()
    log.removeHandler(item)

# Dump the config.
file = open("Global_config.json", mode="w")
json.dump(obj=self.config, fp=file, indent=2)
file.close()

# Call the exit methods of the modules currently Loaded. These should return 1.
for cls in bot.references:
    if bot.references[cls].exit() == 0:
        print("{0} didn't close correctly.".format(cls))
