
import re
import codecs

def find_acc_name(text):
    r = re.findall("\(([\w\säÄöÖüÜß\.~+\-@*!]+)\[",text)  #https://regex101.com/
    if r == []:
        return None
    return r[0][:-1]

def find_coords(text):
    r = re.findall("\(([0-9]+\|[0-9]+)\)",text)
    if r == []:
        return None
    s = r[-1].split("|")
    return int(s[0])*1000+int(s[1])

def parse_troops(text, has_bows, has_paladin):
    lines = text.split("\n")
    bh, types = get_troops_types(has_bows, has_paladin)
    internal = {}
    external = {}
    for type in types: #{"spear": 0, "sword" = 0, ...}
        internal[type] = 0

    for line in lines:
        values = line.split("\t")
        if values[1] == "im Dorf ":
            #interne Truppen
            troops = values[2:-2]
            i = 0
            for type in types:
                internal[type] += int(troops[i])
                i += 1
        else:
            #externe Truppen
            acc = find_acc_name(values[1])
            coord = find_coords(values[0])
            if acc == None:
                #support in own villages
                acc = "self"
            if acc not in external: external[acc] = {}
            if coord not in external[acc]: external[acc][coord] = 0
            external[acc][coord] += add_up_external(types, bh, values[3:])
    return internal, external

def add_up_external(types, bh, troops):
    i = 0
    sum = 0
    for type in types:
        sum += int(troops[i]) * bh[type]
        i += 1
    return sum

def get_troops_types(has_bows, has_paladin):
    if has_bows:
        if has_paladin:
            bh = {"spear":1,"sword":1,"axe":1,"archer":1,"spy":2,"light":4,"marcher":5,"heavy":6,"ram":5,"catapult":8,"knight":10,"snob":100}
            types = ["spear","sword","axe","archer","spy","light","marcher","heavy","ram","catapult","knight","snob"]
        else:
            bh = {"spear":1,"sword":1,"axe":1,"archer":1,"spy":2,"light":4,"marcher":5,"heavy":6,"ram":5,"catapult":8,"snob":100}
            types = ["spear","sword","axe","archer","spy","light","marcher","heavy","ram","catapult","snob"]
    else:
        if has_paladin:
            bh = {"spear":1,"sword":1,"axe":1,"spy":2,"light":4,"heavy":6,"ram":5,"catapult":8,"knight":10,"snob":100}
            types = ["spear","sword","axe","spy","light","heavy","ram","catapult","knight","snob"]
        else:
            bh = {"spear":1,"sword":1,"axe":1,"spy":2,"light":4,"heavy":6,"ram":5,"catapult":8,"snob":100}
            types = ["spear","sword","axe","spy","light","heavy","ram","catapult","snob"]
    return bh, types
