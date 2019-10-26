import random
import card_util as cu
from playfield import *
from mechanics import *
from actions import *
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
    
    # keeps track of reaction
    # -1 means no reaction
    # 0 means a reaction is in progress
    # 1 means a reaction is returned without a reactions
    react = 0 

    # Playfield variables
    pf = Playfield()

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

    # function to check what are some actions we can take.
    # Actions are grouped per field section per card, then action index.
    def gen_actions(self):
        # Clear the actions list.
        self.actions = defaultdict(lambda: defaultdict( lambda: defaultdict(int)))

        # Do the HAND deck first
        # Optimization: Grab the spell cards
        # TODO: Automate this field specification
        org = cu.group_card_type(self.pf.HAND[self.cur_player])
        for typ in org.keys():
            self._gen_specific_action("hand", typ, org[typ])

        return dict(self.actions)
    
    # Play a specific action given by gen_actions
    # Play action with a specific orientation
    # Play action at specific position if applicable
    def play_action(self, act, face = FACE_UP_ATK, pos=0):
        if act != None:
            # Play the action
            params = act[1]
            params[0](params[1], params[2], pos, face)

            if self.react == 0:
                self.react = 1
        else:
            # Increase our reaction count
            if self.react != 0:
                self.react += 1
        
        # No one has played twice in a row, remove our toggles
        # otherwise, toggle and end 
        if self.react == 3 or self.react == 0:
            self.react = 0
            # Resolve our stack
            resolve_stack()
        else:
            self.toggle_player()

    def is_reponse(self):
        return (self.react != 0)

    # toggle player
    def toggle_player(self):
        if self.cur_player == P1:
            self.cur_player = P2
        else:
            self.cur_player = P1

    # Start the game by drawing cards
    def start(self):
        # Draw multiple times.
        for i in range(0, self.start_draw):
            draw(self.pf, P1)
            draw(self.pf, P2)
        # Commit the actions
        resolve_stack(self.pf)

    # function to return available options
    def next(self):
        actions = self.gen_actions()
        return actions

    #
    # Private Functions
    #

    def _gen_specific_action(self, fro, typ, cardind):
        """Helper function for gen_action to generate type list."""
        for rule, func in MECH_LIST[fro][typ].items():
            for ind in cardind:
                if func(self.cur_player, ind):
                    # Get available positions
                    pos = POS_LIST[fro][typ][rule]
                    # Create a callable system
                    # does not encode available positions
                    params = (ACTION_LIST[fro][typ][rule], self.cur_player, ind, pos)
                    self.actions[fro][HAND[self.cur_player][ind]["name"]][rule] = (rule, params)



    # Iteration functions for ease of use.
    def __iter__(self):
        return self
    
    def __next__(self):
        if lose_state(self.pf):
            raise StopIteration
        return self.next()

