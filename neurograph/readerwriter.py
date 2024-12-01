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
        self.handle.close()

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


if __name__ == "__main__":
    test = ReaderWriter("test.txt", "w")
    test.WriteStringNT("hello world")
    test.WriteStringNT("hello\0 world")
    test.WriteUByte(1)
    test.WriteByte(-1)
    test.close()

    test = ReaderWriter("test.txt", "r")
    assert test.ReadStringNT() == "hello world"
    assert test.ReadStringNT() == "hello"
    assert test.ReadStringNT() == " world"
    assert test.ReadUByte() == 1
    assert test.ReadByte() == -1
    test.close()