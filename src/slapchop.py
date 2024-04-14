import threading
import time
import random
import discord
import re

TOKEN = 'YOURTOKEN'
TIMEOUT = 1200  # in seconds; a thread will not time out before TIMEOUT seconds and will always time out within TIMEOUT * 2 seconds
# as long as the bot is being used (since timeout checks aren't made when it isn't).
DEFAULT_CHALLENGE_NAMES = ['angle', 'ant', 'apple', 'arch', 'arm', 'army', 'baby', 'bag', 'ball', 'band', 'basin', 'basket', 'bath', 'bed', 'bee', 'bell', 'berry', 'bird', 'blade', 'board', 'boat', 'bone', 'book', 'boot', 'bottle', 'box', 'boy', 'brain', 'brake', 'branch', 'brick', 'bridge', 'brush', 'bucket', 'bulb', 'button', 'cake', 'camera', 'card', 'cart', 'carriage', 'cat', 'chain', 'cheese', 'chest', 'chin', 'church', 'circle', 'clock', 'cloud', 'coat', 'collar', 'comb', 'cord', 'cow', 'cup', 'curtain', 'cushion', 'dog', 'door', 'drain', 'drawer', 'dress', 'drop', 'ear', 'egg', 'engine', 'eye', 'face', 'farm', 'feather', 'finger', 'fish', 'flag', 'floor', 'fly', 'foot', 'fork', 'fowl', 'frame', 'garden', 'girl', 'glove', 'goat', 'gun', 'hair', 'hammer', 'hand', 'hat', 'head', 'heart', 'hook', 'horn', 'horse', 'hospital', 'house', 'island', 'jewel', 'kettle', 'key', 'knee', 'knife', 'knot', 'leaf', 'leg', 'library', 'line', 'lip', 'lock', 'map', 'match', 'monkey', 'moon', 'mouth', 'muscle', 'nail', 'neck', 'needle', 'nerve', 'net', 'nose', 'nut', 'office', 'orange', 'oven', 'parcel', 'pen', 'pencil', 'picture', 'pig', 'pin', 'pipe', 'plane', 'plate', 'plough', 'pocket', 'pot', 'potato', 'prison', 'pump', 'rail', 'rat', 'receipt', 'ring', 'rod', 'roof', 'root', 'sail', 'school', 'scissors', 'screw', 'seed', 'sheep', 'shelf', 'ship', 'shirt', 'shoe', 'skin', 'skirt', 'snake', 'sock', 'spade', 'sponge', 'spoon', 'spring', 'square', 'stamp', 'star', 'station', 'stem', 'stick', 'stocking', 'stomach', 'store', 'street', 'sun', 'table', 'tail', 'thread', 'throat', 'thumb', 'ticket', 'toe', 'tongue', 'tooth', 'town', 'train', 'tray', 'tree', 'trousers', 'umbrella', 'wall', 'watch', 'wheel', 'whip', 'whistle', 'window', 'wing', 'wire', 'worm']

intents = discord.Intents.default()

client = discord.Client(intents=intents)
# The format of the challenges is a dictionary of codes, which correspond to a
# list, whose elements are pairs of users and responses.
recent_challenges = {}
expiring_challenges = {}
timer = 0
last_time = 0
timer_lock = threading.Lock()
counter_for_code_duplication = 0



def clean_up_and_split(message):
    dirty_split = re.split("[ \t]{1,1000}", message.strip())
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


def get_code_map_if_active(code):
    if code in recent_challenges:
        return recent_challenges
    elif code in expiring_challenges:
        return expiring_challenges

def get_code_with_number(code):
    global counter_for_code_duplication
    counter_for_code_duplication += 1
    if counter_for_code_duplication > 99999:
        counter_for_code_duplication = 0
    return code + "-" + str(counter_for_code_duplication)

def expire_challenges():
    global expiring_challenges
    global recent_challenges
    del expiring_challenges
    expiring_challenges = recent_challenges
    recent_challenges = {}

def add_response_from_user(code, user, response, bid):
    code_map = get_code_map_if_active(code)
    if code_map is None:
        return "Challenge " + code + " not found."
    if bid is not None and bid != "" and re.fullmatch("[0-9]*", bid) is None:
        return "Bid must be a number (no decimals allowed)."
    details = code_map[code]
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

def get_default_challenge_name():
    tries = 0
    code = ""
    while tries < 200: #Not really efficient, but RAM, not CPU, is by far the limiting resource with my current hosting.
        code = DEFAULT_CHALLENGE_NAMES[random.randint(0, len(DEFAULT_CHALLENGE_NAMES))]
        if get_code_map_if_active(code) is None:
            return code
        tries += 1
    return get_code_with_number(code)


async def post_challenge_results(code):
    code_map = get_code_map_if_active(code)
    details = code_map[code]
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
    del code_map[code]

async def post_help_tips(channel):
    await channel.send('Make a static: ' + client.user.mention + " static")
    await channel.send(
            'Make a challenge (you are automatically the aggressor on a challenge you make): ' + client.user.mention + " challenge challenge_name @enemy1 @enemy2 etc")
    await channel.send('Reply to a challenge: follow the directions in the challenge message sent by me :)')
    await channel.send(
            'More detailed guidance is available at: https://github.com/luke-hdl/slapchop/blob/main/README.md')

async def check_if_responses_are_filled_out(code, sender_channel):
    code_map = get_code_map_if_active(code)
    if code_map is None:
        return  # something wrong has happened.
    details = code_map[code]
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

    if message.channel.guild is not None and client.user not in message.mentions:
        #In server messages, SlapChop only looks at messages it's actually mentioned in.
        return

    message_info = clean_up_and_split(message.content)

    if len(message_info) < 2 and message.content.startswith('help'):
        await post_help_tips(message.channel)
        return

    elif len(message_info) < 2:
        await message.channel.send('Hey there! You can send me \r\n' + client.user.mention + '\r\n help to find out what I can do!')

    elif message_info[1].startswith('help'):
        await post_help_tips(message.channel)
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
        code_is_mention = re.fullmatch("<@[0-9]*>", code) is not None
        if re.match(".*<.*:[0-9]{15,1000}>.*", code) is not None:
            await message.channel.send('Sorry, SlapChop doesn\'t support custom server emojis. (Sometimes, I might mistakenly think a long code with a lot of numbers is a custom emoji. Codes that long aren\'t allowed either, though.)')
        elif not code_is_mention and len(code) > 17:
            await message.channel.send(
                'Codes should be 20 characters or shorter. (Be aware that Discord emojis count for more than one, depending on their "name" - for instance, a :smile: is 7.)')
        else:
            success_message = ""
            if code_is_mention: #the code starting with a mention means no code was specified
                code = get_default_challenge_name()
                success_message += '**ALERT**: You didn\'t name your challenge, or you named it after a mention. I\'ve named it ***' + code + '*** for you. When you issue a challenge, you can name it yourself by putting the name between the word "challenge" and the names of your friends. Names can\'t be mentions, though (I\'ll think that\'s who you\'re challenging!) \r\n'
            elif code in recent_challenges or code in expiring_challenges:
                code = get_code_with_number(code)
                success_message += '**ALERT**: Your challenge code is in use somewhere else. I\'ve automatically renamed it to ' + code + ' in my memory.\r\n'
            recent_challenges[code] = [message.channel]
            success_message += "Challenge opened between: "
            for individual in challenged_individuals:
                recent_challenges[code].append([individual, None])
                if individual == message.author:
                    success_message += individual.mention + " (aggressor)\r\n"
                else:
                    success_message += individual.mention + " (defender)\r\n"
            success_message += "all of whom should DM me with the following: "
            success_message += "\r\n```reply " + code + " response```"
            success_message += '\r\nYou can also include a bid! After your response, include "bidding" at the end, then your trait bid, like this:'
            success_message += "\r\n```reply " + code + " response bidding x```"
            success_message += "\r\nreplacing the word response with your response (like rock, paper, scissors, or bomb), and the x with the number of traits you're bidding!"
            success_message += "\r\nBids will only be revealed if the aggressor and at least one person who submitted the same response *both* bid. In that case, the aggressor's bid is revealed, and so is whether any tying defenders bid more or less."
            await message.channel.send(success_message)

    elif message_info[0].startswith('reply'):
        if len(message_info) < 3:
            await message.channel.send(
                'Hey, remember: I need both the challenge name and your response to know what you\'re responding to!')
            await message.channel.send('Try copying the message that I replied to the challenge with exactly.')
            return
        if len(message_info) == 4 or len(message_info) > 5 or (len(message_info) == 5 and message_info[3] != "bidding"):
            await message.channel.send(
                'I\'m not sure what you mean. If you\'d like to send a multi-word response, you can put your response in quotation marks, like "metal scissors" instead of scissors.\r\nTry copying the message that I replied to the challenge with exactly.')
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
                "I know the commands: static, challenge, help. For more details, post the following:\r\n" + client.user.mention + " help")
        else:
            await message.channel.send(
                "If you're trying to respond to a challenge, remember that your message needs to start with reply!\r\nYou can copy and paste the exact message I responded to the challenge with. Just change the word \"response\" to your response!")

client.run(TOKEN)
