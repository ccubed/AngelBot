import discord
import asyncio
import logging
import importlib
import sys
import inspect
import json
from datetime import *
from types import ModuleType
from Gitapi import *


class AngelBot(discord.Client):
    def __init__(self):
        super().__init__()
        with open("Global_config.json", mode="r") as cfg:
            self.config = json.load(cfg)
        self.reporting = GithubApi()
        # Import modules
        if 'Modules' in self.config:
            for mod in self.config['Modules']:
                importlib.import_module(mod)
            importlib.invalidate_caches()
        else:
            raise ImportError("No modules defined in the config.")
        # Create classes. Each module should have exactly one class.
        self.references = {}
        for mod in self.config['Modules']:
            self.references[mod] = inspect.getmembers(sys.modules[mod], inspect.isclass)[0][1]()

    async def on_message(self, message):
        if str(message.author) == self.config['Discord']['discord_bot_username']:
            return
        elif message.content.lower() == "@kill":
            await self.logout()
        elif message.server is None:
            await self.send_message(message.author,
                                    "PMs don't trigger commands. Assuming you want an OAuth link to add to a server.\nhttps://discordapp.com/oauth2/authorize?&client_id={0}&scope=bot&permissions=0".format(
                                        self.config['Discord']['discord_client']))
        elif message.content.startswith("#"):
            if message.content.lower().startswith("#debug"):
                ret = await self.references['Code'].debug(message)
                await self.send_message(message.channel, ret)
            elif message.content.lower().startswith("#hotload"):
                ret = self.references['Code'].hotload(message)
                if isinstance(ret, str):
                    await self.send_message(message.channel, ret)
                elif isinstance(ret, ModuleType):
                    self.references[message.content[8:]] = ret
                    await self.send_message(message.channel, "Hotloaded Module {0}.".format(message.content[8:]))
                else:
                    repret = self.reporting.createissue("Hotloading Returned Something Weird",
                                                        "Hotloading the module {0} returned a {1}.".format(
                                                            message.content[8:], type(ret)))
                    if repret == 0:
                        await self.send_message(message.channel,
                                                "Well I couldn't hotload {0} and I couldn't create an error report.".format(
                                                    message.content[8:]))
                    else:
                        await self.send_message(message.channel,
                                                "Hotloading module {0} didn't work. Created an error report at:\n{1}".format(
                                                    message.content[8:], repret))
            elif message.content.lower().startswith("#reload"):
                ret = self.references['Code'].reload(message)
                if isinstance(ret, str):
                    await self.send_message(message.channel, ret)
                elif isinstance(ret, ModuleType):
                    self.references[message.content[8:]] = ret
                    await self.send_message(message.channel, "Reloaded Module {0}.".format(message.content[8:]))
                else:
                    repret = self.reporting.createissue("Reloading Returned Something Weird",
                                                        "Reloading the module {0} returned a {1}.".format(
                                                            message.content[8:],
                                                            type(ret)))
                    if repret == 0:
                        await self.send_message(message.channel,
                                                "Well I couldn't reload {0} and I couldn't create an error report.".format(
                                                    message.content[8:]))
                    else:
                        await self.send_message(message.channel,
                                                "Reloading module {0} didn't work. Created an error report at:\n{1}".format(
                                                    message.content[8:], repret))
        elif message.content.startswith("@"):
            if message.server.name in self.config['Servers']:
                if str(message.author) in self.config['Servers']['Admin']:
                    for command in self.references['Admin'].commands:
                        if message.content.lower().startswith("@" + command[0]):
                            if command[0] == "server":
                                ret = await command[1](message)
                            else:
                                ret = command[1](message)
                            if isinstance(ret, str):
                                await self.send_message(message.author,
                                                        ret)  # Only for leave, it reports successful leave
                            elif isinstance(ret, dict):
                                self.config = ret  # We got returned updated settings
                            else:
                                # Don't know what the fuck we got, but it's wrong
                                now = datetime.now()
                                repret = self.reporting.createissue("Unexpected Return Type",
                                                                    "I encountered an error while attempting to run a command on {0} from the {1} module using the string {2}.\nType: {3}\nError: Wrong Type".format(
                                                                        now, "Admin", message.content, type(ret)))
                                if repret == 0:
                                    await self.send_message(message.channel,
                                                            "I encountered an error while attempting to run your command and was unable to create a github issue for it. I have informed my creator {0} by DM.".format(
                                                                self.config['Creator']))
                                    await self.send_message(self.config['Creator'],
                                                            "I couldn't create a github ticket for an issue on {0}".format(
                                                                now))
                                else:
                                    await self.send_message(message.channel,
                                                            "I encountered an error while attempting to run your command but was able to create a github issue for it. You can view it here:\n{0}".format(
                                                                repret))
                            break
                else:
                    await self.send_message(message.channel, "Nope. Not an admin.")
            else:
                if message.author == message.server.owner:
                    # Obviously the server owner can manage the bot
                    for command in self.references['Admin'].commands:
                        if message.content.lower().startswith("@" + command[0]):
                            if command[0] == "server":
                                ret = await command[1](message)
                            else:
                                ret = command[1](message)
                            if isinstance(ret, str):
                                await self.send_message(message.channel, str)
                            elif isinstance(ret, dict):
                                self.config = ret
                                await self.send_message(message.channel, "Server settings updated.")
                            else:
                                now = datetime.now()
                                repret = self.reporting.createissue("Unexpected Return Type",
                                                                    "I encountered an error while attempting to run a command in the Admin module on {0} using string {1}.\nType: {2}\nError: Wrong Type Returned".format(
                                                                        now, message.content, type(ret)))
                                if repret == 0:
                                    await self.send_message(message.channel,
                                                            "I encountered an error processing your command and was unable to create a github issue for it.")
                                else:
                                    await self.send_message(message.channel,
                                                            "I encountered an error processing your command and notified my creator on github by opening an issue. See it here:\n{0}".format(
                                                                repret))
                        break
                else:
                    for role in message.author.roles:
                        if role.permissions.manage_server:
                            # Well they can manage the server so they can manage the bot, deal with it
                            for command in self.references['Admin'].commands:
                                if message.content.lower().startswith("@" + command[0]):
                                    if command[0] == "leave":
                                        ret = await command[1](message)
                                    else:
                                        ret = command[1](message)
                                    if isinstance(ret, str):
                                        await self.send_message(message.channel, str)
                                    elif isinstance(ret, dict):
                                        self.config = ret
                                        await self.send_message(message.channel, "Server settings updated.")
                                    else:
                                        now = datetime.now()
                                        repret = self.reporting.createissue("Unexpected Return Type",
                                                                            "I encountered an error while running a command in the Admin module on {0} using the string {1}.\nType: {2}\nError: Wrong Return Type".format(
                                                                                now, message.content, type(ret)))
                                        if repret == 0:
                                            await self.send_message(message.channel,
                                                                    "I encountered an error while processing your command and was unable to report it on github automatically.")
                                        else:
                                            await self.send_message(message.channel,
                                                                    "I encountered an error while processing your command and was able to report it on github automatically. See it here:\n{0}".format(
                                                                        repret))
                                break
                    # They can't manage the server
                    await self.send_message(message.channel, "Nope. NOt an admin.")
        else:
            prefix = "$"
            if message.server.name in self.config['Servers']:
                if 'Prefix' in self.config['Servers'][message.server.name]:
                    prefix = self.config['Servers'][message.server.name]['Prefix']
                for item in self.config['Servers'][message.server.name]['Modules']:
                    if item['channel_lock'] is None or item['channel_lock'] == message.channel:
                        for command in self.references[item['Name']].commands:
                            if message.content.lower().startswith(prefix + command[0]):
                                ret = command[1](message)
                                await self.send_message(message.channel, ret)

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

# Call the exit methods of the modules currently Loaded. These should return 1.
for cls in bot.references:
    if bot.references[cls].exit() == 0:
        print("{0} didn't close correctly.".format(cls))
