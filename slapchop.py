import threading
import time
import random
import discord
import re

TOKEN = ''
TIMEOUT = 1200  # in seconds; a thread will not timeout before TIMEOUT seconds and will always timeout within TIMEOUT * 2 seconds
# as long as the bot is being used (since timeout checks aren't made when it isn't).

intents = discord.Intents.default()

client = discord.Client(intents=intents)
# The format of the challenges is a dictionary of codes, which correspond to a
# list, whose elements are pairs of users and responses.
recent_challenges = {}
expiring_challenges = {}
timer = 0
last_time = 0
timer_lock = threading.Lock()
# Used to prevent misbehavior with keeping track of the TIMEOUT function.
# There might still be some threading nonsense with timeout; improvements to thread-safety are an upcoming feature,
# but as is usage/expected usage is far too low for it to be a top priority.

guild_channels = []


# Keeps track of guild channels known to SlapChop. Since overall RAM usage is low, we don't currently expire this.
# Technically, it's a memory leak, but SlapChop could currently comfortably fit the guild channels of every game in the org on the RAM of the machine it runs on.
# Expiring will be added as part of the thread-safety update.

def clean_up_and_split(message):
    dirty_split = re.split("[ \t]{1,1000}", message)
    clean_split = []

    concatting = False
    concat_result = ""
    for part in dirty_split:
        if concatting:
            if part.endswith('"'):
                concat_result += part
                clean_split.append(concat_result)
                concatting = False
            else:
                concat_result += part + " "
        elif part.startswith('"'):
            concat_result += part + " "
            concatting = True
        else:
            clean_split.append(part)

    return clean_split


def get_code_map_if_active(code):
    if code in recent_challenges:
        return recent_challenges
    elif code in expiring_challenges:
        return expiring_challenges


def expire_challenges():
    global expiring_challenges
    global recent_challenges
    del expiring_challenges
    expiring_challenges = recent_challenges
    recent_challenges = {}


def get_channel_code_from_message(message):
    key = str(message.channel.guild.id) + ":" + str(message.channel.position)
    if key not in guild_channels:
        guild_channels.append(key)
    return str(guild_channels.index(key))


def add_response_from_user(code, user, response, bid):
    map = get_code_map_if_active(code)
    if map is None:
        return "Challenge " + code + " not found."
    if bid is not None and bid != "" and re.fullmatch("[0-9]*", bid) is None:
        return "Bid must be a number (no decimals allowed)."
    details = map[code]
    for challenge in details:
        if type(challenge) is list and challenge[0].id == user.id:
            if challenge[1] is None:
                challenge[1] = response
                if bid is not None and bid.isnumeric():
                    challenge.append(int(bid))
                else:
                    challenge.append(bid)
                return None
            else:
                return "You've already responded to " + code + "; responses are final."
    return "You aren't part of this challenge."


async def post_challenge_results(code):
    map = get_code_map_if_active(code)
    details = map[code]
    initial_challenge_result = "Challenge " + code + " is complete!"
    challenge = details[1]
    have_tied = False
    tying_chop = challenge[1]
    tying_bid = None
    if len(challenge) == 3:
        tying_bid = challenge[2]
    initial_challenge_result += " " + challenge[0].mention + " throws " + challenge[1] + "!"
    description = ""
    iterator = 2
    while iterator < len(details):
        challenge = details[iterator]
        description += "\r\n" + challenge[0].mention + " throws " + challenge[1] + "!"
        if challenge[1] == tying_chop and challenge[2] is not None:
            if len(challenge) == 3 and tying_bid is not None:
                if tying_bid > challenge[2]:
                    description += "\r\n     It's a tie! " + challenge[0].mention + " bid: less!"
                elif tying_bid < challenge[2]:
                    description += "\r\n     It's a tie! " + challenge[0].mention + " bid: more!"
                else:
                    description += "\r\n     It's a tie! " + challenge[
                        0].mention + " bid: the same number! (Remember, ties typically go to the defender, so this should probably be treated as if they'd bid more.)"
            if not have_tied:
                have_tied = True
                if tying_bid is not None:
                    initial_challenge_result += " A tie occurred; they bid " + str(tying_bid) + "."
                else:
                    initial_challenge_result += " A tie occurred, but they did not declare a bid."
        iterator += 1
    await details[0].send(initial_challenge_result + description)
    del map[code]


async def check_if_responses_are_filled_out(code, sender_channel):
    map = get_code_map_if_active(code)
    if map is None:
        return  # something wrong has happened.
    details = map[code]
    for challenge in details:
        if type(challenge) is list and challenge[1] is None:
            await sender_channel.send(
                "Your response has been recorded. Results will be posted when all challenged users have responded.")
            return
    await post_challenge_results(code)
    await sender_channel.send("The challenge is complete! Go check the channel it was issued in for results.")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    global timer
    global last_time
    with timer_lock:
        timer += time.time() - last_time
        last_time = time.time()
        if timer > TIMEOUT:
            # Note that we only check for timeout when messages are actually being sent.
            # This is because checking for timeout is a very simple technique to not have old and forgotten challenges clogging up RAM.
            # If no one's actually sending challenges, it doesn't matter, but this does mean that a challenge won't expire until SlapChop has received
            # at least two messages (from anywhere) after the challenge is sent, regardless of TIMEOUT.
            expire_challenges()
            timer = 0

    if message.author == client.user:
        return

    message_info = clean_up_and_split(message.content)

    if len(message_info) < 2 and message.content.startswith('help'):
        await message.channel.send('Make a static: ' + client.user.mention + " static")
        await message.channel.send(
            'Make a challenge (you are automatically the aggressor on the challenge you send, and they\'re the defender): ' + client.user.mention + " challenge @enemy1 @enemy2 etc")
        await message.channel.send(
            'Reply to a challenge: follow the directions in the challenge message sent by me :)')
        await message.channel.send(
            'More detailed guidance is available at: https://github.com/luke-hdl/slapchop/blob/main/README.md')
        return

    elif message_info[1].startswith('start'):
        await message.guild.me.edit(nick="Your Buddy SlapChop")
        await message.channel.send('All ready to go!')

    elif message_info[1].startswith('help'):
        await message.channel.send('Make a static: ' + client.user.mention + " static")
        await message.channel.send(
            'Make a challenge (you are automatically part of a challenge you make): ' + client.user.mention + " challenge @enemy1 @enemy2 etc")
        await message.channel.send('Reply to a challenge: follow the directions in the challenge message sent by me :)')
        await message.channel.send(
            'More detailed guidance is available at: https://github.com/luke-hdl/slapchop/blob/main/README.md')
        return

    elif message_info[1].startswith('challenge'):
        mentions = message.mentions
        challenged_individuals = [message.author]
        for mention in mentions:
            if mention not in challenged_individuals and mention != client.user:
                challenged_individuals.append(mention)
        if len(challenged_individuals) < 2:
            await message.channel.send(
                'A challenge needs at least two people! Make sure to @ your rivals at the end of the message.')
            return
        code = message_info[2]
        if code in recent_challenges or code in expiring_challenges:
            await message.channel.send('Challenge ' + code + ' is already active; please name a new challenge.')
        elif not code.isalnum():
            await message.channel.send(
                'SlapChop only supports letters and numbers in challenge names. Please name a new challenge.')
        else:
            code = code + "-" + get_channel_code_from_message(message)
            recent_challenges[code] = [message.channel]
            success_message = "Challenge opened between: "
            for individual in challenged_individuals:
                recent_challenges[code].append([individual, None])
                success_message += individual.mention + " - "
            success_message += "all of whom should DM me with the following: "
            await message.channel.send(success_message)
            await message.channel.send("```reply " + code + " response```")
            await message.channel.send(
                'You can also include a bid! After your response, include "bidding" at the end, then your trait bid, like this:')
            await message.channel.send("```reply " + code + " response bidding x```")
            await message.channel.send("replacing the word response with your response (like rock, paper, scissors, or bomb), and the x with the number of traits you're bidding!")
            await message.channel.send("Bids will only be revealed if everyone bids, and only if two people submitted the same chop response. In that case, the aggressor's bid is revealed, and so is whether any tying defenders bid more or less.")

    elif message_info[0].startswith('reply'):
        if len(message_info) < 3:
            await message.channel.send(
                'Hey, remember: I need both the challenge name and your response to know what you\'re responding to!')
            await message.channel.send('Try copying the message that I replied to the challenge with exactly.')
            return
        if len(message_info) == 4 or len(message_info) > 5 or (len(message_info) == 5 and message_info[3] != "bidding"):
            await message.channel.send(
                'I\'m not sure what you mean. If you\'d like to send a multi-word response, you can put your response in quotation marks, like "metal scissors" instead of scissors.')
            await message.channel.send('Try copying the message that I replied to the challenge with exactly.')
        code = message_info[1]
        if message_info[2] == "response":
            await message.channel.send('Hey, make sure to swap the word "response" for your response!')
            return
        if len(message_info) == 5 and message_info[4] == "x":
            await message.channel.send('Hey, make sure to swap the letter "x" for your bid!')
            return

        if len(message_info) == 5:
            error_message = add_response_from_user(code, message.author, message_info[2], message_info[4])
        else:
            error_message = add_response_from_user(code, message.author, message_info[2], None)

        if error_message is None:
            await check_if_responses_are_filled_out(code, message.channel)
        else:
            await message.channel.send(error_message)

    elif message_info[1].startswith('static'):
        match random.randint(1, 3):
            case 1:
                await message.channel.send(message.author.mention + "'s result: Win")
            case 2:
                await message.channel.send(message.author.mention + "'s result: Tie")
            case 3:
                await message.channel.send(message.author.mention + "'s result: Loss")

    else:
        await message.channel.send("I'm not sure what you mean.")
        if message.channel.guild is not None:
            await message.channel.send(
                "I know the commands: static, challenge, help. For more details, post the following:")
            await message.channel.send(client.user.mention + " help")
        else:
            await message.channel.send(
                "If you're trying to respond to a challenge, remember that your message needs to start with reply!")
            await message.channel.send(
                'You can copy and paste the exact message I responded to the challenge with. Just change the word "response" to your response!')


client.run(TOKEN)
