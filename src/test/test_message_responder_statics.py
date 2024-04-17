from .framework.test_framework import *
from .framework.spoof_factory import *
from run.message_responder import MessageResponder

spoof = None
responder = None

@test
async def set_up_spoof():
    global spoof, responder
    spoof = setup_basic_spoof()
    responder = MessageResponder(99999, spoof.client)

@test
async def responder_test_basic_static():
    beckett = spoof.users[0]
    channel = spoof.guild_channels[0]
    message = Message(beckett, channel, spoof.client.user.mention + " static", [spoof.client.user])
    await channel.spoof_send(message, responder)
    expect(len(channel.message_history) >= 2, "A message back was not received.")
    expect(channel.message_history[1].content.startswith(beckett.mention + ", you"), "Something other than a static occurred. Message: " + channel.message_history[1].content)

@test
async def responder_test_static_from_bot():
    channel = spoof.guild_channels[0]
    channel.message_history = []
    beckett = spoof.users[0]
    beckett.bot = True #oh no robo beckett
    message = Message(beckett, channel, spoof.client.user.mention + " static", [spoof.client.user])
    await channel.spoof_send(message, responder)
    expect(len(channel.message_history) == 1, "Robots shouldn't get a response - even if they're Gangrel.")
    
@test
async def responder_test_statistical_bias():
    wins = 0
    losses = 0
    ties = 0
    tries = 0
    beckett = spoof.users[0]
    beckett.bot = False #he's cured :)
    while tries < 1000:
        tries += 1
        channel = spoof.guild_channels[0]
        message = Message(beckett, channel, spoof.client.user.mention + " static", [spoof.client.user])
        await channel.spoof_send(message, responder)
        response = channel.message_history[-1].content
        if "won" in response:
            wins += 1
        elif "lost" in response:
            losses += 1
        elif "tied" in response:
            ties += 1
        else:
            error("An unknown response was recieved: " + response)
    expect(wins > 275, "Unusually low win rate detected. Wins: " + str(wins))
    expect(ties > 275, "Unusually low tie rate detected. Ties: " + str(ties))
    expect(losses > 275, "Unusually low loss rate detected. Losses: " + str(losses))
    log("Results: {}-{}-{}".format(wins, ties, losses))

async def run_tests():
    await set_up_spoof()
    await responder_test_basic_static()
    await responder_test_static_from_bot()
    await responder_test_statistical_bias()
