# SlapChop

[![Test Slapchop](https://github.com/luke-hdl/slapchop/actions/workflows/test_slapchop.yml/badge.svg?branch=main)](https://github.com/luke-hdl/slapchop/actions/workflows/test_slapchop.yml)

A simple Discord bot for strategic rock-paper-scissors (or variants), for online roleplaying games following World of Darkness: Mind's Eye Theater (and similar) rulesets.

SlapChop permits players to secretly select their preferred chop. When all players in a challenge have made their selection, everyone's selections are revealed. Challenges can include mass challenges.

## Adding SlapChop to your server:
To use the developer's hosted version, you can invite it your server with:
https://discord.com/oauth2/authorize?client_id=1228038244550311969

### Setting up your own seperate bot (technical users only)
If you are having difficulties because the developer is being lazy about keeping his hosted version up, you can create your own bot through the Discord Developer Portal and invite it to your server, then keep the Python script running to keep it responding. 

If you're using a command-line Bash interface: once you have the bot's token, create a file called TOKEN (no extensions) containing only the token. Run run_slapchop.bat, which will create and run a new Slapchop python file containing your token.

Otherwise: copy slapchop.py somewhere you won't share it, paste the token into the TOKEN variable, and run. 

## Using SlapChop

### Initial Setup
SlapChop does not offer any server-level settings. Just invite and go!

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
> @SlapChop#0552 challenge [@user 1]...[@user n]

> @Your Buddy SlapChop challenge [@user 1]...[@user n]

You are automatically considered the aggressor, and anyone else a defender. So, for instance, if I wanted to challenge my friend "Wumpus", I might challenge: 

> @Your Buddy SlapChop challenge @Wumpus

When you send this message, everyone involved will receive a DM. If someone's DM settings block SlapChop from DMing them, they can DM SlapChop

> hey

and it will let them know their challenge status. 

#### Replying to a challenge
After this, each user in the challenge privately messages SlapChop with how they want to respond. SlapChop doesn't currently keep track of whether a response is a valid RPS option; it is the responsibility of players to respond appropriately. This lets SlapChop respect unusual RPS variants, like Rock-Paper-Scissors-Bomb or Rock-Paper-Scissors-Lizard-Spock. 

For instance, I might DM: 
> rock

while Wumpus responds:
> paper

SlapChop will then ask for a bid. The MET system is used for bid behavior. If everyone bids, and at least one player threw the same thing as the aggressor, the aggressor's bid is revealed, and so is whether anyone who tied bid more, less, or the same. The bid does need to be a whole number under 1,000,000. If you have over 1,000,000 traits in the MET system, something very silly has happened. 

Once all challenged players have replied, SlapChop will send everyone a DM letting them know that the challenge is completed, then post the results in the channel where the challenge was issued. 
