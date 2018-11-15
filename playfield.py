import random as rand
import card_util as cu

# File to hold game structures besides card actions.
# Stacking shall be done by location

# Index values for player 1 and 2.
P1 = 0
P2 = 1

# Check the action stack
AS = []

# Current stage settings
# Phase count starts at 0
CUR_PHASE = 0

# Global variable to check if the user has already
# summoned in which round.
PREV_NORM_SUMMON = -1

# List of phase names for reference.

# Check the number of rounds played
# Always increases regardless of the player in play
# So always increases round count as a result.
ROUND_CNT = 0

# Types of card positions
# FD is mainly for spells being facedown
CARD_POS = ["FU_ATK", "FU_DEF", "FD_DEF", "FD"]

# Increment a phase
# starts a new round if finish phases.
def next_phase():
    global CUR_PHASE
    CUR_PHASE += 1
    if CUR_PHASE >= 5:
        new_round()
    # Clear the action stack
    AS = []

# Resolve the global stack.
def resolve_stack():
    global AS
    resolve_stack_rec(AS)

# Resolve_stack can be called recursively
# Hence why we need a stack object
# Called by resolve_stack
def resolve_stack_rec(stack):
    while len(stack) != 0:
        f = stack.pop()
        # Run function
        f()
    stack = []

# Logic to start the next round.
def new_round():
    global CUR_PHASE
    global ROUND_CNT
    CUR_PHASE = 0
    ROUND_CNT += 1
    AS = []

## DECK RELATED FUNCTIONS ##

# Set the deck for player
def set_deck(player, deck):
    DECK[player] = deck[0]
    EXTD[player] = deck[1]
    # Set our internal working deck by expansion
    WKDECK[player] = cu.expand_cards(deck[0])
    WKEXTD[player] = cu.expand_cards(deck[1])
    return DECK[player], EXTD[player]

# Shuffle the deck
def shuffle_deck(player):
    rand.shuffle(DECK[player])

# Function to draw from a deck to hand. Returns cards that was drawn.
# Returns none if deck is empty
def draw(player):
    def _draw():
        maxc = len(WKDECK[player])
        if maxc == 0:
            return None
        ind = rand.randint(0, maxc - 1)
        chose = WKDECK[player].pop(ind)
        HAND[player].append(chose)
    AS.append(_draw)

# Summon a card from deck to hand. Does not check validity rules.
def summon(player, cardind, fpos, isnormal=False, cardfaceind=0):
    def _summon():
        FIELD[player][fpos].insert(0, HAND[player].pop(cardind))
        FIELD[player][fpos][0]["cardface"] = cardfaceind
        if isnormal:
            global PREV_NORM_SUMMON
            PREV_NORM_SUMMON = ROUND_CNT
        return FIELD[player][fpos]
    AS.append(_summon)

# SPELL RELATED FUNCTIONS
# Set a spell card, sets a roundset
# flag in order to keep track of setting.
def set_spell(player, handind, spellind):
    def _set_spell():
        SPELL[player][spellind].insert(0, HAND[player].pop(handind))
        SPELL[player][spellind]["cardface"] = 3
    AS.append(_set_spell)

# Play a spell from hand
def play_spell(player, handind):
    pass

# Activate a spell from the field
def activate_spell(player, spellind):
    pass
    

# Life points
LP = [
    8000, 8000
]

# Each entry has two for each side of the field.
FIELD = [
    [[],[],[],[],[]],
    [[],[],[],[],[]]
]

# Trap contains non-pendulum. 
SPELL = [
    [[] ,[] ,[]],
    [[], [], []]
]

PEND = [
    [[], []],
    [[], []]
]

GRAV = [
    [], []
]

BAN = [
    [], []
]

DECK = [
    [], []
]

WKDECK = [
    [], []
]

EXTD = [
    [], []
]

WKEXTD = [
    [], []
]

EXTM = [
    [], []
]

HAND = [
    [], []
]

FIELD_POS = {
    "hand": HAND,
    "field": FIELD,
    "pend": PEND,
    "grave": GRAV,
    "extm": EXTM,
    "ban": BAN,
    "spell": SPELL
}

FIELD_NAMES = list(FIELD_POS.keys())

# Print all deck info
def startdeckinfo(player):
    result = "\nStarting Deck Total(" + str(cu.count_compress_cards(DECK[player])) + "): \n" 
    result += cu.cards_to_string(DECK[player])
    result += "\n"
    result += "\nStarting EXT Deck Total(" + str(len(EXTD[player])) + "): \n" 
    result += cu.cards_to_string(EXTD[player])
    result += "\n"
    return result

# All cards destroyed
def destroyedinfo(player):
    result = "\n"
    result += "\nGraveyard Total(" + str(len(GRAV[player])) + "): \n" 
    result += cu.cards_to_string(cu.compress_cards(GRAV[player]))
    result += "\n"
    result += "\nBan Total(" + str(len(BAN[player])) + "): \n" 
    result = cu.cards_to_string(cu.compress_cards(BAN[player]))
    result += "\n"
    return result

def handinfo(player):
    result = "\n"
    result += "\nHand Total(" + str(len(HAND[player])) + "): \n" 
    result += cu.cards_to_string(cu.compress_cards(HAND[player]))
    result += "\n"
    return result

def fieldinfo(player):
    result = "\nEXT Monster Total(" + str(len(EXTM[player])) + "): \n" 
    result += cu.cards_to_string(cu.compress_cards(EXTM[player]))
    result += "\n"
    result += "\nField Total(" + str(cu.multi_array_count(FIELD[player])) + "): \n" 
    result += cu.cards_to_string(cu.compress_cards(cu.condense_multi(FIELD[player])))
    result += "\n"
    return result

# Returns string with all the info regarding the current player
def cardinfo(player):
    result = "\nDeck Total(" + str(len(WKDECK[player])) + "): \n" 
    result += cu.cards_to_string(cu.compress_cards(WKDECK[player]))
    result += "\n"
    return result

def allinfo(player):
    result = startdeckinfo(player)
    result += handinfo(player)
    result += cardinfo(player)
    result += fieldinfo(player)
    result += destroyedinfo(player)
    return result
