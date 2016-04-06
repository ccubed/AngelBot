class AngelMusic:

    def __init__(self, client):
        try:
            self.voice = client.join_voice_channel('Music')
        except InvalidArgument:
            self.voice = 0
            self.error = "Not a Voice Channel"
        except asyncio.TimeoutError:
            self.voice = 0
            self.error = "Timed out on connection"
        except ClientException:
            self.error = "Already connected to a voice channel"
        except OpusNotLoaded:
            self.voice = 0
            self.error = "Couldn't find lib opus. Try loading manually?"

    def ytplay(self, url):
        try:
            self.stream = self.voice.create_ytdl_player(url)
        except ClientException:
            return 0
        else:
            return 1

    def play(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()