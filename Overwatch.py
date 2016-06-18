import aiohttp

class OWAPI:
    def __init__(self):
        # Map Numbers to names
        self.index = {1: 'Roadhog', 2: 'Junkrat', 3: 'Lucio', 4: 'Soldier: 76', 5: 'Zarya', 6: 'McCree', 7: 'Tracer', 8: 'Reaper',
                      9: 'Widowmaker', 10: 'Winston', 11: 'Pharah', 12: 'Reinhardt', 13: 'Symmetra', 14: 'Torbjorn', 15: 'Bastion',
                      16: 'Hanzo', 17: 'Mercy', 18: 'Zenyatta', 20: 'Mei', 21: 'Genji', 22: 'D.Va'}
        # Map names to Numbers
        self.characters = [{'names': ['roadhog', 'birdie'], 'id': 1}, {'names': ['junkrat', 'crocodile dun dee'], 'id': 2},
                           {'names': ['lucio', 'drop the beats'], 'id': 3}, {'names': ['soldier: 76', 'cod', 'blops'], 'id': 4},
                           {'names': ['zarya', 'i must break you'], 'id': 5}, {'names': ['mccree', 'robo dead redemption'], 'id': 6},
                           {'names': ['tracer', 'booty', 'bootiful'], 'id': 7}, {'names': ['reaper', 'edgelord'], 'id': 8},
                           {'names': ['widowmaker', 'boo berry', 'boobs'], 'id': 9}, {'names': ['winston', 'dr zaius', 'caesar'], 'id': 10},
                           {'names': ['pharah', 'gundam wing'], 'id': 11}, {'names': ['reinhardt', 'the iron giant', 'fell off the map'], 'id': 12},
                           {'names': ['symmetra', 'chellmetra'], 'id': 13}, {'names': ['torbjorn', 'tim the turret man taylor', 'engineer'], 'id': 14},
                           {'names': ['bastion', 'git gud'], 'id': 15}, {'names': ['hanzo', 'ryuu ga teki no'], 'id': 16},
                           {'names': ['mercy', 'the medic', 'mother mercy'], 'id': 17}, {'names': ['zenyatta', 'android krillin'], 'id': 18},
                           {'names': ['mei', 'bae', 'waifu'], 'id': 20}, {'names': ['genji', 'animu'], 'id': 21},
                           {'names': ['D.Va', 'twitch streamer', 'gamer girl'], 'id': 22}]
        self.commands = [['ow', self.ow], ['owheroes', self.owheroes], ['owhero', self.owhero]]

    async def ow(self, message):
        pass

    async def owheroes(self, message):
        pass

    async def owhero(self, message):
        pass