from spoof_factory import *
from test_framework import *

@test
def basic_spoof_framework_sets_up_correctly():
    spoof = setup_basic_spoof()
    expect(len(spoof.users), 2, "Failed to create the correct number of users.")
    expect(len(spoof.guild_channels), 1, "Failed to create the correct number of channels.")

basic_spoof_framework_sets_up_correctly()
