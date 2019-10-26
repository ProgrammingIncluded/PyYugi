import random as rand
import card_util as cu

# Index values for player 1 and 2.
P1 = 0
P2 = 1

class Playfield:
    """Class to hold variables that define a playfield"""

    # Check the action stack
    # Action stack is stored as 
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

    # String to array mapping of field positions
    FIELD_POS = {
        "hand": HAND,
        "field": FIELD,
        "pend": PEND,
        "grave": GRAV,
        "extm": EXTM,
        "ban": BAN,
        "spell": SPELL
    }

    # Array of field names for ease of use
    FIELD_NAMES = list(FIELD_POS.keys())

# Increment a phase
# starts a new round if finish phases.
def next_phase(pf):
    pf.CUR_PHASE += 1
    if pf.CUR_PHASE >= 5:
        new_round()
    # Clear the action stack
    AS = []

# Resolve the global stack.
def resolve_stack(pf):
    resolve_stack_rec(pf.AS)

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
def new_round(pf):
    pf.CUR_PHASE = 0
    pf.ROUND_CNT += 1
    AS = []

# Types of card positions
# FD is mainly for spells being facedown
CARD_POS = ["FU_ATK", "FU_DEF", "FD_DEF", "FD"]

# All face up is > 0  and all face down is < 0
# Card position definitions
FACE_UP_ATK = 1
FACE_UP_DEF = 2
FACE_DOWN_ATK = -1
FACE_DOWN_DEF = -2

# Same enumeration from before, mainly for syntactic sugar.
FACE_UP_SPELL = 1
FACE_DOWN_SPELL = -1


#
# Playfield print functions
#

# Print all deck info
def startdeckinfo(pf, player):
    result = "\nStarting Deck Total(" + str(cu.count_compress_cards(pf.DECK[player])) + "): \n" 
    result += cu.cards_to_string(pf.DECK[player])
    result += "\n"
    result += "\nStarting EXT Deck Total(" + str(len(pf.EXTD[player])) + "): \n" 
    result += cu.cards_to_string(pf.EXTD[player])
    result += "\n"
    return result

# All cards destroyed
def destroyedinfo(pf, player):
    result = "\n"
    ult = ""
    ult += "\nGraveyard Total(" + str(len(pf.GRAV[player])) + "): \n" 
    ult += cu.cards_to_string(cu.compress_cards(pf.GRAV[player]))
    result += "\n"
    result += "\nBan Total(" + str(len(pf.BAN[player])) + "): \n" 
    result = cu.cards_to_string(cu.compress_cards(pf.BAN[player]))
    result += "\n"
    return result

def handinfo(pf, player):
    result = "\n"
    result += "\nHand Total(" + str(len(pf.HAND[player])) + "): \n" 
    result += cu.cards_to_string(cu.compress_cards(pf.HAND[player]))
    result += "\n"
    return result

def fieldinfo(pf, player):
    other = 1 - player
    result = "\nEXT Monster Total(" + str(len(pf.EXTM[player])) + "): \n" 
    result += "\nPLAYER:"
    result += cu.cards_to_string(pf.EXTM[player])
    result += "\nOPPONENT:"
    result += cu.cards_to_string(pf.EXTM[other], True)
    result += "\n"
    result += "\nField Total(" + str(cu.multi_array_count(pf.FIELD[player])) + "): \n" 
    print(pf.FIELD)
    result += "\nPLAYER:"
    result += cu.multi_cards_to_string(pf.FIELD[player])
    result += "\nOPPONENT:"
    result += cu.multi_cards_to_string(pf.FIELD[other], True)
    result += "\n"
    return result

# Returns string with all the info regarding the current player
def cardinfo(pf, player):
    result = "\nDeck Total(" + str(len(pf.WKDECK[player])) + "): \n" 
    result += cu.cards_to_string(cu.compress_cards(pf.WKDECK[player]))
    result += "\n"
    return result

def allinfo(pf, player):
    result = startdeckinfo(pf, player)
    result += handinfo(pf, player)
    result += cardinfo(pf, player)
    result += fieldinfo(pf, player)
    result += destroyedinfo(pf, player)
    return result
