from neurograph_base import NeurographBase

from sections.section_synaptic import ReadSynapticSection, WriteSynapticSection, SYNAPTIC_SECTION_ID

SECTIONS = {
    SYNAPTIC_SECTION_ID: ["synaptic",  ReadSynapticSection],

    "synaptic": [SYNAPTIC_SECTION_ID, WriteSynapticSection]
}

class Neurograph(NeurographBase):
    def BODY_WriteSection(self, name: str, *data):
        sid, writer = SECTIONS.get(name.lower())
        assert sid != None, f"No such section: {name}"
        self.WriteUByte(sid)
        writer(self, *data)

    def BODY_ReadSection(self):
        sid = self.ReadUByte()
        name, reader = SECTIONS.get(sid)
        assert reader != None, f"Unknown section: {sid}"
        return name, reader(self)