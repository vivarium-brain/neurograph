import struct


class ReaderWriter:
    def __init__(self, path: str, mode: str):
        self.path = path
        self.mode = mode
        if mode == "w":
            self.handle = open(self.path, "wb")
        elif mode == "r":
            self.handle = open(self.path, "rb")
        else:
            raise Exception("unexpected mode \"" + mode + "\"")

    def close(self):
        self.flush()
        self.handle.close()

    def flush(self):
        self.handle.flush()

    def seek(self, n):
        self.handle.seek(n)

    def tell(self):
        return self.handle.tell()

    def WriteData(self, data: bytes):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        self.handle.write(data)

    def ReadData(self, amount: int):
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return self.handle.read(amount)

    def WriteStringNT(self, string: str):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        string = [bytes([i]) for i in (string.encode() + b"\0")]
        self.handle.write(struct.pack("c"*len(string), *string))

    def ReadStringNT(self) -> str:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        string = b""
        read = self.handle.read(1)
        while read[0] != 0:
            string += read
            read = self.handle.read(1)
        return string.decode()

    def WriteStringLPS(self, string: str):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        string = [bytes([i]) for i in (len(string).to_bytes(1)+string.encode())]
        self.handle.write(struct.pack("c"*len(string), *string))

    def ReadStringLPS(self) -> str:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return self.handle.read(int.from_bytes(self.handle.read(1))).decode()

    def WriteStringLPL(self, string: str):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        string = [bytes([i]) for i in (len(string).to_bytes(2)+string.encode())]
        self.handle.write(struct.pack("c"*len(string), *string))

    def ReadStringLPL(self) -> str:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return self.handle.read(int.from_bytes(self.handle.read(2))).decode()

    def WriteUByte(self, num: int):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        self.handle.write(struct.pack("B", num))

    def ReadUByte(self) -> int:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return struct.unpack("B", self.handle.read(1))[0]

    def WriteByte(self, num: int):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        self.handle.write(struct.pack("b", num))

    def ReadByte(self) -> int:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return struct.unpack("b", self.handle.read(1))[0]

    def WriteUShort(self, num: int):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        self.handle.write(struct.pack("H", num))

    def ReadUShort(self) -> int:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return struct.unpack("H", self.handle.read(2))[0]

    def WriteShort(self, num: int):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        self.handle.write(struct.pack("h", num))

    def ReadShort(self) -> int:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return struct.unpack("h", self.handle.read(2))[0]

    def WriteUInt(self, num: int):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        self.handle.write(struct.pack("I", num))

    def ReadUInt(self) -> int:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return struct.unpack("I", self.handle.read(4))[0]

    def WriteInt(self, num: int):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        self.handle.write(struct.pack("i", num))

    def ReadInt(self) -> int:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return struct.unpack("i", self.handle.read(4))[0]

    def WriteULong(self, num: int):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        self.handle.write(struct.pack("Q", num))

    def ReadULong(self) -> int:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return struct.unpack("Q", self.handle.read(8))[0]

    def WriteLong(self, num: int):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        self.handle.write(struct.pack("q", num))

    def ReadLong(self) -> int:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return struct.unpack("q", self.handle.read(8))[0]


if __name__ == "__main__":
    import os
    test = ReaderWriter("test.txt", "w")
    test.WriteStringNT("hello world")
    test.WriteStringNT("hello\0 world")
    test.WriteUByte(1)
    test.WriteByte(-1)
    test.WriteUShort(1)
    test.WriteShort(-1)
    test.WriteUInt(1)
    test.WriteInt(-1)
    test.WriteULong(1)
    test.WriteLong(-1)
    test.close()

    test = ReaderWriter("test.txt", "r")
    assert test.ReadStringNT() == "hello world"
    assert test.ReadStringNT() == "hello"
    assert test.ReadStringNT() == " world"
    assert test.ReadUByte() == 1
    assert test.ReadByte() == -1
    assert test.ReadUShort() == 1
    assert test.ReadShort() == -1
    assert test.ReadUInt() == 1
    assert test.ReadInt() == -1
    assert test.ReadULong() == 1
    assert test.ReadLong() == -1
    test.close()

    print("ok!")
    os.remove("test.txt")