import os_paths
import yugidb.yugi_db as db
from playfield import *
from collections import defaultdict
# Some common utils

# Search stats in list using id
def search_card(id, li):
    for c in li:
        if c["id"] == str(id):
            return c
    return None

# Expands a list of card names to count data to unitary card items.
def expand_cards(cards):
    result = []
    for c in cards:
        for x in range(0, c["count"]):
            result.append({k: v for k, v in c.items() if k != "count"})
    return result

# Count recurring cards and print the count instead.
def compress_cards(cards):
    comp = {}
    for c in cards:
        if c["name"] not in comp:
            comp[c["name"]] = [1, {k: v for k, v in c.items()}]
        else:
            comp[c["name"]][0] += 1
    
    result = []
    for k, v in comp.items():
        v[1]["count"] = v[0]
        result.append(v[1])
    return result

def count_compress_cards(cards):
    count = 0
    for c in cards:
        count += int(c["count"])
    return count

# Simple card print, dumps dictionary to string
def cards_to_string(cards, preserve_face=False):
    clen = len(cards)
    if clen == 0:
        return ""
    result = []

    face = 0
    name = cards[0]["name"]
    if "cardface" in cards[0]:
        face = cards[0]["cardface"]

    face_str = cf_to_string(face)
    if preserve_face and face < 0:
        name = cf_to_string(face)
    elif face_str != "":
        name +=  " " + "(" + face_str + ")"


    if "count" not in cards[0]:
        result = name
    else:
        result = name + " (" + str(cards[0]["count"]) + ")"
        
    
    for i in range(1, clen): 
        face = 0

        if "cardface" in cards[i]:
            face = cards[i]["cardface"]

        name = cards[i]["name"]
        face_str = cf_to_string(face)
        if preserve_face and cards[i]["cardface"] < 0:
            name = face_str
        elif face_str != "":
            name += " " + "(" + face_str + ")"
            

        if "count" not in cards[i]:
            result += "\n " + name  
        else:
            result += "\n" + name + " (" + str(cards[i]["count"]) + ")"
    return result

# Print cards in a mult-array setting like fields array
def multi_cards_to_string(cards, preserve_face=False):
    res = ""
    count = 0
    for ar in cards:
        res += "\nPos " + str(count) + "\n"
        res += cards_to_string(ar, preserve_face)
        count += 1
    return res

# Counts cards in multi array settings
# like the field array
def multi_array_count(array):
    count = 0
    for p in array:
        if len(p) != 0:
            count += 1
    return count 

# Condense multidimensional array
# into single.
def condense_multi(array):
    res = []
    for p in array:
        res += p
    return res

# Helper function to group cards by type.
# Returns dictionary of index by cards
def group_card_type(cards):
    res = defaultdict(list)
    for i in range(0, len(cards)):
        c = cards[i]
        stats = db.get_card_stat(c["id"])
        typ = gen_type(stats["type"])
        res[typ].append(i)
    return res
    
# Get card position to string
def cf_to_string(face):
    if int(face) == FACE_DOWN_ATK:
        return "Face Down"
    elif int(face) == FACE_DOWN_DEF:
        return "Face Down Defense"
    elif int(face) == FACE_UP_ATK:
        return "Face Up"
    elif int(face) == FACE_UP_DEF:
        return "Face Up Defense"
    return ""

# Check if card is of a generic type. More coarse definition.
def gen_type(typ):
    tokens = typ.lower().split(' ')
    if tokens[0] == "fusion":
        return "fusion"
    elif tokens[0] == "link":
        return "link"
    elif tokens[0] == "synchro":
        return "synchro"
    elif tokens[0] == "xyz":
        return "xyz"
    elif tokens[-1] == "monster":
        return "monster"
    elif tokens[0] == "spell":
        return "spell"
    elif tokens[0] == "trap":
        return "trap"
    elif tokens[0] == "skill":
        return "skill"
    return "unkown"