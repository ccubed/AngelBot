import importlib
import sys
import inspect


class HotCode:
    def __init__(self):
        self.commands = [['hotload', self.hotload], ['reload', self.reload]]

    def hotload(self, message):
        modtoload = message.content[9:]
        importlib.invalidate_caches()
        try:
            modref = importlib.import_module(modtoload)
        except ImportError:
            return "Couldn't load the specified module: {0}".format(modtoload)
        else:
            return modref

    def reload(self, message):
        modtoload = message.content[8:]
        importlib.invalidate_caches()
        try:
            modref = importlib.reload(modtoload)
        except ImportError:
            return "Couldn't load the specified module: {0}".format(modtoload)
        else:
            return modref

    def exit(self):
        return 1
