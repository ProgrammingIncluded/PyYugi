import ld_deck as ldd
import yugi_db as db
from playfield import *
import mechanics as m

def main():
    db.load_card_names()
    set_deck(P1, ldd.load_deck("maldoche"))
    set_deck(P2, ldd.load_deck("maldoche"))
    shuffle_deck(P1)
    shuffle_deck(P2)

    print("\n")

    # Draw card
    draw(P1)
    draw(P1)
    print(m.can_summon_normal(P1, 0))
    summon(P1, 0, 0, True)
    print(m.can_summon_normal(P1, 0))
    print(allinfo(P1))
    
    db.unload_card_names()

if __name__ == '__main__':
    main()