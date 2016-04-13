import importlib
import sys


class HotCode:
    def __init__(self):
        self.commands = [['hotload', self.hotload], ['reload', self.reload], ['eval', self.debug]]

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
        if modtoload not in globals():
            return "Module {0} isn't loaded. Perhaps you meant to hotload it?".format(modtoload)
        try:
            modref = importlib.reload(modtoload)
        except ImportError:
            return "Couldn't load the specified module: {0}".format(modtoload)
        else:
            importlib.invalidate_caches()
            return modref

    def exit(self):
        return 1

    async def debug(self, message):
        if "|" in message.content:
            context = message.content.split("|")[0]
            code = message.content.split("|")[1]
            if 'bot' not in globals():
                return "I couldn't find the master instance. Did something happen?"
            else:
                if context not in globals()['bot'].references:
                    return "I couldn't find context {0} in loaded contexts. Perhaps you need to hotload it first?".format(context)
                else:
                    context_loaded = globals()['bot'].references[context]
                    check = code.split("(")[0]
                    if " " in check:
                        check = check.split(" ")[-1:]
                    if '_is_coroutine' in context_loaded.check.__dict__:
                        result = await eval(code, globals={'message': message, context: context_loaded})
                    else:
                        result = eval(code, globals={'message': message, context: context_loaded})
                    return str(result)
        else:
            return eval(message.content[8:])
