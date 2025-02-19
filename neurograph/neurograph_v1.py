from .neurograph_base import NeurographBase

SYNAPTIC_SECTION_ID = 0x00
INDEX_SECTION_ID = 0x01

######## SYNAPTIC DATA ########

def ReadSynapticSection(neurograph, handle):
    table = {}
    for _ in range(handle.ReadU64()):
        conns = {}
        table[handle.ReadU64()] = conns
        for _ in range(handle.ReadU64()):
            sid = handle.ReadU64()
            conns[sid] = handle.ReadI32()
    return table

def WriteSynapticSection(neurograph, handle, table):
    handle.WriteU64(len(table))
    for syn, conns in table.items():
        handle.WriteU64(syn)
        handle.WriteU64(len(conns))
        for to_syn, weight in conns.items():
            handle.WriteU64(to_syn)
            handle.WriteI32(weight)

######## NEURITE INDEX ########

def ReadIndexSection(neurograph, handle):
    table = []
    for _ in range(handle.ReadU64()):
        table.append(handle.ReadStringLPS())
    return table

def WriteIndexSection(neurograph, handle, table):
    handle.WriteU64(len(table))
    for syn in table:
        handle.WriteStringLPS(syn)

class Neurograph(NeurographBase):
    SECTIONS = {
        SYNAPTIC_SECTION_ID: ["synaptic",  ReadSynapticSection],
        "synaptic": [SYNAPTIC_SECTION_ID, WriteSynapticSection],

        INDEX_SECTION_ID: ["index",  ReadIndexSection],
        "index": [INDEX_SECTION_ID, WriteIndexSection]
    }