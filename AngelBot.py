import discord
import asyncio
import random
import logging
from discord.ext import commands
from XIVDBBOT import *


class AngelBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.XIVDB = DBParser()

    async def on_message(self, message):
        if message.author == self.user:
            return
        elif message.content.startswith('http://discord.gg'):
            await self.accept_invite(message.content)
        elif message.content.startswith('@help'):
            await self.send_message(message.author,
                              "Help for AngelBot\n\nThis bot has several modules. To get help on the individual modules please use the following commands. You can also use @leave to make the bot leave the server.\n   @xivdb - Commands relating to XIVDB")
        elif message.content.startswith('@xivdb'):
            await self.send_message(message.author, "XIVDB Commands ->\n$search <name or ID> - Search for something on XIVDB\n$item <name or ID> - Search for an item. Items are weapons, armor, etc.\n$quest <name or ID> - Search for a quest.\n$recipe <name or ID> - Search for a crafting recipe.\n$action <name or ID> - Search for a skill.\n$mats <name or ID> - Search for the location details on a gatherable material.\n$npc <name or ID> - Search for details on an NPC.\n$effect <name or ID> - Search for information on a status effect.\n$minion <name or ID> - Search for information on a minion.\n$achievement <name or ID> - Search for information on an achievement.\n$hdim <name or ID> - How do I make...Search for instructions on making a thing.\n$wdif <name> - Where do I find...Search for the locations of items.")
        elif message.content.startswith('@leave'):
            if message.server != 'None' and self.permissions_for(message.author).kick_members:
                await self.leave_server(message.server)
        elif message.content.startswith('$search'):
            await self.send_message(message.channel, self.XIVDB.searchall(message.content[8:]))
        elif message.content.startswith('$item'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[6:],'items'))
        elif message.content.startswith('$quest'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[7:], 'quests'))
        elif message.content.startswith('$recipe'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[8:], 'recipes'))
        elif message.content.startswith('$action'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[8:], 'actions'))
        elif message.content.startswith('$mats'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[6:], 'gatherings'))
        elif message.content.startswith('$npc'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[5:], 'npcs'))
        elif message.content.startswith('$effect'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[8:], 'status'))
        elif message.content.startswith('$minion'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[8:], 'minions'))
        elif message.content.startswith('$achievement'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[13:], 'achievements'))
        elif message.content.startswith('$shop'):
            await self.send_message(message.author, self.XIVDB.searchone(message.content[6:], 'shops'))
        elif message.content.startswith('$hdim'):
            await self.send_message(message.channel, self.XIVDB.parsehdim(message.content[6:]))
        elif message.content.startswith('$wdif'):
            messages = self.XIVDB.parsewdif(message.content[6:])
            async for message in messages:
                await self.send_message(message.author, message)

    async def on_ready(self):
        async for server in self.servers:
            await self.send_message(server, "AngelBot is online. For help type @help.")

bot = AngelBot()
logging.basicConfig(level=logging.DEBUG)
bot.run('email', 'pass')