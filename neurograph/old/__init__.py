from .neurograph_v1 import GoogerNeurographV1
from .neurograph_v2 import GoogerNeurographV2

__all__ = ["Neurograph"]

bases = {
    1: GoogerNeurographV1,
    2: GoogerNeurographV2
}


# noinspection PyTypeChecker
class Neurograph:
    def __init__(self, path, mode, *args, version=2, **kwargs):
        stream = open(path, mode + "b")
        if mode == "r":
            self.version, self.name, self.author = self.readHeader(stream)
            if bases.get(self.version):
                self.base = bases.get(self.version)(path, 'r', self, *args, **kwargs)
            else:
                raise ValueError(f"Unknown neurograph version {self.version}")
        if mode == "w":
            self.version = version
            self.name, self.author = args[0:2]
            if bases.get(self.version):
                self.base = bases.get(self.version)(path, 'w', self, *args[3:], **kwargs)
            else:
                raise ValueError(f"Unknown neurograph version {self.version}")
            self.writeHeader(stream)

    def flush(self):
        self.base.flush()

    def close(self):
        self.base.close()

    def __str__(self):
        return f"[Neurograph version={self.version} author=\"{self.author}\" name=\"{self.name}\"]"

    def writeHeader(self, stream):
        stream.write(b"NGRP")
        stream.write(self.version.to_bytes(1, 'little'))
        stream.write(len(self.name.encode()).to_bytes(1, 'little'))
        stream.write(self.name.encode())
        stream.write(len(self.author.encode()).to_bytes(1, 'little'))
        stream.write(self.author.encode())
        stream.flush()

    @staticmethod
    def readHeader(stream):
        stream.read(4)
        version = int.from_bytes(stream.read(1), 'little')
        name = stream.read(int.from_bytes(stream.read(1), 'little')).decode()
        author = stream.read(int.from_bytes(stream.read(1), 'little')).decode()
        return version, name, author

    def getDendrites(self, *args, **kwargs):
        return self.base.getDendrites(*args, **kwargs)

    def setDendrites(self, *args, **kwargs):
        return self.base.setDendrites(*args, **kwargs)

    def getSynaptic(self, *args, **kwargs):
        return self.base.getSynaptic(*args, **kwargs)

    def setSynaptic(self, *args, **kwargs):
        return self.base.setSynaptic(*args, **kwargs)
