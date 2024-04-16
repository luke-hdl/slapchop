from enum import Enum
import time
import re
from .utils import *
from .exceptions import *

class Challenge:
    #Contains the following fields:
    #channel_for_challenge - the channel for the response
    #time_of_issue - The time the issue was opened, used to expire the challenge if needed.
    #responses - A dictionary that maps responders to their responses. (Responses know their responder, but this improves efficiency.)
    def __init__(self, channel_for_challenge, aggressor, defenders):
        self.channel = channel_for_challenge
        self.time_of_issue = time.time()
        self.responses = {aggressor: Response(aggressor, Role.AGGRESSOR)}
        self.aggressor_response = self.responses[aggressor]
        for defender in defenders:
            self.responses[defender] = Response(defender, Role.DEFENDER)

    def should_expire(self, timeout):
        return timeout < time.time() - self.time_of_issue

    def get_players_in_challenge(self):
        return self.responses.keys()

    def is_complete(self):
        for response in self.responses.values():
            if not response.complete:
                return False
        return True

    def did_everyone_bid(self):
        for response in self.responses.values():
            if response.bid is None:
                return False
        return True

    def did_anyone_tie_with_the_aggressor(self):
        aggressor_response = None
        non_aggressor_responses = []
        for response in self.responses.values():
            if response.role == Role.AGGRESSOR:
                aggressor_response = response.response
            else:
                non_aggressor_responses.append(response.response)
        return equal_input_to_one_of_list(aggressor_response, non_aggressor_responses)

    def get_role_for_player(self, player):
        if player not in self.responses:
            raise ResponderNotInChallengeException
        return self.responses[player].role

    def add_response_from_responder(self, responder, response):
        if responder not in self.responses:
            raise ResponderNotInChallengeException
        self.responses[responder].set_response(response)

    def add_bid_from_responder(self, responder, bid):
        if responder not in self.responses:
            raise ResponderNotInChallengeException
        self.responses[responder].set_bid(bid)

    def get_response_status(self, responder):
        if responder not in self.responses:
            return ResponseStatus.RESPONSE_DOES_NOT_EXIST
        else:
            return self.responses[responder].get_response_status()

    def get_response_description(self, responder, include_bid_information):
        if responder not in self.responses:
            raise ResponderNotInChallengeException
        return self.responses[responder].get_response_description(include_bid_information, self.aggressor_response)

class Response:
    #Contains the following fields:
    #responder - the user represented by this Response
    #role - whether the user is an Aggressor or a Defender
    #complete - whether the response is complete. A complete challenge will always have a response, but may or may not have a bid.
    #response - the response the responder has given (None if not yet provided)
    #bid - the bid of the responder (None if not provided)
    def __init__(self, responder, role):
        self.responder = responder
        self.role = role
        self.complete = False
        self.response = None
        self.bid = None

    def get_response_description(self, include_bid_information, aggressor_response):
        response = "{} ({}) threw: {}".format(self.responder.mention, self.role.get_as_readable(), self.response)
        if include_bid_information:
            if self.role == Role.AGGRESSOR:
                response += " and tied with at least one defender, bidding " + str(self.bid)
            elif equal_inputs(self.response, aggressor_response.response):
                if self.bid < aggressor_response.bid:
                    response += " and tied, bidding less than the aggressor"
                elif self.bid == aggressor_response.bid:
                    response += " and tied, bidding the same as the aggressor"
                else:
                    response += " and tied, bidding more than the aggressor"
        response += "\r\n"
        return response
    def set_response(self, player_response):
        if self.response is not None:
            raise ResponderHasAlreadyRespondedException
        self.response = player_response

    def get_response_status(self):
        if self.complete:
            return ResponseStatus.COMPLETE
        elif self.response is None:
            return ResponseStatus.WAITING_FOR_RESPONSE
        else:
            return ResponseStatus.WAITING_FOR_BID

    def set_bid(self, bid):
        if self.complete:
            raise ResponderHasAlreadyRespondedException
        elif equal_input_to_one_of_list(bid, ["No", "N", "no bid", "no thanks"]):
            self.bid = None
            self.complete = True
        elif bid is None or bid == "" or re.fullmatch("[0-9]{1,6}", bid) is None:
            raise BidIsInvalidException
        else:
            self.bid = int(bid)
            self.complete = True

class Role(Enum):
    AGGRESSOR = 1
    DEFENDER = 2

    def get_as_readable(self):
        match self:
            case Role.AGGRESSOR:
                return "Aggressor"
            case Role.DEFENDER:
                return "Defender"


class ResponseStatus(Enum):
    RESPONSE_DOES_NOT_EXIST = 0
    WAITING_FOR_RESPONSE = 1
    WAITING_FOR_BID = 2
    COMPLETE = 3
