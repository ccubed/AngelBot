import importlib
import sys


class HotCode:
    def __init__(self):
        self.commands = [['hotload', self.hotload], ['reload', self.reload]]

    def hotload(self, message):
        modtoload = message.content[9:]
        try:
            modref = importlib.import_module(modtoload)
        except ImportError:
            return "Couldn't load the specified module: {0}".format(modtoload)
        else:
            importlib.invalidate_caches()
            return modref

    def reload(self, message):
        modtoload = message.content[9:]
        if modtoload not in sys.modules:
            return "Module {0} isn't loaded. Perhaps you meant to hotload it?"
        try:
            modref = importlib.reload(modtoload)
        except ImportError:
            return "Couldn't load the specified module: {0}".format(modtoload)
        else:
            importlib.invalidate_caches()
            return modref

    def exit(self):
        return 1
