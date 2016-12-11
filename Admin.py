import sys
import inspect
import asyncio
from discord import embeds


class admin:
    def __init__(self, client):
        self.commands = [['server', self.serversettings]]
        self.pools = client.redis
        self.bot = client

    async def serversettings(self, message):
        if 'prefix' not in message.content.lower():
            embed = embeds.Embed(description="This bot no longer needs to have modules enabled. All commands are enabled by default with the prefix of $. You can still define a custom prefix. To lock me out of channels restrict me from reading messages.")
            embed.title = "Notice"
            await self.bot.send_message(message.channel, embed=embed)
            return
        key = message.content[10:].split(":")[0].lower()
        value = message.content[10:].split(":")[1]
        async with self.pools.get() as pool:
            test = pool.exists(message.server.id)
            if test:
                if key == 'prefix':
                    if value in ['owl', 'ard', '@']:
                        await self.bot.send_message(message.channel, "You can't use owl, ard or @ as prefixes.")
                    else:
                        await pool.hset(message.server.id, "Prefix", value)
                        await self.bot.send_message(message.channel, "Set Prefix to ```{0}```.".format(value))
            else:
                await self.createnewserver(message.server.id, pool)
                if key == 'prefix':
                    if message.content.split(" ")[1] in ['owl', 'ard', '@']:
                        await self.bot.send_message(message.channel, "You can't use owl, ard or @ as prefixes.")
                    else:
                        await pool.hset(message.server.id, "Prefix", value)
                        await self.bot.send_message(message.channel, "Set prefix to ```{0}```.".format(value))

    async def createnewserver(self, server, pool):
        await pool.hset(server, "Prefix", "$")
        await pool.hset(server + "_Modules", "Admin", "None")
        await pool.hset(server, "Admin", "None")

    async def cleanconfig(self, server):
        async with self.pools.get() as pool:
            await pool.delete(server)
            await pool.delete(server+"_Modules")