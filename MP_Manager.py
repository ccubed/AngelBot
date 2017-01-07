import json
import AngelBot
import requests
import discord
import sys
from multiprocessing import Process, Pipe
from multiprocessing.connection import wait
from termcolor import colored, cprint
from discord.http import HTTPClient

BOT_ENDPOINT = HTTPClient.GATEWAY + "/bot"


class MPManager:
    def __init__(self):
        self.shards = {}
        self.token = None
        self.shard_count = 0
        self.r_pipes = []
        self.setup()
        
    def setup(self):
        self.shard_count = self.get_shard_count()
        if not self.shard_count:
            raise RuntimeError("Shard Count didn't go through. Is token right?")
        else:
            self.start_shards()

    def get_shard_count(self):
        r = requests.get(BOT_ENDPOINT, headers={
            "Authorization": "Bot {}".format(self.token),
            "User-Agent": 'DiscordBot (https://github.com/Rapptz/discord.py {0}) Python/{1[0]}.{1[1]} requests/{2}'.format(
                discord.__version__, sys.version_info, requests.__version__)
        })
        
        if r.status_code == 200:
            return r.json()['shards']+1
        else:
            return None

    def _run(self, sid, count, conn):
        bot = AngelBot.AngelBot(sid, count, conn)
        bot.loop.run_until_complete(bot.setup())
        bot.run(bot.btoken)

    def start_shards(self):
        for number in range(self.shard_count):
            r, w = Pipe(duplex=False)
            self.r_pipes.append(r)
            cprint("INFO:AngelBot Manager: Starting Shard {}".format(number), "yellow")
            temp = Process(target=self._run, args=(number, self.shard_count, w))
            temp.start()
            self.shards[number] = {'Pipe': r, 'Process': temp}
            cprint("STATUS:Shard {}: Shard Started.".format(number), "green")

        while self.shards.keys():
            for reader in wait(self.r_pipes):
                try:
                    msg = reader.recv()
                except EOFError:
                    self.r_pipes.remove(reader)
                else:
                    if 'QUIT' in msg:
                        del self.shards[int(msg.after(':'))]
                        cprint("QUIT:Shard {0}: Shard {0} Exited.".format(msg.after(":")), "red")
                        cprint("INFO:AngelBot Manager: Attempting to restart Shard {}".format(msg.after(':')), "yellow")
                        r, w = Pipe(duplex=False)
                        self.r_pipes.append(r)
                        cprint("INFO:AngelBot Manager: Starting Shard {}".format(msg.after(":")), "yellow")
                        temp = Process(target=self._run, args=(int(msg.after(":")), self.shard_count, w))
                        temp.start()
                        self.shards[int(msg.after(":"))] = {'Pipe': r, 'Process': temp}
                        cprint("STATUS:Shard {}: Shard restarted.".format(msg.after(":")), "green")
                    elif 'STATUS' in msg:
                        _, sid, servs, members = msg.split(":")
                        cprint("UPDATE:Shard {0}: Shard {0} reporting stats. {1} servers. {2} members.".format(sid, servs, members),
                               "cyan")

        cprint("INFO:AngelBot Manager: Shards Exhausted. Shutting down.", "yellow")
        
    
if __name__ == "__main__":
    cprint("STATUS:AngelBot Manager: Starting Up.", "green")
    MPManager()
