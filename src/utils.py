def equal_inputs(string1, string2):
    #SlapChop is case-insensitive.
    #In the future, I'd like to add additional rules, e.g., ignoring internal spaces and text in parens, but not yet.
    if string1 is None or string2 is None:
        return string1 is None and string2 is None
    return string1.casefold() == string2.casefold()

def equal_input_to_one_of_list(string1, list_of_strings):
    for string2 in list_of_strings:
        if equal_inputs(string1, string2):
            return True
    return False