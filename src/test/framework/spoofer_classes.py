import time
import re

player_mention_map = {}
client = None

class SpoofCord:
    def __init__(self, users, guild_channels, new_client):
        global client
        self.guild_channels = guild_channels
        self.users = users
        self.client = new_client
        client = new_client

class Client:
    def __init__(self, user):
        self.user = user

class Message:
    def __init__(self, author, channel, content, mentions):
        self.author = author
        self.channel = channel
        self.content = content
        self.mentions = mentions

class RecordedMessage: #no discord equivalent; used to store the channel buffer
    def __init__(self, message):
        self.author = message.author
        self.content = message.content
        self.mentions = message.mentions
        self.post_time = time.time()
        
class User:
    def __init__(self, display_name):
        self.channel = Channel(None)
        self.display_name = display_name
        self.mention = "<" + str(int(hash(display_name))) + ">"
        player_mention_map[self] = self.mention

    async def send(self, message):
        self.channel.send(message)

class Channel:
    def __init__(self, guild):
        self.guild = guild
        self.message_history = []

    async def spoof_send(self, message, responder):
        self.message_history.append(RecordedMessage(message))
        if responder is not None:
            await responder.on_message(message)

    async def send(self, message_text):
        mentions = []
        for string in re.split("[ \t]{1,1000}", message_text):
            if string in player_mention_map:
                mentions.append(player_mention_map[string])
        message = Message(client.user, self, message_text, mentions)
        self.message_history.append(RecordedMessage(message))

class Guild:
    def __init__(self):
        pass #further details may be needed later: right now we only check if guild is None
