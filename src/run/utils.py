def automatically_determine_winner(string1, string2):
    chop1 = get_recognized_chop(string1)
    chop2 = get_recognized_chop(string2)
    if chop1 == RecognizedChops.UNKNOWN or chop2 == RecognizedChops.UNKNOWN:
        return RecognizedResult.UNKNOWN
    if chop1 == chop2:
        return RecognizedResult.TIE
    if chop1 == RecognizedChops.ROCK:
        match chop2:
            case RecognizedChops.SCISSORS:
                return RecognizedResult.PLAYER_1_WIN
            case __:
                return RecognizedResult.PLAYER_1_LOSS
    if chop1 == RecognizedChops.PAPER:
        match chop2:
            case RecognizedChops.ROCK:
                return RecognizedResult.PLAYER_1_WIN
            case __:
                return RecognizedResult.PLAYER_1_LOSS
    if chop1 == RecognizedChops.SCISSORS:
        match chop2:
            case RecognizedChops.ROCK:
                return RecognizedResult.PLAYER_1_LOSS
            case __:
                return RecognizedResult.PLAYER_1_WIN
    if chop1 == RecognizedChops.BOMB:
        match chop2:
            case RecognizedChops.SCISSORS:
                return RecognizedResult.PLAYER_1_LOSS
            case __:
                return RecognizedResult.PLAYER_1_WIN
    return RecognizedResult.UNKNOWN

def equal_inputs(string1, string2):
    #SlapChop is case-insensitive.
    #In the future, I'd like to add additional rules, e.g., ignoring internal spaces and text in parens, but not yet.
    if string1 is None or string2 is None:
        return string1 is None and string2 is None
    return string1.strip().casefold() == string2.strip().casefold()

def equal_input_to_one_of_list(string1, list_of_strings):
    for string2 in list_of_strings:
        if equal_inputs(string1, string2):
            return True
    return False

class RecognizedChops:
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    BOMB = 4
    UNKNOWN = 5

class RecognizedResult:
    PLAYER_1_WIN = 1
    PLAYER_1_LOSS = 2
    TIE = 3
    UNKNOWN = 4

def get_recognized_chop(from_chop):
    if equal_input_to_one_of_list(from_chop, ["rock", "r", ":new_moon_with_face", "rcok"]):
        return RecognizedChops.ROCK
    elif equal_input_to_one_of_list(from_chop,["paper", "p", ":scroll:", ":paper:"]):
        return RecognizedChops.PAPER
    elif equal_input_to_one_of_list(from_chop, ["scissors", "s", ":scissors:", "sissors", "scsissors"]):
        return RecognizedChops.SCISSORS
    elif equal_input_to_one_of_list(from_chop, ["bomb", "b", ":boom:", "bom"]):
        return RecognizedChops.BOMB
    else:
        return RecognizedChops.UNKNOWN