"""File that houses all card effects. Will eventually be moved into card_logic.
Right now each card logic is added via c_<card_id>.
"""

# Called by the Grave
def c_24224830():
    print("Called by the Grave ACTIVATED")

EFFECTS = {
    24224830: c_24224830
}

# Sort our global value
# EFFECTS = sorted(EFFECTS.iterkeys())