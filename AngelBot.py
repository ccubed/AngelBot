import discord
import asyncio
import logging
from cleverbot import Cleverbot
from XIVDBBOT import *
from AngelEvents import *
from DiscordGlobals import *


class AngelBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.XIVDB = DBParser()
        self.cbot = Cleverbot()
        self.planner = Events()
        self.servers = {}

    async def on_message(self, message):
        if message.author == discord_bot_username:
            return

    async def on_ready(self):
        return


bot = AngelBot()
logging.basicConfig(level=logging.DEBUG)
bot.run(discord_bot_token)
