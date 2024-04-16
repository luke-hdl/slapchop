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
async def spoof_a_basic_challenge():
    beckett = spoof.users[0]
    vykos = spoof.users[1]
    channel = spoof.guild_channels[0]
    message = Message(beckett, channel, spoof.client.user.mention + " challenge " + vykos.mention, [spoof.client.user, vykos])
    await channel.spoof_send(message, responder)
    expect(len(channel.message_history) > 1, "SlapChop didn't respond to the challenge in the guild channel.")
    expect(channel.message_history[-1].content.startswith("Your challenge was successfully created!"), "SlapChop responded incorrectly. Expected successful challenge creation. Received: " + channel.message_history[-1].content)
    expect(len(beckett.channel.message_history) > 0, "Beckett didn't receive a message letting him know about his challenge.")
    expect(len(vykos.channel.message_history) > 0, "Vykos didn't receive a message letting them know about Beckett's challenge.")

    await beckett.channel.spoof_send(Message(beckett, beckett.channel, "rock", []), responder)
    expect(len(beckett.channel.message_history) == 3, "Beckett didn't get a reply back when he threw rock.")
    await beckett.channel.spoof_send(Message(beckett, beckett.channel, "No", []), responder)
    expect(len(beckett.channel.message_history) == 5, "Beckett didn't get a reply back when he declined to bid.")

    await vykos.channel.spoof_send(Message(vykos, vykos.channel, "rock", []), responder)
    expect(len(vykos.channel.message_history) == 3, "Vykos didn't get a reply back when they threw rock.")
    await vykos.channel.spoof_send(Message(vykos, vykos.channel, "No", []), responder)
    expect(len(vykos.channel.message_history) == 6, "Vykos declining to bid didn't complete the challenge.")
    expect(len(beckett.channel.message_history) == 6, "Beckett wasn't alerted that the challenge was done.")
    expect(len(channel.message_history) == 3, "Challenge results weren't posted.")
    expect(vykos in channel.message_history[-1].mentions, "Vykos wasn't mentioned in the challenge results.")
    expect(beckett in channel.message_history[-1].mentions, "Beckett wasn't mentioned in the challenge results.")

async def run_tests():
    await set_up_spoof()
    await spoof_a_basic_challenge()
