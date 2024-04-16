import threading
import re
from random import randint
from .challenge import *
from .exceptions import *
from .utils import *

class MessageResponder:
    def __init__(self, timeout, client):
        self.timeout = timeout
        self.challenges_by_player = {}
        self.alter_challenges_lock = threading.Lock()
        self.client = client

    async def add_players_to_challenge(self, challenge, players):
        with self.alter_challenges_lock:
            for player in players:
                if player in self.challenges_by_player:
                    # Generally, this shouldn't happen much; we check if players are in a challenge while creating it.
                    # But we need to minimize time and logic with the alter_challenges_lock.
                    del challenge
                    raise PlayerIsInAChallengeException
            for player in players:
                self.challenges_by_player[player] = challenge

            for player in players:
                try:
                    await player.send(
                        "You've been challenged to chops! Send me a message with what you'd like to throw, like 'rock', 'paper', or 'scissors'. (I accept custom rules, so feel free to send 'bomb', etc., too - I might not be able to automatically determine winners, though)!)")
                except:
                    pass

    async def attempt_to_cancel_challenge(self, player):
        with self.alter_challenges_lock:
            if player in self.challenges_by_player:
                for notify_player in self.challenges_by_player[player].get_players_in_challenge():
                    self.challenges_by_player.pop(notify_player)
                    try:
                        await notify_player.send("The challenge you were in has been cancelled.")
                    except:
                        pass

            else:
                await player.send("You're not in a challenge!")

    async def expire_challenges(self, ):
        players_to_expire = []
        with self.alter_challenges_lock:
            for player_with_challenge in self.challenges_by_player:
                if self.challenges_by_player[player_with_challenge].should_expire(self.timeout):
                    players_to_expire.append(player_with_challenge)
            for player in players_to_expire:
                self.challenges_by_player.pop(player)
        for player in players_to_expire:
            try:
                await player.send(
                    "Your challenge timed out. If you'd like to be in a challenge, please issue a new one.")
            except:
                pass

    def add_response_from_player(self, player, response):
        challenge = self.challenges_by_player.get(player)
        if challenge is None:
            raise ResponderNotInChallengeException
        challenge.add_response_from_responder(player, response)

    def add_bid_from_player(self, player, bid):
        challenge = self.challenges_by_player.get(player)
        if challenge is None:
            raise ResponderNotInChallengeException
        challenge.add_bid_from_responder(player, bid)

    def clean_up_and_split_message_text(self, message_text):
        dirty_split = re.split("[ \t]{1,1000}", message_text.strip())
        clean_split = []

        concatenating = False
        concat_result = ""
        for part in dirty_split:
            if concatenating:
                if part.endswith('"'):
                    concat_result += part
                    clean_split.append(concat_result)
                    concatenating = False
                else:
                    concat_result += part + " "
            elif part.startswith('"'):
                concat_result += part + " "
                concatenating = True
            else:
                clean_split.append(part)

        return clean_split

    def get_self_mention(self, ):
        return self.client.user.mention

    async def process_guild_message_text_from_player(self, channel, message):
        if self.client.user not in message.mentions:
            return  # By default, SlapChop shouldn't see messages that it doesn't ask for, but it's better safe than sorry.
        message_text = message.content
        tokenized_message_text = re.split("[ \t]{1,1000}", message_text)
        if equal_inputs(tokenized_message_text[1], "challenge"):
            if message.author in self.challenges_by_player:
                await channel.send(
                    message.author.mention + ", you're already in a challenge! If you'd like to leave it, please DM me *quit* or *leave*. (Don't send me it here, though!)")
                return
            defending_players = []
            players_in_challenges = []
            for player in message.mentions:
                if player in self.challenges_by_player:
                    players_in_challenges.append(player)
                if player != self.client.user and player != message.author:
                    defending_players.append(player)
            if len(players_in_challenges) > 0:
                error_message = "Players can only be in one challenge at once. These players are in challenges: "
                for player in players_in_challenges:
                    error_message += player.mention + "; "
                error_message += "I can't start a challenge until they're done. If they'd like, they can quit those by DMing me *quit* or *leave*."
                await channel.send(error_message)
                return
            if len(defending_players) < 1:
                await channel.send("You need to mention at least one person you're challenging!")
                return
            new_challenge = Challenge(message.channel, message.author, defending_players)
            defending_players.append(message.author)
            try:
                await self.add_players_to_challenge(new_challenge, defending_players)
            except PlayerIsInAChallengeException:
                await channel.send(
                    "I recieved multiple challenge requests for one of your players in a very short order. I haven't begun your challenge because of this. Please submit it again.")
                return
            await channel.send(
                "Your challenge was successfully created! All players should've recieved a DM with instructions for how to reply. If you didn't recieve one, you might have settings where I can't message you unprompted. If so, you can send me *hi* or *hey* and I'll get your channel set up.")
        elif equal_inputs(tokenized_message_text[1], "static"):
            await self.perform_static_challenge(channel, message.author)

        else:
            await self.send_help_response(channel)

    async def process_direct_message_text_from_player(self, channel, player, message_text):
        if len(message_text) == 0:
            await self.send_completely_unknown_input_exception(channel)
        elif equal_inputs(message_text, "Help"):
            await self.send_help_response(channel)
        elif equal_input_to_one_of_list(message_text, ["Leave", "Quit"]):
            await self.attempt_to_cancel_challenge(player)
        elif equal_input_to_one_of_list(message_text, ["Hello", "Hey", "Ho", "Status", "State"]):
            if player in self.challenges_by_player:
                match self.challenges_by_player[player].get_response_status(player):
                    case ResponseStatus.RESPONSE_DOES_NOT_EXIST:
                        await channel.send(
                            "Hey there! You're in a challenge, but it looks like I might have lost track of you. I'm going to remove you from the challenge - feel free to issue a new one.")
                        self.challenges_by_player.pop(player)
                    case ResponseStatus.WAITING_FOR_RESPONSE:
                        await channel.send(
                            "Hey there! You're in a challenge, I'm waiting for your response. Please reply with it!")
                    case ResponseStatus.WAITING_FOR_BID:
                        await channel.send(
                            "Hey there! You're in a challenge, I'm waiting for your bid. Please reply with a whole number. If you don't want to bid, send me the word *no* instead!")
                    case ResponseStatus.COMPLETE:
                        await channel.send(
                            "Hey there! You're in a challenge. You've submitted your bid and response, but I'm waiting for other players. If you think they've gotten distracted, you can cancel the challenge by sending me *quit* or *leave*.")
            else:
                await channel.send(
                    "Hey there! You're not in a challenge - feel free to go send one in any server channel I'm in.")
            return

        status = ResponseStatus.RESPONSE_DOES_NOT_EXIST

        if player in self.challenges_by_player:
            status = self.challenges_by_player[player].get_response_status(player)

        try:
            match status:
                case ResponseStatus.RESPONSE_DOES_NOT_EXIST:
                    raise ResponderNotInChallengeException
                case ResponseStatus.WAITING_FOR_RESPONSE:
                    self.add_response_from_player(player, message_text)
                    await channel.send(
                        "Your response has been recorded! Now you can submit a bid. If you'd like to provide a bid, reply with a whole number. Otherwise, reply 'no' so that I know that you're done.")
                case ResponseStatus.WAITING_FOR_BID:
                    self.add_bid_from_player(player, message_text)
                    await channel.send(
                        "Your bid has been recorded! You'll receive a DM and a mention in the challenge channel when everyone has responded.")
                case ResponseStatus.COMPLETE:
                    raise ResponderHasAlreadyRespondedException  # lets us fold this case into the error handling.
        except ResponderNotInChallengeException:
            await channel.send(
                "Hey there! You're not in a challenge right now - you can only issue challenges in a channel that you, I, and whoever you're challenging all have access to. If you'd like more information, please send me the word 'help'.")
        except ResponderHasAlreadyRespondedException:
            await channel.send(
                "Hey there! You've already responded to the challenge you're in right now. If people aren't responding, and you'd like to leave the challenge, you can send me the word 'leave' to leave the challenge. (This cancels the challenge for everyone, though!)")
        except BidIsInvalidException:
            await channel.send(
                "Hey there! Your bid needs to be a whole number under 999999. I understand '3' or '5', but not '-3' or '5.5' or '1/2'.")
        except:
            await channel.send(
                "Something went wrong, and I'm very confused. Your input hasn't been recorded. If you keep seeing this message_text, please contact my developer, discord user marrinkarrin.")

        await self.process_challenge_status_for_player(player)

    async def process_challenge_status_for_player(self, player):
        challenge = self.challenges_by_player.get(player)
        if challenge is not None and challenge.is_complete():
            await self.complete_challenge(challenge)

    async def complete_challenge(self, challenge):
        with self.alter_challenges_lock:
            for notify_player in challenge.get_players_in_challenge():
                self.challenges_by_player.pop(notify_player)
                try:
                    await notify_player.send(
                        "Your challenge has been completed! See the channel it was posted in for results!")
                except:
                    pass
        await self.post_challenge_results(challenge)
        del challenge

    async def post_challenge_results(self, challenge):
        results = "The challenge between "
        players = list(challenge.get_players_in_challenge())
        iterator = 0
        while iterator < len(players) - 1:
            player = players[iterator]
            results += player.display_name + " + "
            iterator += 1
        results += players[iterator].display_name + " is complete!\r\n"
        print_bid_information = challenge.did_anyone_tie_with_the_aggressor()
        if challenge.did_everyone_bid() and print_bid_information:
            results += "Every player submitted a bid, and at least one tie has occurred! I'll reveal the aggressor's bid, and whether any tying players bid more, less, or equal.\r\n"
        elif not challenge.did_everyone_bid() and print_bid_information:
            print_bid_information = False
            results += "A tie occurred, but not every player submitted a bid. I won't reveal bid-related information.\r\n"
        results += "Results: \r\n"
        for player in players:
            results += challenge.get_response_description(player, print_bid_information)
        await challenge.channel.send(results)

    async def perform_static_challenge(self, channel, player, winning_ties=None):
        match randint(1, 3):
            case 1:
                await channel.send(player.mention + ", you won! :)")
            case 2:
                if winning_ties is not None:
                    if winning_ties:
                        await channel.send(player.mention + ", you passed the Static on a tie!")
                    else:
                        await channel.send(player.mention + ", you lost the Static on a tie.")
                else:
                    await channel.send(player.mention + ", you tied. :O")
            case 3:
                await channel.send(player.mention + ", you lost. :(")

    async def send_completely_unknown_input_exception(self, channel):
        await channel.send("""
            Hey there! I'm not quite sure what you meant. 
            If you'd like an explanation of what I can do, you can post

            {} help

            in any channel I'm in. Or just DM me the word "help"!
        """.format(self.get_self_mention()))

    async def send_help_response(self, channel):
        await channel.send("""
            Welcome to SlapChop! If you'd like to challenge someone, go to a channel that they're in, then send: "

            {} challenge @friend

            You can even challenge multiple people in the same challenge, just mention all of them! Just be warned that you can only be in one challenge at a time.
            Everyone in the challenge will receive a DM from me with instructions. Once everyone has replied, I'll post the results!
            I also support static challenges (equivalent to playing against a totally random NPC.) Just send me: 

            {} static

            and I'll tell you if you won or lost.
        """.format(self.get_self_mention(), self.get_self_mention()))

    async def on_ready(self, ):
        print(f'We have logged in as {self.client.user}')

    async def on_message(self, message):
        if message.author == self.client.user:
            return
        await self.expire_challenges()
        if message.channel.guild is not None:
            await self.process_guild_message_text_from_player(message.channel, message)
        else:
            await self.process_direct_message_text_from_player(message.channel, message.author, message.content)
