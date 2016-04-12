import json, sys, inspect, asyncio

class admin:
    def __init__(self):
        self.config = 0
        self.commands = [['server', self.serversettings], ['loadconfig', self.loadconfig], ['leave', self.leave]]

    def loadconfig(self):
        with open("Global_config.json", mode="r") as cfg:
            self.config = json.load(cfg)
        return self.config

    def serversettings(self, message):
        return self.config

    async def leave(self, message):
        for item in inspect.getmembers(sys.modules[__name__], inspect.isclass):
            if item[0] == "bot":
                await item[1].client.leave_server(message.server)
                return "We left {0}".format(message.server)
        return "Well that didn't work."