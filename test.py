from neurograph import openng

neurograph = openng("test.ng1", 'w', True)
neurograph.headers["name"] = ["DUMMY"]
neurograph.sections["index"] = [[
    "0", "1", "2"
]]
neurograph.sections["synaptic"] = [{
    0: {1: 10},
    1: {2: 10},
    2: {0: 10},
}]
neurograph.close()

neurograph = openng("test.ng1", 'r')
print(neurograph.headers)
print(neurograph.sections)
neurograph.close()