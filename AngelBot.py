import discord
import asyncio
import random
import logging
from cleverbot import Cleverbot
from XIVDBBOT import *
from AngelEvents import *


class AngelBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.XIVDB = DBParser()
        self.cbot = Cleverbot()
        self.planner = Events()
        self.stream = 0
        self.playlist = []

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
                await self.send_message(message.author,
                                        "Sorry, I found that item but there's no data for where to find it.")
        elif message.content.lower().startswith('$events'):
            await self.send_message(message.channel, self.planner.listevents(
                message.server if message.server != 'None' else message.channel))
        elif message.content.lower().startswith('$raid'):
            await self.send_message(message.channel, self.planner.create('raid', message.content[6:].lower(),
                                                                         message.server if message.server != 'None' else message.channel))
        elif message.content.lower().startswith('$trial'):
            await self.send_message(message.channel, self.planner.create('trial', message.content[7:].lower(),
                                                                         message.server if message.server != 'None' else message.channel))
        elif message.content.lower().startswith('$roulette'):
            await self.send_message(message.channel, self.planner.create('roulette', message.content[10:].lower(),
                                                                         message.server if message.server != 'None' else message.channel))
        elif message.content.lower().startswith('$other'):
            await self.send_message(message.channel, self.planner.create('raid', message.content[7:].lower(),
                                                                         message.server if message.server != 'None' else message.channel))
        elif message.content.lower().startswith('$join'):
            content = message.content[6:]
            await self.send_message(message.channel,
                                    self.planner.signup(content.split('as')[0].strip(), message.author.name,
                                                        content.split('with')[0].split('as')[1].strip(),
                                                        content.split('with')[1].strip(), message.author))
        elif message.content.lower().startswith('$wn'):
            await self.send_message(message.channel, self.planner.whatsneeded(message.content[4:]))
        elif message.content.lower().startswith('$who'):
            await self.send_message(message.channel, self.planner.whosgoing(message.content[5:]))
        elif message.content.lower().startswith('$yt'):
            self.stream = await self.voice.create_ytdl_player(message.content[4:])
            self.stream.start()
        elif message.content.lower().startswith('$stop'):
            if message.server != 'None' and self.permissions_for(message.author).kick_members:
                if not self.stream.is_done() and self.stream != 0:
                    self.stream.stop()
                else:
                    await self.send_message(message.channel, "There isn't anything playing.")
        elif message.content.lower().startswith('$play'):
            if message.server != 'None' and self.permissions_for(message.author).kick_members:
                if not self.stream.is_done() and self.stream != 0:
                    self.stream.resume()
                else:
                    await self.send_message(message.channel, "There isn't anything playing.")
        elif message.content.lower().startswith('$vjoin'):
            cname = message.content[7:]
            channel = discord.utils.get(message.server.channels, name=cname, type=ChannelType.voice)
            if channel is not None:
                await self.join_voice_channel(channel)
                if self.is_voice_connected():
                    await self.send_message(message.channel, "We connected to that channel.")
                else:
                    await self.send_message(message.channel, "Unable to establish voice connection.")
            else:
                await self.send_message(message.channel, "That's not a voice channel.")

    async def on_ready(self):
        return


bot = AngelBot()
logging.basicConfig(level=logging.DEBUG)
bot.run('email', 'pass')
