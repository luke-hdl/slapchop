from enum import Enum
import time

class Challenge:
    #Contains the following fields:
    #channel_for_challenge - the channel for the response
    #time_of_issue - The time the issue was opened, used to expire the challenge if needed.
    #responses - A dictionary that maps responders to their responses. (Responses know their responder, but this improves efficiency.)
    def __init__(self, channel_for_challenge, aggressor, defenders):
        self.channel_for_challenge = channel_for_challenge
        self.time_of_issue = time.time()
        self.responses = {aggressor: Response(aggressor, Role.AGGRESSOR)}
        for defender in defenders:
            self.responses[defender] = Response(defender, Role.DEFENDER)\

    def should_expire(self, timeout):
        return timeout > time.time() - self.time_of_issue

    def is_complete(self):
        for response in self.responses:
            if not response.complete:
                return False
        return True

class Response:
    #Contains the following fields:
    #responder - the user represented by this Response
    #role - whether the user is an Aggressor or a Defender
    #complete - whether the response is complete. A complete challenge will always have a response, but may or may not have a bid.
    #response - the response the responder has given (None if not yet provided)
    #bid - the bid of the responder (None if not provided)
    def __init__self(self, responder, role):
        self.responder = responder
        self.role = role
        self.complete = False
        self.response = None
        self.bid = None

class Role(Enum):
    AGGRESSOR = 1
    DEFENDER = 2