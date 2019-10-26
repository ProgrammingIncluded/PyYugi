"""
File to manage querying to database to get file metadata.
The file handles CACHES folder. Essential pulls the 4000+
card names in order to all_cards.json and loads it into memory
as a lookup table for names and id values. get_card_stat()
can load more meta data about the card.

Meta data is cached locally in 10 files for easier cache object loading
and keeps the last read meta data file cache in memory. Ejects it if a card
stat is not found.
"""

import requests
import os
import json
import card_util as cu


DEBUG_DB = False
DATA_DIR = "data/"
AC_FILE = DATA_DIR + "allcards.json"

# Functions to connect to yugioh db.
ALL_CARDS = None

# Loaded card stats in memory
CARD_STATS = {}

# Stats cache
STATS_ID_CACHE = -1
STATS_CACHE = []

# Create a directory if not applicable
def check_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

# Function to return the meta data of a card.
def get_card_stat(id):
    global CARD_STATS
    global STATS_CACHE
    global STATS_ID_CACHE

    id = int(id)
    # Check first if in memory
    if str(id) in CARD_STATS:
        return CARD_STATS[str(id)]

    # check if there is anything in the previous read cache
    # if applicable
    if id % 10 == STATS_ID_CACHE:
        val = cu.search_card(id, STATS_CACHE)
        if val != None:
            CARD_STATS[val["id"]] = val
            return val

    number = id % 10
    fname = DATA_DIR + "cardmeta" + str(number) + ".json"

    data = []
    # Check if in file:
    if os.path.isfile(fname):
        with open(fname, "r") as inf:
            data = json.load(inf)
            
            if DEBUG_DB:
                print("Finding card meta data for " + str(id))
            val = cu.search_card(str(id), data)

            STATS_CACHE = data
            STATS_ID_CACHE = id % 10
            # object found
            if val != None:
                CARD_STATS[val["id"]] = val
                return val
    else:
        # create file
        with open(fname, "w") as inf:
            inf.write("[]")

    if DEBUG_DB:
        print("Fetching card meta online data for: " + str(id))
    # Fetch online and then write to file.
    response = requests.get(
        "https://db.ygoprodeck.com/api/cardinfo.php?name=" + str(id), 
        headers={"Content-Type": "application/json"}
    )
    val = json.loads(response.text)
    val = val[0]
    CARD_STATS[val["id"]] = val["id"]

    # Write everytime.
    # Flush our results when done
    data = []
    with open(fname, "r") as js:
        data = json.load(js)
    data.append(val)
    with open(fname, "w") as js:
        json.dump(data, js)

    return val
    
# Function to unload all yugioh card names to id.
def unload_card_names():
    ALL_CARDS = None

# Load all the card names from file.
# Note: Only function that checks data directory
# this is okay because this function must be called.
# Must call this before find_card() will work.
# Loads entire unique ID to card name DB.
def load_card_names():
    global ALL_CARDS
    if ALL_CARDS != None:
        return

    check_dir()
    if not os.path.isfile(AC_FILE):
        print("Fetching AC File")
        response = requests.get(
            "https://db.ygoprodeck.com/api/allcards.php",
            headers={"Content-Type": "application/json"}
        )
        ALL_CARDS = json.loads(response.text)

        print("Saving AC File")
        with open(AC_FILE, "w") as outf:
            outf.write(response.text)
    else:
        print("Loading AC File")
        with open(AC_FILE, "r") as inf:
            ALL_CARDS = json.load(inf)

    # Remove the extra array
    ALL_CARDS = ALL_CARDS[0]

#### QUERY FUNCTIONS ####
# Can only work if load_card_names() is first called
# Searches the DB of cardnames to id to find the card dictionary.
# See py_terminal for returned values.
#
# Implementation is mainly a linear search because a game should
# not have too many queries to do. Can be more efficient if data
# type is sorted for binary search.

def find_card(name):
    """Finds cards with name"""
    name = name.lower()
    for i in ALL_CARDS:
        if i["name"].lower() == name:
            return i
    return None


def find_card_with_id(card_id):
    """Finds cards given id"""
    card_id = int(card_id)
    for i in ALL_CARDS:
        if card_id == ALL_CARDS:
