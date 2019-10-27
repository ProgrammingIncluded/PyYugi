import os_paths
import yugidb as db

def main():
    db.load_card_names()
    
    print("Type e to exit.")
    while(True):
        inp = input("Card Name: ")
        if inp == 'e':
            return 
        try:
            card = db.find_card(inp)
            res = db.get_card_stat(card["id"])
            for k, v in res.items():
                print(k, v)
        except:
            print("Unable to find card.")
        print("\n")

if __name__ == '__main__':
    main()