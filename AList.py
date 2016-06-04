import time
import aiohttp
from datetime import timedelta
import json
import encryption
from secret import *
from AList_ProfileProcessor import profile_preprocessor
import random


class AList:
    def __init__(self, redis):
        self.apiurl = "https://anilist.co/api"
        self.commands = [['awaifu', self.waifu], ['ahusbando', self.husbando], ['acharacter', self.searchcharacter],
                         ['acurrent', self.currentanime], ['aanime', self.searchanime], ['amanga', self.searchmanga],
                         ['auser', self.get_user], ['anotifications', self.get_notifications], ['apeople', self.user_search],
                         ['afollow', self.follow_user], ['anilist', self.get_anime_list], ['amangalist', self.get_manga_list],
                         ['awatch', self.mark_to_watch], ['anext', self.mark_one_up], ['awatching', self.get_watching],
                         ['areading', self.get_reading], ['aread', self.mark_to_read]]
        self.pools = redis
        self.events = [[self.get_readonly, 0]]
        self.enc = encryption.AESCipher(cryptokey)
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'AngelBot (aiohttp 0.21.6 python 3.5.1)'}

    def get_readonly(self, loop):
        loop.create_task(self._get_readonly())
        loop.call_later(3500, self.get_readonly, loop)

    async def _get_readonly(self):
        async with self.pools.get() as pool:
            cid = await pool.hget("AniList", "ClientID")
            csecret = await pool.hget("AniList", "ClientSecret")
            data = {'grant_type': 'client_credentials', 'client_id': cid,
                    'client_secret': csecret}
            url = self.apiurl + "/auth/access_token"
            with aiohttp.ClientSession() as session:
                async with session.post(url, params=data) as response:
                    jsd = await response.json()
                    await pool.hset("ALReadOnly", "Expiration", jsd['expires'])
                    await pool.hset("ALReadOnly", "AccessToken", jsd['access_token'])

    async def get_oauth(self, id):
        async with self.pools.get() as dbp:
            test = await dbp.exists(id)
            if test:
                test = await dbp.hexists(id, "Anilist_Expires")
                if test:
                    expiration = await dbp.hget(id, "Anilist_Expires")
                    if int(expiration) < time.time():
                        refresh = await dbp.hget(id, "Anilist_Refresh")
                        cid = await dbp.hget("AniList", "ClientID")
                        csec = await dbp.hget("AniList", "ClientSecret")
                        params = {'grant_type': 'refresh_token', 'client_id': cid, 'client_secret': csec, 'refresh_token': refresh}
                        with aiohttp.ClientSession() as session:
                            async with session.post("https://anilist.co/api/auth/access_token", params=params) as response:
                                text = await response.text()
                                if text == "\n" or response.status == 404:
                                    return 0
                                else:
                                    jsd = json.loads(text)
                                    await dbp.hset(id, "Anilist_Expires", jsd['expires'])
                                    await dbp.hset(id, "Anilist_Token", self.enc.encrypt(jsd['access_token']))
                                    return jsd['access_token']
                    else:
                        atoken = await dbp.hget(id, "Anilist_Token")
                        return self.enc.decrypt(atoken).decode()
                else:
                    return 0
            else:
                return 0

    async def set_aid(self, message):
        if len(message.content.split(" ")) == 1:
            return "Need to provide a username or user id to set your AniList ID."
        uid = " ".join(message.content.split(" ")[1:])
        async with self.pools.get() as pool:
            token = await pool.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            url = self.apiurl + "/user/" + uid
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    text = await response.text()
                    if text == "\n" or response.status == 404:
                        return "Not a valid username or user id."
                    else:
                        jsd = json.loads(text)
                        await pool.hset(message.author.id, "Anilist_ID", jsd['id'])
                        return "Set your AniList ID to <https://anilist.co/user/{0}>".format(jsd['id'])

    async def waifu(self, message):
        name = "%20".join(message.content.split(" ")[1:])
        async with self.pools.get() as pool:
            token = await pool.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            if name.isdigit():
                url = self.apiurl + "/character/" + str(name)
            else:
                url = self.apiurl + "/character/search/" + name
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    text = await response.text()
                    if response.status == 404 or text == "\n":
                        return "What character? You don't even know the name of your waifu? The shame."
                    jsd = json.loads(text)
                    if isinstance(jsd, list) and len(jsd) > 0:
                        jsd = jsd[0]
                    elif isinstance(jsd, list) and len(jsd) == 0:
                        print("[" + jsd + "\n" + response.status + "]")
                    whc = "{0} confesses their undying devotion to their waifu {1}{2}!\n{3}".format(message.author.name,
                                                                                                    jsd['name_first'],
                                                                                                    ' ' + jsd['name_last'] if jsd['name_last'] is not None else '',
                                                                                                    jsd['image_url_med'])
                    return whc

    async def husbando(self, message):
        name = "%20".join(message.content.split(" ")[1:])
        async with self.pools.get() as pool:
            token = await pool.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            if name.isdigit():
                url = self.apiurl + "/character/" + str(name)
            else:
                url = self.apiurl + "/character/search/" + name
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    text = await response.text()
                    if text == "\n" or response.status == 404:
                        return "What character? You don't even know the name of your husbando? The shame."
                    jsd = json.loads(text)
                    if isinstance(jsd, list) and len(jsd) > 0:
                        jsd = jsd[0]
                    elif isinstance(jsd, list) and len(jsd) == 0:
                        print("[" + jsd + "\n" + response.status + "]")
                    whc = "{0} confesses their undying devotion to their husbando {1}{2}!\n{3}".format(message.author.name,
                                                                                               jsd['name_first'],
                                                                                               ' ' + jsd['name_last'] if jsd['name_last'] is not None else '',
                                                                                               jsd['image_url_med'])
                    return whc

    async def searchcharacter(self, message):
        name = "%20".join(message.content.split(" ")[1:])
        if name.isdigit():
            return await self.parsecharacter(name)
        async with self.pools.get() as pool:
            token = await pool.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            url = self.apiurl + "/character/search/" + name.replace(' ', '%20')
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    text = await response.text()
                    if text == '\n' or response.status == 404:
                        return "[ANILIST] No results for a character named {0} in Anilist.".format(name)
                    else:
                        jsd = json.loads(text)
                        if len(jsd) > 1:
                            msg = "Found these characters ->\n"
                            for i in jsd:
                                msg += " {0}{1} (ID: {2})\n".format(i['name_first'], '\b' + i.get('name_last', ''), i['id'])
                            return msg
                        elif len(jsd) == 1:
                            return await self.parsecharacter(jsd[0]['id'])

    async def parsecharacter(self, id):
        async with self.pools.get() as pool:
            token = await pool.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            url = self.apiurl + "/character/" + str(id)
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    jsd = await response.json()
                    return " {0} {1}\nInfo: {2}\n{3}".format(jsd['name_first'], jsd.get('name_last', ''),
                                                            jsd['info'], jsd['image_url_med'])

    async def searchanime(self, message):
        name = "%20".join(message.content.split(" ")[1:])
        if name.isdigit():
            return await self.parseanime(name)
        async with self.pools.get() as pool:
            token = await pool.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            url = self.apiurl + "/anime/search/" + name.replace(' ', '%20')
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    text = await response.text()
                    if text == '\n' or response.status == 404:
                        return "[ANILIST] No results found on Anilist for Anime {0}".format(name.replace("%20", " "))
                    else:
                        jsd = json.loads(text)
                        if len(jsd) > 1:
                            msg = "Found these Anime ->\n"
                            for i in jsd:
                                msg += " {0} (ID: {1})\n".format(i['title_english'], i['id'])
                            return msg
                        elif len(jsd) == 1:
                            return await self.parseanime(jsd[0]['id'])

    async def parseanime(self, id):
        async with self.pools.get() as pool:
            token = await pool.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            url = self.apiurl + "/anime/" + str(id)
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    jsd = await response.json()
                    return "Titles\n English: {0}\n Romaji: {1}\n Japanese: {2}\nStatus: {3}\n{4}\nAverage Score: {5}\nGenres: {6}\nDescriptions: {7}\n{8}".format(
                        jsd['title_english'], jsd['title_romaji'], jsd['title_japanese'],
                        jsd['airing_status'], 'Episode {0} in {1}'.format(jsd['airing']['next_episode'], str(timedelta(seconds=jsd['airing']['countdown']))) if jsd['airing_status'].lower() == 'currently airing' else 'Episodes: {0}'.format(jsd['total_episodes']),
                        jsd['average_score'], ', '.join(jsd['genres']), jsd['description'].replace('<br>', '\n'),
                        jsd['image_url_med'])

    async def currentanime(self, message):
        async with self.pools.get() as pool:
            token = await pool.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token, 'status': 'Currently Airing',
                    'sort': 'popularity-desc', 'year': '2016'}
            url = self.apiurl + "/browse/anime"
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    jsd = await response.json()
                    msg = "Currently Airing Popular Anime ->\n"
                    for item in jsd[0:10]:
                        msg += " {0}: {1}\n".format(item['title_english'], item['id'])
                    return msg

    async def searchmanga(self, message):
        name = "%20".join(message.content.split(" ")[1:])
        if name.isdigit():
            return await self.parsemanga(name)
        async with self.pools.get() as pool:
            token = await pool.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            url = self.apiurl + "/manga/search/" + name.replace(' ', '%20')
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    text = await response.text()
                    if response.text() == "\n" or response.status == 404:
                        return "[ANILIST] No results found for {0} in Manga.".format(name)
                    else:
                        jsd = json.loads(text)
                        if len(jsd) == 1:
                            return await self.parsemanga(jsd[0]['id'])
                        elif len(jsd) > 1:
                            msg = "Found these Manga ->\n"
                            for i in jsd:
                                msg += " {0} (ID: {1})\n".format(i['title_english'], i['id'])
                            return msg

    async def parsemanga(self, id):
        async with self.pools.get() as pool:
            token = await pool.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            url = self.apiurl + "/manga/" + str(id)
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    jsd = await response.json()
                    return "Titles\n English: {0}\n Romaji: {1}\n Japanese: {2}\nStatus: {3}\nLength: {4} volumes and {5} chapters\nAverage Score: {6}\nGenres: {7}\nDescriptions: {8}\n{9}".format(
                        jsd['title_english'], jsd['title_romaji'], jsd['title_japanese'],
                        jsd['publishing_status'], jsd['total_volumes'], jsd['total_chapters'],
                        jsd['average_score'], ','.join(jsd['genres']), jsd['description'],
                        jsd['image_url_med'])

    async def get_user(self, message):
        url = self.apiurl + "/user"
        if len(message.content.split(" ")) == 1:
            key = await self.get_oauth(message.author.id)
            if key == 0:
                return "I can't pull your details from AniList because you haven't verified your account. PM me about anilist to do that."
            else:
                header = self.headers
                header['Authorization'] = 'Bearer {0}'.format(key)
                with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=header) as response:
                        text = await response.text()
                        if response.status == 404 or text == "\n":
                            return "Anilist says you don't exist."
                        else:
                            jsd = json.loads(text)
                            about = await profile_preprocessor(jsd['about'])
                            ret = "{0} ({1})\n{2} Pending Notifications.\n{3}\n\nI've spent {4} on Anime and read {5} Manga Chapters.\n{6}".format(jsd['display_name'], jsd['id'], jsd['notifications'], about, str(timedelta(minutes=jsd['anime_time'])), jsd['manga_chap'], jsd['image_url_lge'])
                            if len(ret) > 2000:
                                return "{0} ({1})\n{2} Pending Notifications.\n{3}\n\nI've spent {4} on Anime and read {5} Manga Chapters.\n{6}".format(jsd['display_name'], jsd['id'], jsd['notifications'], "Attempt to parse novel failed. Visit <http://anilist.co/user/{0}> to view about section.".format(jsd['display_name']), str(timedelta(minutes=jsd['anime_time'])), jsd['manga_chap'], jsd['image_url_lge'])
                            else:
                                return ret
        else:
            name = "%20".join(message.content.split(" ")[1:])
            async with self.pools.get() as dbp:
                token = await dbp.hget("ALReadOnly", "AccessToken")
                data = {'access_token': token}
                url = url + "/" + name
                with aiohttp.ClientSession() as session:
                    async with session.get(url, params=data) as response:
                        if response.status in [403, 401]:
                            return "Your profile is private."
                        elif response.status == 404:
                            return "No user found by name {0}".format(name)
                        else:
                            text = await response.text()
                            if text == "\n":
                                return "No user found by name {0}".format(name)
                            else:
                                jsd = json.loads(text)
                                about = await profile_preprocessor(jsd['about'])
                                ret = "{0} ({1})\n{2}\n\nI've spent {3} on Anime and read {4} Manga Chapters.\n{5}".format(jsd['display_name'], jsd['id'], about, str(timedelta(minutes=jsd['anime_time'])), jsd['manga_chap'], jsd['image_url_lge'])
                                if len(ret) > 2000:
                                    return "{0} ({1})\n{2} Pending Notifications.\n{3}\n\nI've spent {4} on Anime and read {5} Manga Chapters.\n{6}".format(jsd['display_name'], jsd['id'], jsd['notifications'], "Attempt to parse novel failed. Visit <http://anilist.co/user/{0}> to view about section.".format(jsd['display_name']), str(timedelta(minutes=jsd['anime_time'])), jsd['manga_chap'], jsd['image_url_lge'])
                                else:
                                    return ret

    async def get_notifications(self, message):
        url = self.apiurl + "/user/notifications"
        key = await self.get_oauth(message.author.id)
        if key == 0:
            return "Notifications require you to verify your account with Oauth. PM me about anilist to do that."
        else:
            header = self.headers
            header['Authorization'] = 'Bearer {0}'.format(key)
            with aiohttp.ClientSession() as session:
                async with session.get(url, headers=header) as response:
                    text = await response.text()
                    if text == "\n" or response.status == 404:
                        return "Something went wrong. I wasn't able to get your notifications."
                    else:
                        jsd = json.loads(text)
                        msg = "Notifications ->\n"
                        for item in jsd:
                            msg += "{0}({1}) {2}".format(item['user']['display_name'], item['user']['id'], item['value'])
                            if 'thread' in item:
                                msg += " {0}({1})".format(item['thread']['title'], item['thread']['id'])
                            msg += "\n"
                        return msg

    async def follow_user(self, message):
        url = self.apiurl + "/user/follow"
        key = await self.get_oauth(message.author.id)
        if len(message.content.split(" ")) == 1:
            return "Need a user id."
        else:
            uid = "%20".join(message.content.split(" ")[1:])
            if not uid.isdigit():
                uid = self.get_user_id(uid)
                if uid == 0:
                    return "Couldn't narrow that down to one user."
            header = self.headers
            header['Authorization'] = 'Bearer {0}'.format(key)
            with aiohttp.ClientSession() as session:
                async with session.post(url, headers=header, data=json.dumps({'id': uid})) as response:
                    text = await response.text()
                    if response.text == "\n" or response.status == 404:
                        return "Encountered an error following that user."
                    elif response.status in [401, 403]:
                        return "I'm not authorized to follow that user for you."
                    else:
                        return "You are now following that user."

    async def user_search(self, message):
        async with self.pools.get() as dbp:
            token = await dbp.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            url = self.apiurl + "/user/search/{0}".format(" ".join(message.content.split(" ")[1:])).replace(" ", "%20")
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    text = await response.text()
                    if response.status == 404 or text == "\n":
                        return "No users found."
                    elif response.status in [403, 401]:
                        return "Bot is not authorized."
                    else:
                        jsd = json.loads(text)
                        print(text + "\n" + str(len(jsd)))
                        if isinstance(jsd, list):
                            msg = "Found {0} Users. Here are the first few. =>\n".format(len(jsd))
                            for x in jsd[0:10]:
                                msg += "   {0} ({1})\n".format(x['display_name'], x['id'])
                            return msg
                        else:
                            return "{0} ({1})".format(jsd['display_name'], jsd['id'])

    async def get_user_id(self, id):
        async with self.pools.get() as dbp:
            token = await dbp.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            url = self.apiurl + "/user/search/{0}".format(id)
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    text = await response.text()
                    if response.status == 404 or text == "\n":
                        return 0
                    elif response.status in [403, 401]:
                        return 0
                    else:
                        jsd = json.loads(text)
                        if isinstance(jsd, list) and len(jsd) == 1:
                            return jsd[0]['id']
                        elif isinstance(jsd, list) and len(jsd) > 1:
                            return 0
                        else:
                            return jsd['id']

    async def get_anime_list(self, message):
        url = self.apiurl + "/user/{0}/animelist"
        if len(message.content.split(" ")) == 1:
            return "You didn't provide a username."
        name = "%20".join(message.content.split(" ")[1:])
        async with self.pools.get() as dbp:
            token = await dbp.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            with aiohttp.ClientSession() as session:
                async with session.get(url.format(name), params=data) as response:
                    if response.status == 404:
                        return "User not found"
                    elif response.status in [403, 401]:
                        return "Access denied for that user's AnimeList. Must be private."
                    jsd = await response.json()
                    jsd = jsd['lists'].get('completed', None)
                    if not jsd:
                        return "That user has no completed anime."
                    msg = "{} has watched ->\n".format(name.replace("%20", " ").capitalize())
                    if len(jsd) > 20:
                        pids = []
                        while len(pids) < 20:
                            randid = random.randint(0, len(jsd)-1)
                            if randid not in pids:
                                pids.append(randid)
                        for x in pids:
                            msg += "   {}({}) - {}/{} Episodes Watched and {}\n".format(jsd[x]['anime']['title_english'],
                                                                         jsd[x]['anime']['id'],
                                                                         jsd[x]['episodes_watched'],
                                                                         jsd[x]['anime']['total_episodes'],
                                                                         'scored it {}'.format(jsd[x]['score_raw']) if jsd[x]['score_raw'] != 0 else "not scored.")
                    else:
                        for x in jsd:
                            msg += "   {}({}) - {}/{} Chapters Read and {}\n".format(x['manga']['title_english'],
                                                                                     x['manga']['id'],
                                                                                     x['chapters_read'],
                                                                                     x['manga']['total_chapters'],
                                                                                     "scored it {}".format(jsd[x]['score_raw']) if jsd[x]['score_raw'] != 0 else 'not scored.')
                    return msg

    async def get_manga_list(self, message):
        url = self.apiurl + "/user/{0}/mangalist"
        if len(message.content.split(" ")) == 1:
            return "You didn't provide a username."
        name = "%20".join(message.content.split(" ")[1:])
        async with self.pools.get() as dbp:
            token = await dbp.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            with aiohttp.ClientSession() as session:
                async with session.get(url.format(name), params=data) as response:
                    if response.status == 404:
                        return "User not found."
                    elif response.status in [403, 401]:
                        return "Permission denied for that user's MangaList."
                    jsd = await response.json()
                    jsd = jsd['lists'].get('completed', None)
                    if not jsd:
                        return "That user has no completed Manga."
                    msg = "{} has read ->\n".format(name.replace("%20", " ").capitalize())
                    if len(jsd) > 20:
                        pids = []
                        while len(pids) < 20:
                            randid = random.randint(0, len(jsd)-1)
                            if randid not in pids:
                                pids.append(randid)
                        for x in pids:
                            msg += "   {}({}) - {}/{} Chapters Read and {}\n".format(jsd[x]['manga']['title_english'],
                                                                                jsd[x]['manga']['id'],
                                                                                jsd[x]['chapters_read'],
                                                                                jsd[x]['manga']['total_chapters'],
                                                                                "scored it {}".format(jsd[x]['score_raw']) if jsd[x]['score_raw'] != 0 else 'not scored.')
                    else:
                        for x in jsd:
                            msg += "   {}({}) - {}/{} Chapters Read and {}\n".format(x['manga']['title_english'],
                                                                                     x['manga']['id'],
                                                                                     x['chapters_read'],
                                                                                     x['manga']['total_chapters'],
                                                                                     "scored it {}".format(x['score_raw']) if x['score_raw'] != 0 else 'not scored.')
                    return msg

    async def mark_to_watch(self, message):
        if len(message.content.split(" ")) == 1:
            return "Need an anime."
        name = "%20".join(message.content.split(" ")[1:])
        if name.isdigit():
            url = self.apiurl + "/anime/{}".format(name)
        else:
            url = self.apiurl + "/anime/search/{}".format(name)
        key = await self.get_oauth(message.author.id)
        if key == 0:
            return "This requires OAuth permission for your account. PM me about Anilist to start that."
        async with self.pools.get() as pool:
            token = await pool.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    if response.status == 404:
                        return "No anime by that name."
                    jsd = await response.json()
                    if isinstance(jsd, list):
                        jsd = jsd[0]
                    payload = {'id': jsd['id'], 'list_status': 'plan to watch'}
                    header = self.headers
                    header['Authorization'] = 'Bearer {0}'.format(key)
                    async with session.post(self.apiurl+"/animelist", headers=header, params=payload) as response:
                        if response.status in [403, 401]:
                            return "The bot wasn't authorized to take that action for you."
                        elif response.status == 200:
                            return "I marked {} as Plan to Watch for you.".format(jsd['title_english'])

    async def mark_to_read(self, message):
        if len(message.content.split(" ")) == 1:
            return "Need a manga."
        name = "%20".join(message.content.split(" ")[1:])
        if name.isdigit():
            url = self.apiurl + "/manga/{}".format(name)
        else:
            url = self.apiurl + "/manga/search/{}".format(name)
        key = await self.get_oauth(message.author.id)
        if key == 0:
            return "This requires OAuth permission for your account. PM me about Anilist to start that."
        async with self.pools.get() as pool:
            token = await pool.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            with aiohttp.ClientSession() as session:
                async with session.get(url, params=data) as response:
                    if response.status == 404:
                        return "No manga by that name."
                    jsd = await response.json()
                    if isinstance(jsd, list):
                        jsd = jsd[0]
                    payload = {'id': jsd['id'], 'list_status': 'plan to read'}
                    header = self.headers
                    header['Authorization'] = 'Bearer {0}'.format(key)
                    async with session.post(self.apiurl+"/mangalist", headers=header, params=payload) as response:
                        if response.status in [403, 401]:
                            return "The bot wasn't authorized to take that action for you."
                        elif response.status == 200:
                            return "I marked {} as Plan to Read for you.".format(jsd['title_english'])
                        else:
                            print(await response.text())

    async def mark_one_up(self, message):
        if len(message.content.split(" ")) == 1:
            return "Need to tell me what you read or watched."
        type = message.content.split(" ")[1].split(":")[0]
        what = message.content.split(":")[1].replace(" ", "%20")
        key = await self.get_oauth(message.author.id)
        if key == 0:
            return "This requires you to authenticate your account. PM me about anilist to do that."
        header = self.headers
        header['Authorization'] = 'Bearer {}'.format(key)
        uid = 0
        async with self.pools.get() as dbp:
            token = await dbp.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            with aiohttp.ClientSession() as session:
                async with session.get(self.apiurl+"/user", headers=header) as userdata:
                    jsd = await userdata.json()
                    uid = jsd['id']
                if what.isdigit():
                    if type == "m":
                        async with session.get(self.apiurl+"/user/{}/mangalist".format(uid), params=data) as response:
                            if response.status in [403, 401]:
                                return "Not authorized to access your manga list."
                            current, maxc = 0, 0
                            jsd = await response.json()
                            title = 0
                            for x in jsd['lists']['reading']:
                                if str(x['manga']['id']) == what:
                                    current = x['chapters_read']
                                    maxc = x['manga']['total_chapters'] if x['manga']['publishing_status'] in ['finished', 'cancelled'] else 0
                                    title = x['manga']['title_english']
                                    break
                            payload = {'id': what, 'list_status': 'reading' if current+1 < maxc or maxc == 0 else 'completed', 'chapters_read': current+1}
                            async with session.put(self.apiurl+"/mangalist", headers=header, params=payload) as mangalist:
                                if mangalist.status in [403, 401]:
                                    return "I wasn't authorized to modify that list item."
                                elif mangalist.status == 200:
                                    return "+1'd {}. Now {}.".format(title, "at {} Chapters read.".format(current+1) if payload['list_status'] == 'reading' else 'Completed!')
                    elif type == "a":
                        async with session.get(self.apiurl + "/user/{}/animelist".format(uid), params=data) as response:
                            if response.status in [403, 401]:
                                return "Not authorized to access your anime list."
                            current, maxc = 0, 0
                            jsd = await response.json()
                            title = 0
                            for x in jsd['lists']['watching']:
                                if str(x['anime']['id']) == what:
                                    current = x['episodes_watched']
                                    maxc = x['anime']['total_episodes'] if x['anime']['airing_status'] in ['finished airing', 'cancelled'] else 0
                                    title = x['anime']['title_english']
                                    break
                            payload = {'id': what, 'list_status': 'watching' if current + 1 < maxc or maxc == 0 else 'completed', 'episodes_watched': current + 1}
                            async with session.put(self.apiurl + "/animelist", headers=header, params=payload) as animelist:
                                if animelist.status in [403, 401]:
                                    return "I wasn't authorized to modify that list item."
                                elif animelist.status == 200:
                                    return "+1'd {}. Now {}.".format(title, "at {} Episodes watched".format(current+1) if payload['list_status'] == 'watching' else "Completed")
                    else:
                        return "Unknown type {}. Must be a(nime) or m(anga).".format(type)
                else:
                        if type == 'm':
                            async with session.get(self.apiurl+"/manga/search/{}".format(what), params=data) as response:
                                if response.status == 404:
                                    return "Couldn't find a manga by the name {}".format(what.replace("%20", " "))
                                else:
                                    jsd = await response.json()
                                    if len(jsd) > 1:
                                        return "That search matched {} results. Please use an ID or add more terms to narrow the result.".format(len(jsd))
                                    else:
                                        mid = jsd[0]['id']
                                        maxc = jsd[0]['total_chapters'] if jsd[0]['publishing_status'] in ['finished', 'cancelled'] else 0
                                        title = jsd[0]['title_english']
                                        current = 0
                                        async with session.get(self.apiurl+"/user/{}/mangalist".format(uid), headers=header) as mangalist:
                                            if mangalist.status in [403, 401]:
                                                return "Not authorized to access your manga list."
                                            jsd = await mangalist.json()
                                            for x in jsd['lists']['reading']:
                                                if x['manga']['id'] == mid:
                                                    current = x['chapters_read']
                                                    break
                                            payload = {'id': mid, 'list_status': 'reading' if current + 1 < maxc or maxc == 0 else 'completed', 'episodes_watched': current + 1}
                                            async with session.put(self.apiurl + "/mangalist", headers=header, params=payload) as markup:
                                                if markup.status in [403, 401]:
                                                    return "I wasn't authorized to modify that list item."
                                                elif markup.status == 200:
                                                    return "+1'd {}. Now {}.".format(title, "at {} Chapters read".format(current + 1) if payload['list_status'] == 'reading' else "Completed")
                        elif type == 'a':
                            async with session.get(self.apiurl + "/anime/search/{}".format(what), params=data) as response:
                                if response.status == 404:
                                    return "Couldn't find an anime by the name {}".format(what.replace("%20", " "))
                                else:
                                    jsd = await response.json()
                                    if len(jsd) > 1:
                                        return "That search matched {} results. Please use an ID or add more terms to narrow the result.".format(len(jsd))
                                    else:
                                        mid = jsd[0]['id']
                                        maxc = jsd[0]['total_episodes'] if jsd[0]['airing_status'] in ['finished airing', 'cancelled'] else 0
                                        title = jsd[0]['title_english']
                                        current = 0
                                        async with session.get(self.apiurl + "/user/{}/animelist".format(uid), headers=header) as animelist:
                                            if animelist.status in [403, 401]:
                                                return "Not authorized to access your anime list."
                                            jsd = await animelist.json()
                                            for x in jsd['lists']['watching']:
                                                if x['anime']['id'] == mid:
                                                    current = x['episodes_watched']
                                                    break
                                            payload = {'id': mid, 'list_status': 'watching' if current + 1 < maxc or maxc == 0 else 'completed', 'episodes_watched': current + 1}
                                            async with session.put(self.apiurl + "/animelist", headers=header, params=payload) as markup:
                                                if markup.status in [403, 401]:
                                                    return "I wasn't authorized to modify that list item."
                                                elif markup.status == 200:
                                                    return "+1'd {}. Now {}.".format(title, "at {} Episodes watched".format(current + 1) if payload['list_status'] == 'watching' else "Completed")
                        else:
                            return "Unknown type {}. Must be a(nime) or m(anga).".format(type)

    async def get_watching(self, message):
        if len(message.content.split(" ")) == 1:
            return "Need a username."
        name = "%20".join(message.content.split(" ")[1:])
        async with self.pools.get() as dbp:
            token = await dbp.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            with aiohttp.ClientSession() as session:
                async with session.get(self.apiurl+"/user/{}/animelist".format(name), params=data) as response:
                    if response.status == 404:
                        return "No user by that name or ID."
                    elif response.status in [403, 401]:
                        return "Not authorized to access that user's list."
                    jsd = await response.json()
                    jsd = jsd['lists']['watching']
                    pids = []
                    msg = "{} is currently watching ->\n".format(name.replace("%20", " "))
                    if len(jsd) > 20:
                        while len(pids) < 20:
                            randid = random.randint(0, len(jsd)-1)
                            if randid not in pids:
                                pids.append(randid)
                        for x in pids:
                            msg += "    {}({}) - Last Episode watched was {}\n".format(jsd[x]['anime']['title_english'], jsd[x]['anime']['id'], jsd[x]['episodes_watched'])
                        return msg
                    elif len(jsd) == 0:
                        return "Not watching any Anime."
                    else:
                        for x in jsd:
                            msg += "    {}({}) - Last Episode watched was {}\n".format(x['anime']['title_english'], x['anime']['id'], x['episodes_watched'])
                        return msg

    async def get_reading(self, message):
        if len(message.content.split(" ")) == 1:
            return "Need a username."
        name = "%20".join(message.content.split(" ")[1:])
        async with self.pools.get() as dbp:
            token = await dbp.hget("ALReadOnly", "AccessToken")
            data = {'access_token': token}
            with aiohttp.ClientSession() as session:
                async with session.get(self.apiurl + "/user/{}/mangalist".format(name), params=data) as response:
                    if response.status == 404:
                        return "No user by that name or ID."
                    elif response.status in [403, 401]:
                        return "Not authorized to access that user's list."
                    jsd = await response.json()
                    jsd = jsd['lists']['reading']
                    pids = []
                    msg = "{} is currently reading ->\n"
                    if len(jsd) > 20:
                        while len(pids) < 20:
                            randid = random.randint(0, len(jsd) - 1)
                            if randid not in pids:
                                pids.append(randid)
                        for x in pids:
                            msg += "    {}({}) - Last Chapter read was {}\n".format(jsd[x]['manga']['title_english'], jsd[x]['manga']['id'], jsd[x]['chapters_read'])
                        return msg
                    elif len(jsd) == 0:
                        return "Not reading any Manga."
                    else:
                        for x in jsd:
                            msg += "    {}({}) - Last Chapter read was {}\n".format(x['manga']['title_english'], x['manga']['id'], x['chapters_read'])
                        return msg