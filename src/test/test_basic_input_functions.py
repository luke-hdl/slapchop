from .framework.test_framework import *
from run import *

@test
async def test_input_equality():
    expect(equal_inputs("vampire", "vampire"), "Exact equality not functional.")
    expect(equal_inputs("vampire", " vampire "), "Trimmed equality not functional.")
    expect(equal_inputs("vampire", "Vampire"), "Case equality not functional.")
    expect(equal_inputs("vampire", " VAMPire "), "Trimmed equality with case differences not functional.")
    expect_not(equal_inputs("vampire", "werewolf"), "Inequality not functional.")
    expect_not(equal_inputs("vampire", None), "Inequality with None not functional.")
    expect(equal_inputs(None, None), "Equality with None not functional.")

@test
async def test_input_list_equality():
    expect(equal_input_to_one_of_list("vampire", ["vampire", "werewolf", "mage"]), "Basic list inclusion not functional.")
    expect(equal_input_to_one_of_list("vampire", ["werewolf", " vamPire", "mage"]), "Complicated list inclusion not functional.")
    expect(equal_input_to_one_of_list("vampire", [None, "vampire", "werewolf", "mage"]), "Basic list with None inclusion not functional.")
    expect_not(equal_input_to_one_of_list("vampire", ["fae", "werewolf", "mage"]), "Basic list disinclusion not functional.")
    expect_not(equal_input_to_one_of_list("vampire", []), "Empty list disinclusion not functional.")
    expect_not(equal_input_to_one_of_list("vampire", [None, "werewolf"]), "List with None disinclusion not functional.")

@test
async def test_rps_logic():
    expect(automatically_determine_winner("rock", "scissors") == RecognizedResult.PLAYER_1_WIN, "Rock should beat scissors.")
    expect(automatically_determine_winner("rock", "paper") == RecognizedResult.PLAYER_1_LOSS, "Rock should lose to paper.")
    expect(automatically_determine_winner("rock", "rock") == RecognizedResult.TIE, "Rock should tie itself.")
    expect(automatically_determine_winner("rock", "bomb") == RecognizedResult.PLAYER_1_LOSS, "Rock should lose to bomb.")
    expect(automatically_determine_winner("rock", "candy") == RecognizedResult.UNKNOWN, "Rock should have an unknown result against odd input.")

    expect(automatically_determine_winner("paper", "scissors") == RecognizedResult.PLAYER_1_LOSS, "Paper should lose to scissors.")
    expect(automatically_determine_winner("paper", "paper") == RecognizedResult.TIE, "Paper should tie paper.")
    expect(automatically_determine_winner("paper", "rock") == RecognizedResult.PLAYER_1_WIN, "Paper should beat rock.")
    expect(automatically_determine_winner("paper", "bomb") == RecognizedResult.PLAYER_1_LOSS, "Paper should lose to bomb.")
    expect(automatically_determine_winner("paper", "candy") == RecognizedResult.UNKNOWN, "Paper should have an unknown result against odd input.")

    expect(automatically_determine_winner("scissors", "scissors") == RecognizedResult.TIE, "Scissors should tie itself.")
    expect(automatically_determine_winner("scissors", "paper") == RecognizedResult.PLAYER_1_WIN, "Scissors should beat paper.")
    expect(automatically_determine_winner("scissors", "rock") == RecognizedResult.PLAYER_1_LOSS, "Scissors should lose to rock.")
    expect(automatically_determine_winner("scissors", "bomb") == RecognizedResult.PLAYER_1_WIN, "Scissors should beat bomb.")
    expect(automatically_determine_winner("scissors", "candy") == RecognizedResult.UNKNOWN, "Scissors should have an unknown result against odd input.")

    expect(automatically_determine_winner("bomb", "scissors") == RecognizedResult.PLAYER_1_LOSS, "Bomb should lose to scissors.")
    expect(automatically_determine_winner("bomb", "paper") == RecognizedResult.PLAYER_1_WIN, "Bomb should beat paper.")
    expect(automatically_determine_winner("bomb", "rock") == RecognizedResult.PLAYER_1_WIN, "Bomb should beat rock.")
    expect(automatically_determine_winner("bomb", "bomb") == RecognizedResult.TIE, "Bomb should tie bomb.")
    expect(automatically_determine_winner("bomb", "candy") == RecognizedResult.UNKNOWN, "Rock should have an unknown result against odd input.")

    expect(automatically_determine_winner("rock", "r") == RecognizedResult.TIE, "Aliasing should work for rock.")
    expect(automatically_determine_winner("paper", "p") == RecognizedResult.TIE, "Aliasing should work for paper.")
    expect(automatically_determine_winner("scissors", "s") == RecognizedResult.TIE, "Aliasing should work for scissors.")
    expect(automatically_determine_winner("bomb", "b") == RecognizedResult.TIE, "Aliasing should work for bomb.")

    expect(automatically_determine_winner("candy", "candy") == RecognizedResult.UNKNOWN, "Two unknown inputs are unknown, even if they're the same.")

async def run_tests():
    await test_input_equality()
    await test_input_list_equality()
    await test_rps_logic()