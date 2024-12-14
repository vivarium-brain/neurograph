SYNAPTIC_SECTION_ID = 0x00

def ReadSynapticSection(neurograph):
    return neurograph.handle.ReadStringLPS()

def WriteSynapticSection(neurograph, name):
    neurograph.handle.WriteStringLPS(name)