import json
import AngelBot
import requests
import discord
from multiprocessing import Process, Pipe
from multiprocessing.connection import wait
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
            "User-Agent": 'DiscordBot (https://github.com/Rapptz/discord.py {0}) Python/{1[0]}.{1[1]} requests/{2}'.format(discord.__version__, sys.version_info, requests.__version__)
        })
        
        if r.status_code == 200:
            return r.json()['shards']+1
        else:
            return None
    
    
    def start_shards(self):
        for number in range(self.shard_count):
            r,w = Pipe(duplex=False)
            self.r_pipes.append(r)
            temp = Process(target=AngelBot, args=(number, self.shard_count, w))
            temp.start()
            self.shards[number] = {'Pipe': r, 'Bot': temp}
        
        while self.shards.keys():
            for reader in wait(self.r_pipes):
                try:
                    msg = r.recv()
                except EOFError:
                    self.r_pipes.remove(reader)
                else:
                    print(msg)
                    
        
        print("Going down. No more shards.")
        
    
if __name__ == "__main__":
    MPManager()
    