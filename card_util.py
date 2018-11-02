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
def cards_to_string(cards):
    clen = len(cards)
    if clen == 0:
        return ""
    result = []
    if "count" not in cards[0]:
        result = cards[0]["name"]
    else:
        result = cards[0]["name"] + " (" + str(cards[0]["count"]) + ")"
    
    for i in range(1, clen): 
        if "count" not in cards[i]:
            result += "\n " + cards[i]["name"]
        else:
            result += "\n" + cards[i]["name"] + " (" + str(cards[i]["count"]) + ")"
    return result

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