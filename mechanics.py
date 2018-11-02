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


# check if the player has won
# Only check lifepoints and deck size.
def player_win(player):
    if LP[player] <= 0:
        return True
    elif len(DECK[player]) == 0:
        return True
    return False