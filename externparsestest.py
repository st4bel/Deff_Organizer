import os
import re
import codecs

def find_acc_name(text):
    return re.search("\(([\w\säÄöÖüÜß\.~+\-@*!]+)\[",text) #https://regex101.com/

filename = "externtroops.txt"

with codecs.open(filename,"r","utf-8") as f:
    lines = [line.rstrip() for line in f]

for line in lines:
    values = line.split("\t")
    if values[1] != "" and values[1] != "im Dorf ":
        accname =find_acc_name(line)#values[1])
        print(values[1])
        if accname != []:
            print(accname)
        else:
            print("--------------------------------------------------")
