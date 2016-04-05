import discord
import asyncio
import random
import logging
from cleverbot import Cleverbot
from XIVDBBOT import *

class AngelBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.XIVDB = DBParser()
        self.cbot = Cleverbot()

    async def on_message(self, message):
        if message.author == self.user:
            return
        elif self.user in message.mentions:
            await self.send_message(message.channel, self.cbot.ask(message.content))
        elif message.content.startswith('https://discord.gg'):
            await self.accept_invite(message.content)
        elif message.content.lower().startswith('@help'):
            await self.send_message(message.author,
                                    "You can get help for this bot online from the manual.\nThis bot written by Cooper.\nhttp://angelbot.rtfd.org/")
        elif message.content.lower().startswith('@leave'):
            if message.server != 'None' and self.permissions_for(message.author).kick_members:
                await self.leave_server(message.server)
        elif message.content.lower().startswith('$search'):
            await self.send_message(message.channel, self.XIVDB.searchall(message.content[8:]))
        elif message.content.lower().startswith('$item'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[6:], 'items'))
        elif message.content.lower().startswith('$quest'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[7:], 'quests'))
        elif message.content.lower().startswith('$recipe'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[8:], 'recipes'))
        elif message.content.lower().startswith('$action'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[8:], 'actions'))
        elif message.content.lower().startswith('$mats'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[6:], 'gatherings'))
        elif message.content.lower().startswith('$npc'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[5:], 'npcs'))
        elif message.content.lower().startswith('$effect'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[8:], 'status'))
        elif message.content.lower().startswith('$minion'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[8:], 'minions'))
        elif message.content.lower().startswith('$achievement'):
            await self.send_message(message.channel, self.XIVDB.searchone(message.content[13:], 'achievements'))
        elif message.content.lower().startswith('$shop'):
            await self.send_message(message.author, self.XIVDB.searchone(message.content[6:], 'shops'))
        elif message.content.lower().startswith('$hdim'):
            await self.send_message(message.channel, self.XIVDB.parsehdim(message.content[6:]))
        elif message.content.lower().startswith('$wdif'):
            messages = self.XIVDB.parsewdif(message.content[6:])
            if len(messages):
                for item in messages:
                    await self.send_message(message.author, item)
            else:
                await self.send_message(message.author, "Sorry, I found that item but there's no data for where to find it.")

    async def on_ready(self):
        return


bot = AngelBot()
logging.basicConfig(level=logging.DEBUG)
bot.run('email', 'pass')
