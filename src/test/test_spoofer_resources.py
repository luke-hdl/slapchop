from .framework.test_framework import *
from .framework.spoof_factory import *

spoof = None

@test
async def test_basic_spoof_setup():
    global spoof
    spoof = setup_basic_spoof()
    expect_equal(len(spoof.users), 2, "Users were not correctly initialized.")
    expect_equal(len(spoof.guild_channels), 1, "Guild channels were not correctly initialized.")
    expect_equal(spoof.users[0].display_name, "beckett", "Beckett was not initialized, or has the wrong name.")
    expect_equal(spoof.users[1].display_name, "vykos", "Vykos was not initialized, or has the wrong name.")

@test
async def send_a_basic_spoofed_message():
    beckett = spoof.users[0]
    vykos = spoof.users[1]
    channel = spoof.guild_channels[0]
    message = Message(beckett, channel, "hello, " + vykos.mention, [vykos])
    await channel.spoof_send(message, None)
    expect_equal(len(channel.message_history), 1, "Failed to save message.")


async def run_tests():
    await test_basic_spoof_setup()
    await send_a_basic_spoofed_message()
