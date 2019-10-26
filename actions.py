from playfield import *

# File to hold all the viable actions.
## DECK RELATED FUNCTIONS ##

# Set the deck for player
def set_deck(pf, player, deck):
    pf.DECK[player] = deck[0]
    pf.EXTD[player] = deck[1]
    # Set our internal working deck by expansion
    pf.WKDECK[player] = cu.expand_cards(deck[0])
    pf.WKEXTD[player] = cu.expand_cards(deck[1])
    return pf.DECK[player], pf.EXTD[player]

# Shuffle the deck
def shuffle_deck(pf, player):
    rand.shuffle(pf.DECK[player])

# Function to draw from a deck to hand. Returns cards that was drawn.
# Returns none if deck is empty
def draw(pf, player):
    def _draw():
        maxc = len(pf.WKDECK[player])
        if maxc == 0:
            return None
        ind = rand.randint(0, maxc - 1)
        chose = pf.WKDECK[player].pop(ind)
        pf.HAND[player].append(chose)
    pf.AS.append(_draw)

## Action Related Card Functions ##
# All these functions must only have 4 parameters
# Player, cardind relative to a set of cards, field position
# and cardfaceindex for the flipping of the card if applicable.
#
# Yes, that means that you are able to set a spell but put it face up
# or you can set a card face up in hand. This leave interpretation
# in the future or for custom rules in card decks.

# Summon a card from deck to hand. Does not check validity rules.
def normal_summon(pf, player, cardind, fpos, cardfaceind=FACE_UP_ATK):
    def _normal_summon():
        pf.FIELD[player][fpos].insert(0, pf.HAND[player].pop(cardind))
        pf.FIELD[player][fpos][0]["cardface"] = cardfaceind
        pf.PREV_NORM_SUMMON = pf.ROUND_CNT
        return pf.FIELD[player][fpos]
    pf.AS.append(_normal_summon)

# Similar to normal summon but does not tick the normal summon ticker.
def special_summon(pf, player, cardind, fpos, cardfaceind = FACE_UP_ATK):
    def _special_summon():
        pf.FIELD[player][fpos].insert(0, pf.HAND[player].pop(cardind))
        pf.FIELD[player][fpos][0]["cardface"] = cardfaceind
        pf.PREV_NORM_SUMMON = pf.ROUND_CNT
        return pf.FIELD[player][fpos]
    pf.AS.append(_special_summon)

 # Play a spell from hand
def play_spell(pf, player, handind, fpos, cardfaceind = FACE_UP_SPELL):
    pass

# Activate a spell from the field
def activate_spell(pf, player, spellind, fpos, cardfaceind = FACE_UP_SPELL):
    pass

# SPELL RELATED FUNCTIONS
# Set a spell card, sets a roundset
# flag in order to keep track of setting.
def set_spell(pf, player, handind, fpos, cardfaceind = FACE_DOWN_SPELL):
    def _set_spell():
        pf.SPELL[player][fpos].insert(0, pf.HAND[player].pop(handind))
        pf.SPELL[player][fpos]["cardface"] = cardfaceind
    pf.AS.append(_set_spell)

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