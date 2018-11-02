import csv
import yugi_db as db
# File to load deck data from text files.

DECK_DIR = "decks/"
DEBUG = False
EXT_KEYWORD = "EXT"

# Loads from deck directory, with id set from maldoche deck.
# Returns array of deck info
def load_deck(deckname):
    if db.ALL_CARDS == None:
        print("Card Names not loaded")
        exit(1)

    print("Loading Deck: ", deckname)
    result = [[], []]
    count = [0, 0]
    with open(DECK_DIR + deckname + ".csv", 'r') as csvfile:
        creader = csv.reader(csvfile, delimiter=':', quotechar='"')
        deckid = 0
        for row in creader:
            if len(row) == 0:
                continue

            if deckid == 0:
                if row[0] == EXT_KEYWORD:
                    if DEBUG:
                        print("EXT: ")
                    deckid = 1
                    continue

            value = db.find_card(row[0])

            if DEBUG:
                print(value)

            value["count"] = int(row[1])
            count[deckid] += int(row[1])
            result[deckid].append(value)


    print("Total Main Deck Cards: ", count[0])
    print("Total EXT Cards: ", count[1])
    return result
