from framework.test_framework import *
from framework.spoof_factory import *

@test
def test_basic_spoof_setup():
    spoof = setup_basic_spoof()
    expect_equal(len(spoof.users), 2, "Users were not correctly initialized.")
    expect_equal(len(spoof.guild_channels), 1, "Guild channels were not correctly initialized.")
    expect_equal(spoof.users[0].display_name, "beckett", "Beckett was not initialized, or has the wrong name.")
    expect_equal(spoof.users[1].display_name, "vykos", "Vykos was not initialized, or has the wrong name.")

def run_tests():
    test_basic_spoof_setup()
