import json
import sys
import time
import AngelBot
import IPC_Test
import discord
import redis
import requests
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
        self.last_update = None
        
    def setup(self):
        rdb = redis.StrictRedis(host='localhost', port=6379, db=1, decode_responses=True)
        self.token = rdb.get("BotToken")
        del rdb
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

    def _runtest(self, sid, count, conn):
        bot = IPC_Test.AngelBot(sid, count, conn)
        bot.loop.run_until_complete(bot.setup())
        bot.run(bot.btoken)

    def start_shards(self):
        for number in range(self.shard_count):
            if number != 1:
                r, w = Pipe(duplex=False)
                self.r_pipes.append(r)
                journal.send("INFO:AngelBot Manager: Starting Shard {}".format(number))
                temp = Process(target=self._run, args=(number, self.shard_count, w))
                temp.start()
                self.shards[number] = {'Pipe': r, 'Process': temp}
                journal.send("STATUS:Shard {}: Shard Started.".format(number))
            else:
                r, w = Pipe(duplex=False)
                self.r_pipes.append(r)
                journal.send("INFO:AngelBot Manager: Starting Shard {}".format(number))
                temp = Process(target=self._runtest, args=(number, self.shard_count, w))
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
                        journal.send("UPDATE:Shard {0}: Shard {0} reporting stats. {1} servers. {2} members.".format(sid,
                                                                                                                     servs,
                                                                                                                     members))
                        print(self.shards)
                        self.shards[sid]['stats'] = {'servers': servs, 'users': members}

                        if all(self.shards[x].has_key('stats') for x in range(self.shard_count)) and (self.last_update is None or time.time() - self.last_update > 1500):
                            total_stats = {'Servers': sum(self.shards[x]['stats']['servers'] for x in range(self.shard_count)),
                                           'Users': sum(self.shards[x]['stats']['users'] for x in range(self.shard_count))}

                            rdb = redis.StrictRedis(host='localhost', port=6379, db=1, decode_responses=True)
                            ckey = rdb.get("CarbonKey")
                            lkey = rdb.get("CarbonKey")

                            r = requests.post("https://www.carbonitex.net/discord/data/botdata.php",
                                              data=json.dumps({'key': ckey, 'servercount': total_stats['Servers']}),
                                              headers={'Content-Type': 'application/json'})
                            if r.status_code != 200:
                                journal.send("ERROR:AngelBot Manager: Attempted to update carbonitex but got {}".format(r.status_code))
                                journal.send("ERROR DETAILS: {}".format(r.text))

                            r = requests.post("https://bots.discord.pw/api/bots/168925517079248896/stats",
                                              data=json.dumps({'server_count': total_stats['Servers']}),
                                              headers={"Authorization": lkey, "Content-Type": "application/json"})
                            if r.status_code != 200:
                                journal.send("ERROR:AngelBot Manager: Attempted to update bots.discord.pw but got {}".format(r.status_code))
                                journal.send("ERROR DETAILS: {}".format(r.text))

                            rdb.hset("stats", "users", total_stats['Users'])
                            rdb.hset("stats", "servers", total_stats['Servers'])
                            journal.send("INFO:AngelBot Manager: Finished updating stats.")
                            self.last_update = time.time()
                            for shard in range(self.shard_count):
                                del self.shards[shard]['stats']

        journal.send("INFO:AngelBot Manager: Shards Exhausted. Shutting down.")
        
    
if __name__ == "__main__":
    journal.send("STATUS:AngelBot Manager: Starting Up.")
    MPManager()
