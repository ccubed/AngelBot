import datetime
from dateutil import parser
from globals import *
import json


class Events():
    def __init__(self):
        file = open("Events_config.json", mode="r")
        self.config = json.load(file)
        file.close()
        self.commands = [['events', self.listevents], ['raid', self.create], ['roulette', self.create],
                         ['trial', self.create], ['other', self.create], ['join', self.signup],
                         ['wn', self.whatsneeded], ['who', self.whosgoing]]

    def create(self, message):
        etype = message.content.split(" ")[0].split("$")[1]
        cstring = message.content[len(etype) + 2:]
        nextid = self.config['ID']
        self.config['ID'] += 1
        if etype == 'raid':
            raid = cstring.split('at')[0].strip()
            if 'for' in cstring:
                time = cstring.split('at')[1].split('for')[0].strip()
                stage = cstring.split('for')[1].strip()
                self.config['Events'].append(
                    {'id': nextid, 'raid': raid.split('savage')[0].strip() if 'savage' in raid else raid,
                     'savage': 1 if 'savage' in raid else 0, 'stage': stage, 'time': time,
                     'tobject': parser.parse(time), 'server': message.server, 'party': parties['full'],
                     'signups': {}})
                msg = "Created Event {0} which happens at {1}".format(nextid, time)
                return msg
            else:
                time = cstring.split('at')[1].strip()
                self.config['Events'].append(
                    {'id': nextid, 'raid': raid.split('savage')[0].strip() if 'savage' in raid else raid,
                     'savage': 1 if 'savage' in raid else 0, 'time': time,
                     'tobject': parser.parse(time), 'server': message.server, 'party': parties['full'],
                     'signups': {}})
                msg = "Created Event {0} which happens at {1}".format(nextid, time)
                return msg
        elif etype == 'roulette':
            raid = cstring.split('at')[0].strip()
            date = cstring.split('at')[1].strip()
            self.config['Events'].append(
                {'id': nextid, 'raid': raid, 'time': date, 'tobject': parser.parse(date), 'server': message.server,
                 'party': parties['light'], 'signups': {}})
            msg = "Created Event {0} which happens at {1}".format(nextid, date)
            return msg
        elif etype == 'trial':
            raid = cstring.split('at')[0].strip()
            date = cstring.split('at')[1].split('for')[0].strip()
            mode = cstring.split('for')[1].strip()
            self.config['Events'].append(
                {'id': nextid, 'raid': raid, 'time': date, 'tobject': parser.parse(date), 'server': message.server,
                 'party': parties['light'] if mode == 'normal' else parties['full'], 'signups': {}, 'mode': mode})
            msg = "Created Event {0} which happens at {1}".format(nextid, date)
            return msg
        elif etype == 'other':
            raid = cstring.split('at')[0].strip()
            date = cstring.split('at')[1].strip()
            self.config['Events'].append(
                {'id': nextid, 'raid': raid, 'time': date, 'tobject': parser.parse(date), 'server': message.server,
                 'signups': {}})
            msg = "Created Event {0} which happens at {1}".format(nextid, date)
            return msg

    def whatsneeded(self, message):
        event = 0
        eid = message.content[4:]
        for item in self.config['Events']:
            if item['id'] == eid:
                event = item
        if event == 0:
            return "No event by that ID."
        elif message.server != event['server']:
            return "That's not your server's event."
        elif 'party' not in event:
            return "That event doesn't have a party makeup defined."
        else:
            return "Roles Required\n   Tanks: {0}\n   DPS: {1}\n   Healers: {2}".format(event['party']['Tank'],
                                                                                        event['party']['DPS'],
                                                                                        event['party']['Healer'])

    def whosgoing(self, message):
        event = 0
        eid = message.content[5:]
        for item in self.config['Events']:
            if item['id'] == eid:
                event = item
        if event == 0:
            return "No event by that ID."
        elif message.server != event['server']:
            return "That's not your server's event."
        elif len(event['signups']) == 0:
            return "No signups for that event yet."
        else:
            message = "Signups for Event {0}\n".format(eid)
            if 'savage' in event:
                message += "{0}{1}\n".format(event['raid'], '\bSavage' if event['savage'] else '')
            elif 'mode' in event:
                message += "{0} {1}\n".format(event['raid'], event['mode'])
            else:
                message += "{0}\n".format(event['raid'])
            for person in event['signups']:
                message += "{0}-{1}-{2}".format(person,
                                                event['signups'][person]['class'] if 'class' in event['signups'][
                                                    person] else 'N/A',
                                                event['signups'][person]['role'] if 'role' in event['signups'][
                                                    person] else 'N/A')
            return message

    def signup(self, message):
        event = 0
        if 'as' in message.content:
            eid = message.content[6:].split('as')[0]
            role = message.content[6:].split('as')[1].split('with')[0]
            cls = message.content[6:].split('as')[1].split('with')[1]
            for item in self.config['Events']:
                if item['id'] == eid:
                    event = item
            if event == 0:
                return "No event by that ID."
            elif message.server != event['server']:
                return "That's not your server's event."
            elif event['party'][role] == 0:
                return "This event already has enough {0}".format(role)
            else:
                event['party'][role] -= 1
                event['signups'][message.author.name] = {'role': role, 'class': cls, 'dcuserobj': message.author}
                return "Signed you up as a {0} for event {1}".format(role, event['raid'])
        else:
            eid = message.content[6:]
            for item in self.config['Events']:
                if item['id'] == eid:
                    event = item
            if event == 0:
                return "No event by that ID."
            elif message.server != event['server']:
                return "That's not your server's event."
            else:
                event['signups'][message.author.name] = {'dcuserobj': message.author}
                return "Signed you up for event {0}.".format(event['raid'])

    def listevents(self, message):
        server_events = []
        for item in self.config['Events']:
            if item['server'] == message.server:
                server_events.append(item)
        message = "Current Events ->\n"
        if len(server_events):
            for item in self.config['Events']:
                if item['server'] == message.server:
                    if 'savage' in item:
                        message += "Event {0} is on {1} for {2}{3}".format(item['id'], item['time'], item['raid'],
                                                                           '\bSavage' if item['savage'] else '')
                    elif 'mode' in item:
                        message += "Event {0} is on {1} for {2} {3}".format(item['id'], item['time'], item['raid'],
                                                                            item['mode'])
                    else:
                        message += "Event {0} is on {1} for {2}".format(item['id'], item['time'], item['raid'])
        else:
            message += "None currently."
        return message

    def exit(self):
        try:
            file = open("Events_config.json", mode="w")
        except IOError:
            return 0
        else:
            json.dump(obj=self.config, fp=file, indent=2)
            file.close()
            return 1
