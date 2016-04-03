import discord
import random
from discord.ext import commands
from XIVDBBOT import *


class AngelBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.XIVDB = DBParser()

    @client.async_event
    def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('$help'):
            await self.send_message(message.author,
                              "Help for AngelBot\n\n- XIVDB Commands -\n!search <name or ID> - Search for something on XIVDB\n!item <name or ID> - Search for an item. Items are weapons, armor, etc.\n!quest <name or ID> - Search for a quest.\n!recipe <name or ID> - Search for a crafting recipe.\n!action <name or ID> - Search for a skill.\n!mats <name or ID> - Search for the location details on a gatherable material.\n!npc <name or ID> - Search for details on an NPC.\n!effect <name or ID> - Search for information on a status effect.\n!minion <name or ID> - Search for information on a minion.\n!achievement <name or ID> - Search for information on an achievement.\n!hdim <name or ID> - How do I make...Search for instructions on making a thing.\n!wdif <name> - Where do I find...Search for the locations of items.")


    @client.async_event
    def on_ready(self):
        print('Logged in')


bot = AngelBot()
bot.run('email', 'password')