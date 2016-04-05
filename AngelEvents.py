import datetime
from dateutil import parser
from globals import *


class Events():
    def __init__(self):
        self.events = []
        self.nextid = 0

    def create(self, etype, cstring, server):
        if etype == 'raid':
            raid = cstring.split('at')[0]
            if 'for' in cstring:
                time = cstring.split('at')[1].split('for')[0]
                stage = cstring.split('for')[1]
                self.events.append(
                    {'id': self.nextid, 'raid': raid.split('savage')[0].strip() if 'savage' in raid else raid,
                     'savage': 1 if 'savage' in raid else 0, 'stage': stage, 'time': time,
                     'tobject': parser.parse(time), 'server': server, 'party': globals.parties['full'],
                     'signups': {}})
                self.nextid += 1
            else:
                time = cstring.split('at')[1]
                self.events.append(
                    {'id': self.nextid, 'raid': raid.split('savage')[0].strip() if 'savage' in raid else raid,
                     'savage': 1 if 'savage' in raid else 0, 'time': time,
                     'tobject': parser.parse(time), 'server': server, 'party': globals.parties['full'],
                     'signups': {}})
                self.nextid += 1
        elif etype == 'roulette':

        elif etype == 'trial':
        elif etype == 'other':
