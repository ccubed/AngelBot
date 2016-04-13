import json
import sys
import inspect
import asyncio


class admin:
    def __init__(self):
        with open("Global_config.json", mode="r") as cfg:
            self.config = json.load(cfg)
        self.commands = [['server', self.serversettings]]
        self.lock = asyncio.Lock()

    async def serversettings(self, message):
        await self.lock.acquire()
        key = message.content[8:].split(":")[0].lower()
        value = message.content[8:].split(":")[1]
        if message.server.name in self.config['Servers']:
            if key == 'modules':
                cname, mod = self.parsechannel(value)
                if mod not in self.config['Modules']:
                    self.lock.release()
                    return "No module by name {0}".format(mod)
                for item in self.config['Servers'][message.server.name]['Modules']:
                    if item['Name'] == mod:
                        if cname is None:
                            item['channel_lock'] = None
                            self.lock.release()
                            return self.config
                        else:
                            s = set(cname)
                            item['channel_lock'] = [x for x in item['channel_lock'] if x not in s]
                            self.lock.release()
                            return self.config
                # New Mod
                self.config['Servers'][message.server.name]['Modules'].append({'Name': mod, 'channel_lock': cname})
                self.lock.release()
                return self.config
            elif key == 'admin':
                names = list(
                    set(value.split(" ")).symmetric_difference(self.config['Servers'][message.server.name]['Admin']))
                self.config['Servers'][message.server.name]['Admin'] = names
                self.lock.release()
                return self.config
            elif key == 'prefix':
                if value in ['#', '@']:
                    self.lock.release()
                    return "You can't use # or @ as prefixes."
                else:
                    self.config['Servers'][message.server.name]['Prefix'] = value
                    self.lock.release()
                    return self.config
            else:
                self.lock.release()
                return 1
        else:
            self.createnewserver(message.server.name)
            if key == 'modules':
                cname, mod = self.parsechannel(value)
                if mod not in self.config['Modules']:
                    self.lock.release()
                    return "No module by name {0}".format(mod)
                else:
                    self.config['Servers'][message.server.name]['Modules'].append({'Name': mod, 'channel_lock': cname})
                    self.lock.release()
                    return self.config
            elif key == 'admin':
                self.config['Servers'][message.server.name]['Admin'] = value.split(" ")
                self.lock.release()
                return self.config
            elif key == 'prefix':
                if value in ['#', '@']:
                    self.lock.release()
                    return "You can't use # or @ as prefixes."
                else:
                    self.config['Servers'][message.server.name]['Prefix'] = value
                    self.lock.release()
                    return self.config
            else:
                self.lock.release()
                return 1

    def parsechannel(self, value):
        module = value.split("=")[0]
        if "=" in value:
            channel_name = value.split("=")[1].split(" ")
        else:
            channel_name = None
        return channel_name, module

    def createnewserver(self, server):
        self.config['Servers'][server] = {}
        self.config['Servers'][server]['Modules'] = [{'Name': 'Admin', 'channel_lock': None}]
        self.config['Servers'][server]['Prefix'] = '$'
        self.config['Servers'][server]['Admin'] = []

    def exit(self):
        with open("Global_config.json", mode="w") as cfg:
            json.dump(obj=self.config, fp=cfg, indent=2)
        return 1