from readerwriter import ReaderWriter

from headers.header_name import ReadNameHeader, WriteNameHeader, NAME_HEADER_ID

HEADERS = {
    NAME_HEADER_ID: ["name",  ReadNameHeader],

    "name": [NAME_HEADER_ID, WriteNameHeader]
}

class NeurographBase:
    def __init__(self, path, mode='r', handle=None):
        self.headers = {}

        self.path = path
        self.mode = mode

        if handle:
            self.handle = handle
        else:
            self.handle = ReaderWriter(path, mode)

        if mode == "r":
            self.ReadHeaders()

    def close(self):
        if self.mode == 'w':
            self.WriteHeaders()
        self.handle.close()

    def HEAD_WriteSection(self, name: str, *data):
        hid, writer = HEADERS.get(name.lower())
        assert hid != None, f"No such header: {name}"
        self.handle.WriteUByte(hid)
        writer(self, *data)

    def HEAD_ReadSection(self):
        hid = self.handle.ReadUByte()
        name, reader = HEADERS.get(hid)
        assert reader != None, f"Unknown header: {hid}"
        return name, reader(self)

    def ReadHeaders(self):
        for _ in range(self.handle.ReadUByte()):
            name, *data = self.HEAD_ReadSection()
            self.headers[name] = data

    def WriteHeaders(self):
        self.handle.WriteUByte(len(self.headers))
        for name, data in self.headers.items():
            self.HEAD_WriteSection(name, *data)