import discord
from message_responder import MessageResponder

TOKEN = 'YOURTOKEN'
TIMEOUT = 1200  # in seconds

intents = discord.Intents.default()
client = discord.Client(intents=intents)
message_responder = MessageResponder(TIMEOUT, client)
@client.event
async def on_ready():
    await message_responder.on_ready()

@client.event
async def on_message(message):
    await message_responder.on_message(message)

client.run(TOKEN)
