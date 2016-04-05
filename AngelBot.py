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
            await self.send_message(message.channel, cbot.ask(message.content))
        elif message.content.startswith('https://discord.gg'):
            await self.accept_invite(message.content)
        elif message.content.lower().startswith('@help'):
            await self.send_message(message.author,
                                    "Help for AngelBot\n\nThis bot has several modules. To get help on the individual modules please use the following commands. You can also use @leave to make the bot leave the server.\n   @xivdb - Commands relating to XIVDB")
        elif message.content.lower().startswith('@xivdb'):
            await self.send_message(message.author,
                                    "XIVDB Commands ->\n$search <name or ID> - Search for something on XIVDB\n$item <name or ID> - Search for an item. Items are weapons, armor, etc.\n$quest <name or ID> - Search for a quest.\n$recipe <name or ID> - Search for a crafting recipe.\n$action <name or ID> - Search for a skill.\n$mats <name or ID> - Search for the location details on a gatherable material.\n$npc <name or ID> - Search for details on an NPC.\n$effect <name or ID> - Search for information on a status effect.\n$minion <name or ID> - Search for information on a minion.\n$achievement <name or ID> - Search for information on an achievement.\n$hdim <name or ID> - How do I make...Search for instructions on making a thing.\n$wdif <name> - Where do I find...Search for the locations of items.")
        elif message.content.startswith('@event'):
            await self.send_message(message.author,
                                    "Events System ->\n$events - Overview of upcoming events\n$raid <name> at <date> for <stage> - Recruit a raid party. Name is the raid. IE: Alexander Midas Savage. Date is either a date in YYYY-MM-DD HH:MM Format or a word like tomorrow. For Stage is optional but allows you to specify which stage inside a raid. IE: For 5 for A5S.\n$roulette <Name> at <date> - Recruit a roulette party. See above for date details. Name should be Level 50, Level 60, Expert or Leveling.\n$trial <name> at <date> for <mode> - Recruit a primal party. Name is the primal, not the name of the dungeon. IE: Shiva or Ifrit or Ravana. It can be partial, like Mog for King Moogle. See above for Date. Mode should be Normal, Hard or Extreme.\n$other <name> at <date> - Register an event such as a wedding or FC meeting that doesn't fall under the other categories.\n$join <id> as <role> with <class> - Join event <id> as <role> where role is Healer, Tank or DPS with <class> where class should be the class you intend to use such as BRD or Bard, etc. If the event is an other type you can just use use $join <id>.")
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
            for item in messages:
                await self.send_message(message.author, item)

    async def on_ready(self):
        return


bot = AngelBot()
logging.basicConfig(level=logging.DEBUG)
bot.run('email', 'pass')
