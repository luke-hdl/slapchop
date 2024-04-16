from .spoofer_classes import *

def setup_basic_spoof():
    users = [User("beckett"), User("vykos")]
    channels = [Channel(Guild())]
    client = Client(User("slapchop"))
    return SpoofCord(users, channels, client)
