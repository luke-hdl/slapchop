from framework.test_framework import *
from src.utils import *

@test
def test_input_equality():
    expect(equal_inputs("vampire", "vampire"), "Exact equality not functional.")
    expect(equal_inputs("vampire", " vampire "), "Trimmed equality not functional.")
    expect(equal_inputs("vampire", "Vampire"), "Case equality not functional.")
    expect(equal_inputs("vampire", " VAMPire "), "Trimmed equality with case differences not functional.")
    expect_not(equal_inputs("vampire", "werewolf"), "Inequality not functional.")
    expect_not(equal_inputs("vampire", None), "Inequality with None not functional.")
    expect(equal_inputs(None, None), "Equality with None not functional.")

@test
def test_input_list_equality():
    expect(equal_input_to_one_of_list("vampire", ["vampire", "werewolf", "mage"]), "Basic list inclusion not functional.")
    expect(equal_input_to_one_of_list("vampire", ["werewolf", " vamPire", "mage"]), "Complicated list inclusion not functional.")
    expect(equal_input_to_one_of_list("vampire", [None, "vampire", "werewolf", "mage"]), "Basic list with None inclusion not functional.")
    expect_not(equal_input_to_one_of_list("vampire", ["fae", "werewolf", "mage"]), "Basic list disinclusion not functional.")
    expect_not(equal_input_to_one_of_list("vampire", []), "Empty list disinclusion not functional.")
    expect_not(equal_input_to_one_of_list("vampire", [None, "werewolf"]), "List with None disinclusion not functional.")

def run_tests():
    test_input_equality()
    test_input_list_equality()