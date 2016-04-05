import datetime
from dateutil import parser
from globals import *


class Events():
    def __init__(self):
        self.events = []
        self.nextid = 0

    def create(self, etype, cstring, server):
        if etype == 'raid':
            raid = cstring.split('at')[0].strip()
            if 'for' in cstring:
                time = cstring.split('at')[1].split('for')[0].strip()
                stage = cstring.split('for')[1].strip()
                self.events.append(
                    {'id': self.nextid, 'raid': raid.split('savage')[0].strip() if 'savage' in raid else raid,
                     'savage': 1 if 'savage' in raid else 0, 'stage': stage, 'time': time,
                     'tobject': parser.parse(time), 'server': server, 'party': parties['full'],
                     'signups': {}})
                msg = "Created Event {0} which happens at {1}".format(self.nextid, time)
                self.nextid += 1
                return msg
            else:
                time = cstring.split('at')[1].strip()
                self.events.append(
                    {'id': self.nextid, 'raid': raid.split('savage')[0].strip() if 'savage' in raid else raid,
                     'savage': 1 if 'savage' in raid else 0, 'time': time,
                     'tobject': parser.parse(time), 'server': server, 'party': parties['full'],
                     'signups': {}})
                msg = "Created Event {0} which happens at {1}".format(self.nextid, time)
                self.nextid += 1
                return msg
        elif etype == 'roulette':
            raid = cstring.split('at')[0].strip()
            date = cstring.split('at')[1].strip()
            self.events.append(
                {'id': self.nextid, 'raid': raid 'time': date, 'tobject': parser.parse(date), 'server': server,
                 'party': parties['light'], 'signups': {}})
            msg = "Created Event {0} which happens at {1}".format(self.nextid, date)
            self.nextid += 1
            return msg
        elif etype == 'trial':
            raid = cstring.split('at')[0].strip()
            date = cstring.split('at')[1].split('for')[0].strip()
            mode = cstring.split('for')[1].strip()
            self.events.append(
                {'id': self.nextid, 'raid': raid, 'time': date, 'tobject': parser.parse(date), 'server': server,
                 'party': parties['light'] if mode == 'normal' else parties['full'], 'signups': {}, 'mode': mode})
            msg = "Created Event {0} which happens at {1}".format(self.nextid, date)
            self.nextid += 1
            return msg
        elif etype == 'other':
            raid = cstring.split('at')[0].strip()
            date = cstring.split('at')[1].strip()
            self.events.append(
                {'id': self.nextid, 'raid': raid, 'time': date, 'tobject': parser.parse(date), 'server': server,
                 'signups': {}})
            msg = "Created Event {0} which happens at {1}".format(self.nextid, date)
            self.nextid += 1
            return msg

    def whatsneeded(self, id):
        event = 0
        for item in self.events:
            if item['id'] == id:
                event = item
        if event == 0:
            return "No event by that ID."
        elif 'party' not in event:
            return "That event doesn't have a party makeup defined."
        else:
            return "Roles Required\n   Tanks: {0}\n   DPS: {1}\n   Healers: {2}".format(event['party']['Tank'],
                                                                                        event['party']['DPS'],
                                                                                        event['party']['Healer'])

    def whosgoing(self, id):
        event = 0
        for item in self.events:
            if item['id'] == id:
                event = item
        if event == 0:
            return "No event by that ID."
        elif len(event['signups']) == 0:
            return "No signups for that event yet."
        else:
            message = "Signups for Event {0}\n".format(id)
            if 'savage' in event:
                message += "{0}{1}\n".format(event['raid'], '\bSavage' if event['savage'] else '')
            elif 'mode' in event:
                message += "{0} {1}\n".format(event['raid'], event['mode'])
            else:
                message += "{0}\n".format(event['raid'])
            for person in event['signups']:
                message += "{0}-{1}-{2}".format(person['name'], person['class'] if 'class' in person or 'N/A',
                                                person['role'] if 'role' in person or 'N/A')
            return message

    def signup(self, id, name, role, cls):
        event = 0
        for item in self.events:
            if item['id'] == id:
                event = item
        if event == 0:
            return "No event by that ID."
        elif event['party'][role] == 0:
            return "This event already has enough {0}".format(role)
        else:
            event['party'][role] -= 1
            event['signups'][name] = {'role': role, 'class': cls}
            return "Signed you up as a {0} for event {1}".format(role, event['raid'])

    def events(self):
        message = "Current Events ->\n"
        for item in self.events:
            if 'savage' in item:
                message += "Event {0} is on {1} for {2}{3}".format(item['id'], item['time'], item['raid'],
                                                                   '\bSavage' if item['savage'] else '')
            elif 'mode' in item:
                message += "Event {0} is on {1} for {2} {3}".format(item['id'], item['time'], item['raid'],
                                                                    item['mode'])
            else:
                message += "Event {0} is on {1} for {2}".format(item['id'], item['time'], item['raid'])
        return message
