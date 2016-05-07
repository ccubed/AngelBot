import sys
import inspect
import asyncio


class admin:
    def __init__(self, redis):
        self.commands = [['server', self.serversettings]]
        self.pools = redis

    async def serversettings(self, message):
        key = message.content[10:].split(":")[0].lower()
        value = message.content[10:].split(":")[1]
        async with self.pools.get() as pool:
            if await pool.exists(message.server.id):
                if key == 'modules':
                    cname, mod = self.parsechannel(value)
                    mods = await pool.lrange("BotModules", 0, -1)
                    if mod not in mods:
                        return "No module by name {0}".format(mod)
                    smods = await pool.hgetall(message.server.id + "_Modules")
                    for item in smods.keys():
                        if item == mod:
                            if cname is None:
                                await pool.hset(message.server.id + "_Modules", item, "None")
                            else:
                                s = set(cname)
                                locks = await pool.hget(message.server.id + "_Modules", item)
                                chanlock = [x for x in locks if x not in s]
                                await pool.hset(message.server.id + "_Modules", item, '|'.join(chanlock))
                            return "Added {0} to your server. Locked to channel {1}.".format(mod, cname if cname is not None else 'All')
                    await pool.hset(message.server.id + "_Modules", mod, cname if cname is not None else 'None')
                    return "Added {0} to your server. Locked to channel {1}".format(mod, cname if cname is not None else 'All')
                elif key == 'admin':
                    names = await pool.hget(message.server.id, "Admin")
                    newlist = [x.id for x in message.mentions]
                    if names != "None":
                        final = "|".join(set(newlist).symmetric_difference(set(names.split("|"))))
                    else:
                        final = newlist
                    await pool.hset(message.server.id, "Admin", final)
                    return "Admin list is now: ```{0}```".format(", ".join(final.split("|")))
                elif key == 'prefix':
                    if value in ['owl', 'ard', '@']:
                        return "You can't use owl, ard or @ as prefixes."
                    else:
                        await pool.hset(message.server.id, "Prefix", message.content.split(" ")[1])
                        return "Set Prefix to ```{0}```.".format(message.content.split(" ")[1])
            else:
                await self.createnewserver(message.server.id, pool)
                if key == 'modules':
                    cname, mod = self.parsechannel(value)
                    mods = await pool.lrange("BotModules", 0, -1)
                    if mod not in mods:
                        return "No module by name {0}".format(mod)
                    await pool.hset(message.server.id + "_Modules", mod, '|'.join(cname))
                    return "Added {0} to your server. Locked to channel {1}.".format(mod,
                                                                                             cname if cname is not None else 'All')
                elif key == 'admin':
                    ids = [x.id for x in message.mentions]
                    await pool.hset(message.server.id, "Admin", "|".join(ids))
                    return "List of Admin now: ```{0}```".format(", ".join(value.replace("@", "@/")))
                elif key == 'prefix':
                    if message.content.split(" ")[1] in ['owl', 'ard', '@']:
                        return "You can't use owl, ard or @ as prefixes."
                    else:
                        await pool.hset(message.server.id, "Prefix", value)
                        return "Set prefix to ```{0}```.".format(value)

    def parsechannel(self, value):
        module = value.split("=")[0]
        if "=" in value:
            channel_name = value.split("=")[1].split(" ")
        else:
            channel_name = None
        return channel_name, module

    async def createnewserver(self, server, pool):
        await pool.hset(server, "Prefix", "$")
        await pool.hset(server + "_Modules", "Admin", "None")
        await pool.hset(server, "Admin", "None")

    async def cleanconfig(self, server):
        async with self.pools.get() as pool:
            await pool.delete(server)
            await pool.delete(server+"_Modules")

    def exit(self):
        return 1