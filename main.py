import ld_deck as ldd
import yugi_db as db
from actions import *
from game import Game

from playfield import *

# Request user input from specific value
# value is exclusive
def request_input(minval, maxval):
    ex = False
    i = "NONE"
    while not ex:
        i = input("Enter a Number: ")
        if not i.isdigit():
            continue
        i = int(i)
        if i <= maxval and minval <= i:
            ex = True
    return i

# print options as integers
def print_options(options):
    for ind in range(1, len(options) + 1):
        print(ind, ": ", options[ind - 1])
    print()

def main():
    db.load_card_names()
    set_deck(P1, ldd.load_deck("maldoche_test"))
    set_deck(P2, ldd.load_deck("maldoche_test"))
    shuffle_deck(P1)
    shuffle_deck(P2)

    print("\n")
    print("INTIALIZING GAME....")
    game = Game()
    game.start()
    print("GAME HAND INFO FOR CURRENT PLAYER: ")
    print(allinfo(game.cur_player))

    for actions in game:
        if game.is_reponse():
            print("\nRESPONSE P"+ str(game.cur_player + 1))
        else:
            print("\nROUND ", ROUND_CNT + 1)
        # Print currect cards
        print(fieldinfo(game.cur_player))
        print(handinfo(game.cur_player))
        

        fro = -1
        typ = -1
        cardind = -1

        # Get fro info
        fro_opt = list(actions.keys())
        print("Select a Location:")
        print("0 : Do Nothing")
        print_options(fro_opt)
        fro = request_input(0, len(fro_opt))

        # Action if the user chooses to do nothing.
        if fro == 0:
            game.play_action(None)
            continue
            

        fro = fro_opt[fro - 1]
        # Get the specific type
        typ_opt = list(actions[fro].keys())
        print("Select a Card: ")
        print_options(typ_opt)
        typ = request_input(1, len(typ_opt))

        typ = typ_opt[typ - 1]
        # Get our specific card options
        card_opt = list(actions[fro][typ].keys())
        print("Select an Action: ")
        print_options(card_opt)
        cardind = request_input(1, len(card_opt))
        cardind = card_opt[cardind-1]

        # Play the action
        print(actions[fro][typ][cardind])
        game.play_action(actions[fro][typ][cardind])



    db.unload_card_names()

if __name__ == '__main__':
    main()
