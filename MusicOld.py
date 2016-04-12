# Here you would process your message.content
# Self.play_next is an asyncio.event
# Self is a discord.client
# Self.message_channel is a discord channel. It was the first version of channel locking.
if message.content.lower().startswith('$yt'):
    if message.channel == self.message_channel:
        if self.stream == 0:
            await self.playlist.put(message.content[4:])
            self.loop.create_task(self._play_urls(server=message.server))
        else:
            if self.stream.is_done():
                await self.playlist.put(message.content[4:])
                self.loop.create_task(self._play_urls(server=message.server))
            else:
                await self.playlist.put(message.content[4:])
                await self.send_message(self.message_channel,
                                  "Added your url to the queue. There are {0} songs in the queue.".format(
                                      self.playlist.qsize()))
elif message.content.lower().startswith('$stop'):
    if message.channel == self.message_channel:
        if self.stream == 0:
            await self.send_message(message.channel, "Nothing playing.")
            return
        if message.server != 'None':
            for role in message.author.roles:
                if role.permissions.kick_members:
                    if not self.stream.is_done() and self.stream != 0:
                        self.stream.stop()
                    else:
                        await self.send_message(message.channel, "There isn't anything playing.")
                    return
            else:
                await self.send_message(message.author, "No permission to stop play.")
elif message.content.lower().startswith('$play'):
    if message.channel == self.message_channel:
        if self.stream == 0:
            await self.send_message(message.channel, "Nothing playing.")
            return
        if message.server != 'None':
            for role in message.author.roles:
                if role.permissions.kick_members:
                    if not self.stream.is_done() and self.stream != 0:
                        self.stream.resume()
                    else:
                        await self.send_message(message.channel, "There isn't anything playing.")
                    return
            else:
                await self.send_message(message.author, "No permission to resume play.")
elif message.content.lower().startswith('$next'):
    if message.channel == self.message_channel:
        if self.playlist.qsize():
            for role in message.author.roles:
                if role.permissions.kick_members:
                    self.stream.stop()
                    self.loop.call_soon_threadsafe(self.play_next.set)
                    return
            await self.send_message(message.author, "No permission to skip to next song.")
            return
        else:
            await self.send_message(message.channel, "There aren't any more songs in the queue.")
elif message.content.lower().startswith('$vjoin'):
    if message.channel == self.message_channel:
        if self.voice is None:
            cname = message.content[7:]
            channel = discord.utils.get(message.server.channels, name=cname, type=discord.ChannelType.voice)
            if channel is not None:
                await self.join_voice_channel(channel)
                if self.is_voice_connected():
                    await self.send_message(message.channel, "Connected to Voice Channel {0}.".format(cname))
                else:
                    await self.send_message(message.channel, "Unable to establish voice connection.")
            else:
                await self.send_message(message.channel, "That's not a voice channel.")
        elif self.voice is not None:
            for role in message.author.roles:
                if role.permissions.kick_members:
                    await self.voice.disconnect()
                    cname = message.content[7:]
                    channel = discord.utils.get(message.server.channels, name=cname,
                                                type=discord.ChannelType.voice)
                    if channel is not None:
                        await self.join_voice_channel(channel)
                        if self.is_voice_connected():
                            await self.send_message(message.channel,
                                              "Connected to Voice Channel {0}.".format(cname))
                        else:
                            await self.send_message(message.channel, "Unable to establish voice connection.")
                    else:
                        await self.send_message(message.channel, "That's not a voice channel.")
                    return
            else:
                await self.send_message(message.author,
                                  "Already on voice channel {0}.".format(self.voice.channel.name))
else:
    if message.channel == self.message_channel:
        for command in self.XIVDB.commands:
            if message.content.lower().startswith(command[0]):
                if command[2]:
                    await self.send_message(message.author, command[1](message.content[len(command[0]) + 1:]))
                else:
                    await self.send_message(self.message_channel,
                                      command[1](message.content[len(command[0]) + 1:]))


def toggle_next(self):
    self.loop.call_soon_threadsafe(self.play_next.set)


async def _play_urls(self, server):
    while self.playlist.qsize():
        if self.voice is None:
            self.stream.stop()
            self.playlist.empty()
            await self.send_message(self.message_channel,
                                    "I lost connection to voice. Please give me a channel to join again.")
            return
        self.play_next.clear()
        nurl = await self.playlist.get()
        self.stream = await self.voice.create_ytdl_player(nurl, after=self.toggle_next)
        self.stream.start()
        await self.send_message(self.message_channel, "Now Playing: {0}".format(self.stream.title))
        await self.play_next.wait()
