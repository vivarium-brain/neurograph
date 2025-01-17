import io
import os
import struct


class ReaderWriter:
    def __init__(self, handle: io.BytesIO, mode: str):
        if mode != "w" and mode != "r":
            raise Exception("unexpected mode \"" + mode + "\"")
        self.handle = handle
        self.mode = mode

    @classmethod
    def fromFile(cls, path: str, mode: str):
        if mode == "w":
            handle = open(path, "wb")
        elif mode == "r":
            handle = open(path, "rb")
        else:
            raise Exception("unexpected mode \"" + mode + "\"")
        return cls(handle, mode)

    @classmethod
    def fromNoFile(cls, data: bytes, mode: str):
        return cls(io.BytesIO(data), mode)

    def close(self):
        self.flush()
        self.handle.close()

    def flush(self):
        self.handle.flush()

    def seek(self, n):
        self.handle.seek(n)

    def tell(self):
        return self.handle.tell()

    def size(self):
        tell = self.tell()
        self.handle.seek(0, os.SEEK_END)
        size = self.tell()
        self.seek(tell)
        return size

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
        string = [bytes([i]) for i in (string.encode())]
        self.handle.write(struct.pack("B", len(string)))
        self.handle.write(struct.pack("c"*len(string), *string))

    def ReadStringLPS(self) -> str:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return self.handle.read(struct.unpack('B', self.handle.read(1))[0]).decode()

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

    def WriteBool(self, bool: bool):
        self.WriteUByte(0xFF if bool else 0x00)
    
    def ReadBool(self) -> bool:
        return self.ReadUByte() == 0xFF

    def WriteFloat(self, num: int):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        self.handle.write(struct.pack("f", num))

    def ReadFloat(self) -> int:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return struct.unpack("f", self.handle.read(1))[0]

    def WriteDouble(self, num: int):
        if self.mode != "w":
            raise IOError("not open in writing mode")
        self.handle.write(struct.pack("d", num))

    def ReadDouble(self) -> int:
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return struct.unpack("d", self.handle.read(1))[0]