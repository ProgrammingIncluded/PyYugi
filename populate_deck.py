from get_card_from_image import get_card_from_image
from os import listdir
from os.path import isfile, join
from yugidb import load_card_names

card_images = [f for f in listdir('card_images') if isfile(join('card_images', f))]

load_card_names()

deck = open('deck.csv', 'w')

for i in card_images:
    card_stats = get_card_from_image('card_images/' + i)
    if card_stats is not None:
        if card_stats['type'] not in ['XYZ Monster', 'Link Monster', 'Synchro Monster', 'Pendulum Monster']:
            deck.write(card_stats['name'] + "\n")
    else:
        print("Could not classify " + i)

deck.write('EXT:\n')

for i in card_images:
    card_stats = get_card_from_image('card_images/' + i)
    if card_stats is not None:
        if card_stats['type'] in ['XYZ Monster', 'Link Monster', 'Synchro Monster', 'Pendulum Monster']:
            deck.write(card_stats['name'] + "\n")

deck.close()