from neurograph import openng
from neurograph.old import Neurograph

file = "worm"

print("converting neurograph from engine 1 to engine 2")
file = input("file: ")

try:
    new_worm = openng(f"./new{file}.ng1", 'r', True)
    new_worm.close()
except Exception as e:
    print(f"exception while opening last new{file}.ng1: ", e)
else:
    print("neurograph read successful")

print("reading old data...", end="")
old_worm = Neurograph(f"../vivarium/modules/{file}/{file}.ng", 'r')
dendrites = old_worm.getDendrites()
synaptic = old_worm.getSynaptic()
old_worm.close()
print("done")
index = []
new_synaptic = {}

print("building neurite index...", end="")
for dendrite in dendrites:
    if dendrite['name'] in index: continue
    index.append(dendrite['name'])
    for act in dendrite['activations']:
        if act['excited'] in index: continue
        index.append(act['excited'])
print("done")

print("building synaptic table...", end="")
for dendrite in dendrites:
    syn = {}
    new_synaptic[index.index(dendrite['name'])] = syn
    for act in dendrite['activations']:
        if act['excited'] not in index: continue
        syn[index.index(act['excited'])] = act['amount'] * (-1 if act['mode'] == 1 else 1)
print("done")

print("writing neurograph...")
new_worm = openng(f"./new{file}.ng1", 'w', True)
new_worm.sections['synaptic'] = [new_synaptic]
new_worm.sections['index'] = [index]
new_worm.headers['name'] = [input("name: ")]
new_worm.close()