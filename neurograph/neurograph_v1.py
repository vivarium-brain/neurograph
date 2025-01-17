from neurograph_base import NeurographBase

SYNAPTIC_SECTION_ID = 0x00

def ReadSynapticSection(neurograph):
    table = {}
    syns = neurograph.handle.ReadULong()
    for _ in range(syns):
        conns = {}
        table[neurograph.handle.ReadStringLPS()] = conns
        cnns = neurograph.handle.ReadULong()
        for _ in range(cnns):
            name = neurograph.handle.ReadStringLPS()
            conns[name] = neurograph.handle.ReadInt()
    return table

def WriteSynapticSection(neurograph, table):
    neurograph.handle.WriteULong(len(table))
    for syn, conns in table.items():
        neurograph.handle.WriteStringLPS(syn)
        neurograph.handle.WriteULong(len(conns))
        for to_syn, weights in conns.items():
            neurograph.handle.WriteStringLPS(to_syn)
            neurograph.handle.WriteInt(weights)

SECTIONS = {
    SYNAPTIC_SECTION_ID: ["synaptic",  ReadSynapticSection],

    "synaptic": [SYNAPTIC_SECTION_ID, WriteSynapticSection]
}

class Neurograph(NeurographBase):
    def BODY_WriteSection(self, name: str, *data):
        sid, writer = SECTIONS.get(name.lower())
        assert sid != None, f"No such section: {name}"
        self.handle.WriteUByte(sid)
        writer(self, *data)

    def BODY_ReadSection(self):
        sid = self.handle.ReadUByte()
        name, reader = SECTIONS.get(sid)
        assert reader != None, f"Unknown section: {sid}"
        return name, reader(self)