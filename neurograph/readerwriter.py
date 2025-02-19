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
        return self.handle.write(data)

    def ReadData(self, amount: int):
        if self.mode != "r":
            raise IOError("not open in reading mode")
        return self.handle.read(amount)


    def WriteStringNT(self, string: str):
        string = [bytes([i]) for i in (string.encode() + b"\0")]
        self.WriteData(struct.pack("c"*len(string), *string))

    def ReadStringNT(self) -> str:
        string = b""
        read = self.ReadData(1)
        while read[0] != 0:
            string += read
            read = self.ReadData(1)
        return string.decode()

    def WriteU8(self, num: int):
        self.WriteData(struct.pack("B", num))

    def ReadU8(self) -> int:
        return struct.unpack("B", self.ReadData(1))[0]


    def WriteI8(self, num: int):
        self.WriteData(struct.pack("b", num))

    def ReadI8(self) -> int:
        return struct.unpack("b", self.ReadData(1))[0]

    def WriteU16(self, num: int):
        self.WriteData(struct.pack("H", num))

    def ReadU16(self) -> int:
        return struct.unpack("H", self.ReadData(2))[0]

    def WriteI16(self, num: int):
        self.WriteData(struct.pack("h", num))

    def ReadI16(self) -> int:
        return struct.unpack("h", self.ReadData(2))[0]

    def WriteU32(self, num: int):
        self.WriteData(struct.pack("I", num))

    def ReadU32(self) -> int:
        return struct.unpack("I", self.ReadData(4))[0]

    def WriteI32(self, num: int):
        self.WriteData(struct.pack("i", num))

    def ReadI32(self) -> int:
        return struct.unpack("i", self.ReadData(4))[0]

    def WriteU64(self, num: int):
        self.WriteData(struct.pack("Q", num))

    def ReadU64(self) -> int:
        return struct.unpack("Q", self.ReadData(8))[0]

    def WriteI64(self, num: int):
        self.WriteData(struct.pack("q", num))

    def ReadI64(self) -> int:
        return struct.unpack("q", self.ReadData(8))[0]


    def WriteBool(self, bool: bool):
        self.WriteU8(0xFF if bool else 0x00)
    
    def ReadBool(self) -> bool:
        return self.ReadU8() == 0xFF
    

    def WriteFloat(self, num: int):
        self.WriteData(struct.pack("f", num))

    def ReadFloat(self) -> int:
        return struct.unpack("f", self.ReadData(1))[0]

    def WriteDouble(self, num: int):
        self.WriteData(struct.pack("d", num))

    def ReadDouble(self) -> int:
        return struct.unpack("d", self.ReadData(1))[0]
    
    def WriteStringLPS(self, string: str):
        string = [bytes([i]) for i in (string.encode())]
        self.WriteU8(len(string))
        self.WriteData(struct.pack("c"*len(string), *string))

    def ReadStringLPS(self) -> str:
        return self.ReadData(self.ReadU8()).decode()

    def WriteStringLPL(self, string: str):
        string = [bytes([i]) for i in (string.encode())]
        self.WriteU16(len(string))
        self.WriteData(struct.pack("c"*len(string), *string))

    def ReadStringLPL(self) -> str:
        return self.ReadData(self.ReadU16()).decode()