from playfield import *

# File to hold all the viable actions.
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

## Action Related Card Functions ##
# All these functions must only have 4 parameters
# Player, cardind relative to a set of cards, field position
# and cardfaceindex for the flipping of the card if applicable.
#
# Yes, that means that you are able to set a spell but put it face up
# or you can set a card face up in hand. This leave interpretation
# in the future or for custom rules in card decks.

# Summon a card from deck to hand. Does not check validity rules.
def normal_summon(player, cardind, fpos, cardfaceind=FACE_UP_ATK):
    def _normal_summon():
        FIELD[player][fpos].insert(0, HAND[player].pop(cardind))
        FIELD[player][fpos][0]["cardface"] = cardfaceind
        global PREV_NORM_SUMMON
        PREV_NORM_SUMMON = ROUND_CNT
        return FIELD[player][fpos]
    AS.append(_normal_summon)

# Similar to normal summon but does not tick the normal summon ticker.
def special_summon(player, cardind, fpos, cardfaceind = FACE_UP_ATK):
    def _special_summon():
        FIELD[player][fpos].insert(0, HAND[player].pop(cardind))
        FIELD[player][fpos][0]["cardface"] = cardfaceind
        global PREV_NORM_SUMMON
        PREV_NORM_SUMMON = ROUND_CNT
        return FIELD[player][fpos]
    AS.append(_special_summon)

 # Play a spell from hand
def play_spell(player, handind, fpos, cardfaceind = FACE_UP_SPELL):
    pass

# Activate a spell from the field
def activate_spell(player, spellind, fpos, cardfaceind = FACE_UP_SPELL):
    pass

# SPELL RELATED FUNCTIONS
# Set a spell card, sets a roundset
# flag in order to keep track of setting.
def set_spell(player, handind, fpos, cardfaceind = FACE_DOWN_SPELL):
    def _set_spell():
        SPELL[player][fpos].insert(0, HAND[player].pop(handind))
        SPELL[player][fpos]["cardface"] = cardfaceind
    AS.append(_set_spell)

ACTION_LIST = {
    "hand": {
        "monster": {
            "Normal Summon": normal_summon,
        },

        "spell": {
            "Set Spell": set_spell,
            "Play Spell": play_spell,
        },

        "trap": {
            "Set Trap": set_spell,
            "Play Trap": play_spell,
        }
    },

    "play": {
        
    }
}