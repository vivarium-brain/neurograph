NAME_HEADER_ID = 0x00

def ReadNameHeader(neurograph):
    return neurograph.handle.ReadStringLPS()

def WriteNameHeader(neurograph, name):
    neurograph.handle.WriteStringLPS(name)