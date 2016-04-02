import importlib
import sys
import inspect


class HotCode:
    def __init__(self, redis):
        self.commands = [['hotload', self.hotload]]
        self.pools = redis

    def hotload(self, message):
        modtoload = message.content[11:]
        importlib.invalidate_caches()
        try:
            modref = importlib.import_module(modtoload)
        except ImportError:
            return "Couldn't load the specified module: {0}".format(modtoload)
        else:
            return modref

    def exit(self):
        return 1
