import ld_deck as ldd
import yugi_db as db
import mechanics as m
from game import Game

from playfield import *

def main():
    db.load_card_names()
    set_deck(P1, ldd.load_deck("maldoche"))
    set_deck(P2, ldd.load_deck("maldoche"))
    shuffle_deck(P1)
    shuffle_deck(P2)

    print("\n")
    game = Game()
    game.start()

    print(HAND[P1])
    print(HAND[P2])
    print(game.next())

    db.unload_card_names()

if __name__ == '__main__':
    main()