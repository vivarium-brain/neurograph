import zlib

from .readerwriter import ReaderWriter

from .headers.header_name import ReadNameHeader, WriteNameHeader, NAME_HEADER_ID

HEADERS = {
    NAME_HEADER_ID: ["name",  ReadNameHeader],

    "name": [NAME_HEADER_ID, WriteNameHeader]
}

class NeurographBase:
    SECTIONS = {}

    def __init__(self, path, mode='r', flat=True, handle=None):
        self.headers = {}
        self.sections = {}

        self.path = path
        self.mode = mode
        self.flat = flat

        if handle:
            self.handle = handle
        else:
            self.handle = ReaderWriter.fromFile(path, mode)

        if mode == "r":
            self.ReadHeaders()
            self.ReadSections()

    def close(self):
        if self.mode == 'w':
            self.WriteHeaders()
            self.WriteSections()
        self.handle.close()

    def HEAD_WriteSection(self, name: str, *data):
        hid, writer = HEADERS.get(name.lower())
        assert hid != None, f"No such header: {name}"
        self.handle.WriteU8(hid)
        writer(self, *data)

    def HEAD_ReadSection(self):
        sid = self.handle.ReadU8()
        name, reader = HEADERS.get(sid, [None, None])
        assert reader != None, f"Unknown header: {sid}"
        return name, reader(self)

    def BODY_WriteSection(self, name: str, *data):
        sid, writer = self.SECTIONS.get(name.lower(), [None, None])
        assert sid != None, f"No such section: {name}"

        handle = ReaderWriter.fromNoFile(b'', 'w')
        writer(self, handle, *data)
        handle.seek(0)
        handle.mode = 'r'

        raw = handle.ReadData(handle.size())
        crc = zlib.crc32(raw)

        self.handle.WriteU8(sid)
        self.handle.WriteI64(crc)
        self.handle.WriteU32(len(raw))
        self.handle.WriteData(raw)

    def BODY_ReadSection(self):
        hid = self.handle.ReadU8()
        crc = self.handle.ReadI64()
        size = self.handle.ReadU32()
        name, reader = self.SECTIONS.get(hid)
        assert reader != None, f"Unknown section: {hid}"
        raw = self.handle.ReadData(size)

        real_crc = zlib.crc32(raw)
        assert crc == real_crc, f"Section '{name}' checksum mismatch: {crc} ~= {real_crc}!"

        handle = ReaderWriter.fromNoFile(raw, 'r')
        data = reader(self, handle)
        return name, data

    def ReadHeaders(self):
        for _ in range(self.handle.ReadU8()):
            name, *data = self.HEAD_ReadSection()
            self.headers[name] = data

    def WriteHeaders(self):
        self.handle.WriteU8(len(self.headers))
        for name, data in self.headers.items():
            self.HEAD_WriteSection(name, *data)

    def ReadSections(self):
        while self.handle.tell() < self.handle.size():
            name, *data = self.BODY_ReadSection()
            self.sections[name] = data

    def WriteSections(self):
        for name, data in self.sections.items():
            self.BODY_WriteSection(name, *data)