import time

class SpoofCord:
    def __init__(self, users, guild_channels, clients):
        self.guild_channels = guild_channels
        self.users = users

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
        self.mention = "<" + str(int(hash(display_name))) + ">" #we use a different means for these

    def send(self, message):
        self.channel.send(message)

class Channel:
    def __init__(self, guild):
        self.guild = guild
        self.message_history = []

    def send(self, message):
        message_history.append(RecordedMessage(message))

class Guild:
    def __init__(self):
        pass #further details may be needed later: right now we only check if guild is None
