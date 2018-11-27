import yugi_db as db
import card_util as cu
from playfield import *


# Phase->start effect->microphase->end effect
# Microphase stack: effect->summon/set->response->effect->...

# Rule checking for summoning a normal monster
# Includes cases for tributing summons
# Does not check if handind is valid.
def can_summon_normal(player, handind):
    # Check if a normal summon had already occurred for this round.
    if PREV_NORM_SUMMON == ROUND_CNT:
        return False

    # Get the stats of the card
    stats = db.get_card_stat(HAND[player][handind]["id"])

    if cu.gen_type(stats["type"]) != "monster" or int(stats["level"]) > 4:
        return False
    return True

# Check if can set spell or trap card
def can_set_spell(player, handind):
    spell_count = cu.multi_array_count(SPELL[player])
    pend_count = cu.multi_array_count(PEND[player])
    if spell_count >= 3 and pend_count >= 2:
        return False
    return True

# Only quick play if quick play card type.
def can_play_spell(player, handind):
    stat = db.get_card_stat(HAND[player][handind]["id"])
    if stat["race"] != "Quick-Play":
        return False
    return True

# Check if we can activate the spell
def can_activate_spell(player, spellind):
    if SPELL[player][spellind][0]["roundset"] == ROUND_CNT:
        return False
    return True

# Position functions return a dict of arrays
# Mainly for those cards that can play in more than one zone.
# e.g. spell cards
# Basic function to get available positions
def avail_summon_pos(player):
    avail = {"field": []}
    for a in FIELD[player]:
        if len(FIELD[player][a]) == 0:
            avail["field"].append(a)
    return avail

# Returns first the spell card zone followed by pend
def avail_spell_pos(player):
    avail = {"spell": [], "pend": []}
    for a in SPELL[player]:
        if len(SPELL[player][a]) == 0:
            avail["spell"].append(a)
    for a in PEND[player]:
        if len(PEND[player][a]) == 0:
            avail["pend"].append(a)

    return avail


# Recall Types as listed in util:
# fusion, link, synchro, xyz, monster, spell, trap, skill
# Function to list positions to play
POS_LIST = {
    "hand": {
        "monster": {
            "Normal Summon": avail_summon_pos,
        },

        "spell": {
            "Set Spell": avail_spell_pos,
            "Play Spell": avail_spell_pos,
        },

        "trap": {
            "Set Trap": avail_spell_pos,
            "Play Trap": avail_spell_pos,
        }
    }
}

# List of actions grouped by type

# also grouped by card location
MECH_LIST = {
    "hand": {
        "monster": {
            "Normal Summon": can_summon_normal,
        },

        "spell": {
            "Set Spell": can_set_spell,
            "Play Spell": can_play_spell,
        },

        "trap": {
            "Set Trap": can_set_spell,
            "Play Trap": can_play_spell,
        }
    }
}

# check if the player has won
# Only check lifepoints and deck size.
def player_lose(player):
    if LP[player] <= 0:
        return True
    elif len(DECK[player]) == 0:
        return True
    return False

# Check if there is a lose state.
def lose_state():
    return (player_lose(P1) or player_lose(P2))