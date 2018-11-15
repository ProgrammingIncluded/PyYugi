import random
import card_util as cu
from playfield import *
from mechanics import *
from collections import defaultdict

class Game:
    # Number of cards to draw at the start
    start_draw = 5

    # Who starts first?
    pfirst = P1
    psec = P2
    
    # Who is the current player
    cur_player = -1

    # Default Dictionary to hold actions.
    actions = {}
    

    # Constructor
    def __init__(self):
        # Pick a random character to start
        if random.randint(0, 1) == 0:
            self.pfirst = P1
            self.psec = P2
        else:
            self.pfirst = P2
            self.psec = P1
        self.cur_player = self.pfirst

    # Helper function for gen_action to generate type list.
    def _gen_specific_action(self, fro, typ, cardind):
        for rule, func in MECH_LIST[fro][typ].items():
            for ind in cardind:
                if func(self.cur_player, ind):
                    self.actions[fro][ind].append((rule, ))

    # function to check what are some actions we can take.
    # Actions are grouped per field section per card, then action index.
    def gen_actions(self):
        # Clear the actions list.
        self.actions = defaultdict(
            lambda: {x:[] for x in range(0, len(HAND[self.cur_player]))}
        )

        # Do the HAND deck first
        # Optimization: Grab the spell cards
        # TODO: Automate this field specification
        org = cu.group_card_type(HAND[self.cur_player])
        for typ in org.keys():
            self._gen_specific_action("hand", typ, org[typ])

        return dict(self.actions)
                    
    # Start the game by drawing cards
    def start(self):
        # Draw multiple times.
        for i in range(0, self.start_draw):
            draw(P1)
            draw(P2)
        # Commit the actions
        resolve_stack()

    # function to advance to the next stage
    def next(self):
        actions = self.gen_actions()
        return actions

    # Iteration functions for ease of use.
    def __iter__(self):
        return self
    
    def __next__(self):
        if lose_state():
            raise StopIteration
        return next()
        