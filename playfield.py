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
# No support stacking midway.
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

# All face up is > 0  and all face down is < 0
# Card position definitions
FACE_UP_ATK = 1
FACE_UP_DEF = 2
FACE_DOWN_ATK = -1
FACE_DOWN_DEF = -2

# Same enumeration from before, mainly for syntactic sugar.
FACE_UP_SPELL = 1
FACE_DOWN_SPELL = -1

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
    other = 1 - player
    result = "\nEXT Monster Total(" + str(len(EXTM[player])) + "): \n" 
    result += "\nPLAYER:"
    result += cu.cards_to_string(EXTM[player])
    result += "\nOPPONENT:"
    result += cu.cards_to_string(EXTM[other], True)
    result += "\n"
    result += "\nField Total(" + str(cu.multi_array_count(FIELD[player])) + "): \n" 
    print(FIELD)
    result += "\nPLAYER:"
    result += cu.multi_cards_to_string(FIELD[player])
    result += "\nOPPONENT:"
    result += cu.multi_cards_to_string(FIELD[other], True)
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
