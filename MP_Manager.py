import json
import AngelBot
import requests
import discord
import sys
from multiprocessing import Process, Pipe
from multiprocessing.connection import wait
from systemd import journal
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
            journal.send("INFO:AngelBot Manager: Starting Shard {}".format(number))
            temp = Process(target=self._run, args=(number, self.shard_count, w))
            temp.start()
            self.shards[number] = {'Pipe': r, 'Process': temp}
            journal.send("STATUS:Shard {}: Shard Started.".format(number))

        while self.shards.keys():
            for reader in wait(self.r_pipes):
                try:
                    msg = reader.recv()
                except EOFError:
                    self.r_pipes.remove(reader)
                else:
                    if 'QUIT' in msg:
                        shard = int(msg.split(":")[1])
                        del self.shards[shard]
                        journal.send("QUIT:Shard {0}: Shard {0} Exited.".format(shard))
                        journal.send("INFO:AngelBot Manager: Attempting to restart Shard {}".format(shard))
                        r, w = Pipe(duplex=False)
                        self.r_pipes.append(r)
                        journal.send("INFO:AngelBot Manager: Starting Shard {}".format(shard))
                        temp = Process(target=self._run, args=(shard, self.shard_count, w))
                        temp.start()
                        self.shards[shard] = {'Pipe': r, 'Process': temp}
                        journal.send("STATUS:Shard {}: Shard restarted.".format(shard))
                    elif 'STATUS' in msg:
                        _, sid, servs, members = msg.split(":")
                        journal.send("UPDATE:Shard {0}: Shard {0} reporting stats. {1} servers. {2} members.".format(sid, servs, members))

        journal.send("INFO:AngelBot Manager: Shards Exhausted. Shutting down.")
        
    
if __name__ == "__main__":
    journal.send("STATUS:AngelBot Manager: Starting Up.")
    MPManager()
