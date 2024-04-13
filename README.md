# SlapChop
A simple Discord bot for strategic rock-paper-scissors (or variants), for online roleplaying games following World of Darkness: Mind's Eye Theater (and similar) rulesets.

SlapChop permits players to secretly select their preferred chop. When all players in a challenge have made their selection, everyone's selections are revealed. Challenges can include mass challenges.

## Adding SlapChop to your server:
To use the developer's hosted version, you can invite it your server with:
https://discord.com/oauth2/authorize?client_id=1228038244550311969&permissions=274945018880&scope=bot

### Setting up your own seperate bot (technical users only)
If you are having difficulties because the developer is being lazy about keeping his hosted version up, you can create your own bot through the Discord Developer Portal and invite it to your server, then keep the Python script running to keep it responding. 

If you're using a command-line Bash interface: once you have the bot's token, create a file called TOKEN (no extensions) containing only the token. Run run_slapchop.bat, which will create and run a new Slapchop python file containing your token.

Otherwise: copy slapchop.py somewhere you won't share it, paste the token into the TOKEN variable, and run. 

## Using SlapChop

### Initial Setup
> @SlapChop#0552 start

This command changes SlapChop's nickname to 'Your Buddy SlapChop'. By default, Discord gives bots a role with the same name as the bot's name, which can cause user confusion when users accidentally @ the role, instead of the bot itself. Giving itself a nickname fixes this. Future versions may perform additional setup. (Replace @SlapChop#0552 with your instance of SlapChop's name, if you're not using the developer-hosted version.)

You only need to run this once; you can also manually change SlapChop's name anyways. 

### Help in Discord
> @SlapChop#0552 help

In a DM: 
> help

This doesn't give more information than is in README.md, but includes basic usage and a link to this document. It also uses the correct @ names for the server you are in, if SlapChop's nickname has been changed. 

### Static Challenge
> @SlapChop#0552 static

> @Your Buddy SlapChop static

This makes a static challenge, as in the MET system. It has even odds of "Win", "Tie", or "Loss"; functionally, it's equivalent to playing RPS with a completely random opponent. 

### Contested Challenge
#### Issuing the challenge
> @SlapChop#0552 challenge [name] [@user 1]...[@user n]

> @Your Buddy SlapChop challenge [name] [@user 1]...[@user n]

where name is a name for your challenge that no one else in your channel is currently using, and the list of users are mentioned users you want to be part of the challenge. You are automatically part of any challenge you issue. So, for instance, if I wanted to challenge my friend "Wumpus", I might challenge: 

> @Your Buddy SlapChop challenge fight @Wumpus

The name for your challenge can be any single-word combination of letters and numbers. The name is important because it lets you be in multiple challenges at once. 

When you send this message, SlapChop will reply: 

> Challenge opened between: @yourCoolNick - @Wumpus - all of whom should DM me with the following:  
> reply fight-0 response  
> You can also include a bid! After your response, include "bidding" at the end, then your trait bid, like this:  
> reply test-0 response bidding x  
> replacing the word response with your response (like rock, paper, scissors, or bomb), and the x with the number of traits you're bidding!  
> Bids will only be revealed if there's at least one tie where both the aggressor and at least one tying defending players submitted a bid. In that case, the aggressor's bid is revealed, and so is whether any tying defenders bid more or less.

The number given after the code is used by SlapChop to keep track of what server and channel the challenge came from. 

#### Replying to a challenge
After this, each user in the challenge privately messages SlapChop with how they want to respond. SlapChop doesn't currently keep track of whether a response is a valid RPS option; it is the responsibility of players to respond appropriately. This lets SlapChop respect unusual RPS variants, like Rock-Paper-Scissors-Bomb or Rock-Paper-Scissors-Lizard-Spock. 

For instance, I might DM: 
> reply fight-0 rock

while Wumpus responds:
> reply fight-0 paper

SlapChop will reply to each of our messages to let us know our response was recorded, and will let whoever answers last know that the results are being posted. 

Optionally, players can bid, using this syntax: 
> reply fight-0 rock bidding 10

replacing 10 with whatever your bid is. The MET system is used for bid behavior. If the aggressor (the person who made the challenge) bids, and at least one other person who picked the same thing to throw bids, the aggressor's bid is revealed, and so is whether anyone who tied bid more, less, or the same.

Once all challenged players have replied, SlapChop will post in the same channel the challenge was made. The results will look like this: 
> Challenge fight-0 is complete! @yourCoolNick throws rock!  
> @Wumpus throws paper!

at which point everyone can see that Wumpus has won the RPS game. If both player bid, this will instead look like, e.g.:
> Challenge test-0 is complete! @yourCoolNick throws paper! A tie occurred; they bid 13.  
> @Wumpus throws paper!  
> It's a tie! @Wumpus bid: the same number! (Remember, ties typically go to the defender, so this should probably be treated as if they'd bid more.)


## Upcoming Features
### User-oriented
* Automatically determining winners for RPS and RPS+Bomb variants in 2-player challenges.
* Better mass-bid features, such as declaring a single aggressor and many defenders, to extend these features.
* Built-in help functionality. 

### Developer-oriented
SlapChop is not designed for very heavy usage; there are some niche circumstances that could cause multithreading issues during heavy use, and its RAM performance is a little questionable. Upcoming updates will improve this. 

