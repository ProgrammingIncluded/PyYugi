import math
import random
from game import Game

###   Everywhere in this file, state is an object that implements the following
###
###   state.play_action(action) -> state
###   state.next() -> [action]
###   state.game_over() -> Boolean
###   state.is_lose() -> Boolean

# rollout(state) -> state
# rollout plays the game starting from state, taking random actions until
# it reaches a terminal state
def rollout(state):
    if state.game_over():
        return 0 if state.is_lose() else 1

    next_state = state.play_action(random_action(state))
    return rollout(next_state)

# random_action(state) -> action
def random_action(state):
    actions = state.next()
    return random.choice(actions)

# MCTS_policy(state, int) -> action
# MCTS uses monte carlo tree search to find the best action to take,
# after exploring num_nodes number of nodes.
def MCTS_policy(state, num_nodes=1000):
    root = MCTS(state)
    s = root

    for n in num_nodes:

        #get leaf that is greedily the best descendant 
        while not s.is_leaf:
            s = s.best_child()[0]

        # already seen it once, need to get to its children
        if s.t != 0:
            s.expand()
            s = s.children[0][0]
        s.v = rollout(s.state)
        s.update_ancestors()

    return s.best_child()[1]

# MCTS
# MCTS is a tree that has the following attributes:
# state: state
# parent: MCTS
# children: [[MCTS, action]] , where action is the action taken to get to the child
# val: float , where val is the average UCB values of the children
# t: int, where t is the times this node has been visited
# is_root: Boolean, where is_root is whether or not this node has a parent
class MCTS:
    self.state = None
    self.parent = None
    self.children = []
    self.val = 0
    self.t = 0
    self.is_root = False
    self.is_leaf = False

    def __init__(self, state, parent=None):
        self.parent = parent
        self.state = state
        self.is_root = not self.parent
        self.is_leaf = self.state.game_over()
    
    # update_ancestors: for each node in the ancestry line (starting at this node
    # and ending at the root), update its val to be their children's avg UCB
    def update_ancestors(self):
        self.t += 1
        if len(children) == 0:
            self.val = float("inf")
        else:
            self.val = sum([c[0].val for c in self.children])/len(self.children)
        if not is_root:
            parent.update_ancestors()

    # Compute UCB using a formula
    def UCB(self):
        return self.val + 2*math.sqrt( math.ln(self.parent_t())/self.t)

    # returns number of times parent was visited, unless parent is root
    def parent_t(self):
        if self.is_root:
            return 0
        return self.parent.t

    # argmax over all the children for their UCB value
    def best_child(self):
        extended_children = [[c[0], c[1], c[1].UCB()] for c in self.state.children]
        for s, a, v in extended_children:
            if v == float("inf"):
                return [s, a]
 
        return max(extended_children, key=lambda x:x[2])[0:1]

    # populate children with [MCTS, action] where action is one of the possible
    # actions from this state, along with the consequential MCTS
    def expand(self):
        if len(self.children) == 0:
            actions = self.state.next()
            self.children = [[a, MCTS(self.state.play_action(a), self)] for a in actions]
