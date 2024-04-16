class ResponderNotInChallengeException(Exception):
    """Raised when someone tries to respond to a challenge they were not invited to."""

class ResponderHasAlreadyRespondedException(Exception):
    """Raised when someone tries to respond to a challenge more than once."""

class BidIsInvalidException(Exception):
    """Raised when someone bids a number that is not a whole number or that is more than 999999"""

class PlayerIsInAChallengeException(Exception):
    """Raised when a player is already in a challenge. Limiting to one challenge at a time simplifies things a lot."""

class CouldNotUnderstandInputException(Exception):
    """Generic exception for highly invalid input, e.g. sending nothing."""