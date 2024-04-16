from framework.test_framework import *
from framework.spoof_factory import *
from src.message_responder import MessageResponder

spoof = None
responder = None

@test
async def set_up_spoof():
    global spoof, responder
    spoof = setup_basic_spoof()
    responder = MessageResponder(99999, spoof.client)

@test
async def responder_process_static():
    beckett = spoof.users[0]
    channel = spoof.guild_channels[0]
    message = Message(beckett, channel, spoof.client.user.mention + " static", [spoof.client.user]) #We don't actually spoof mentions correctly... I'll update that later if needed.
    await channel.spoof_send(message, responder)
    expect(len(channel.message_history) >= 2, "A message back was not received.")
    expect(channel.message_history[1].content.startswith(beckett.mention + ", you"), "Something other than a static occurred. Message: " + channel.message_history[1].content)

async def run_tests():
    await set_up_spoof()
    await responder_process_static()
