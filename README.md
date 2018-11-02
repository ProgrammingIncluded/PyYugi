# PyYugi
## Intro
PyYugi is an attempt to capture the Yu Gi Oh game in Python in such a way that is easy and extendable. 
The goal is to be able to design an automated system for auto play and optimization problems.

## Disclaimer
I do not provide any data that pertains to the trademarks of the game Yu Gi Oh and I am not affiliated with Konami.

Any and all Yu Gi Oh metadata is from the Yu Gi Oh database [https://ygoprodeck.com/](https://ygoprodeck.com/). If the website is down, then one will have to resupply the metadata for the program to work properly.

## How to Run
There are two main programs included.
### PyYugi
Program to kickstart a file that plays the framework.

> python main.py

### PyYugiTerm
A simple interactive terminal to search for a card in the database.

> python yugi_terminal.py

## Deck Loading and Building a Deck
PyYugi allows fast loading of cards from a deck by listing out cardnames in a count within csv files.

To create a deck, go to the deck folder and create a csv file. For example, "synchron.csv"

Now format the file like the following:

> swift scarecrow: 3
> tuningware: 1
> EXT:
> junk speeder: 2
> stardust dragon: 1

Everything after the "EXT:" keyword will be treated as cards in the extra deck. Numbers after the card name represents the card count for that specific card.

Cards can be specifically loaded by the ld_deck.py module and can becalled via:

> load_deck("synchron")

Notice the lack of csv ext in the load function.
Besure to load the DB before hand. Refer to main.py for example.

## Q/A
### ygoprodeck is down?
If the main database that is being used does not exist, the files must be provided locally.

### What are the empty data and deck folders?
They are folders to store DB data for caching and deck data for building decks.

### Will there be more documentation on the PyYugi sourcecode?
Depending on the success of the project, more documentation will be written. Right now, main.py will be assumed to be a standalone program.