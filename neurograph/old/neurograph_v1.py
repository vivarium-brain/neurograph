import io


class GoogerNeurographV1:
    def __init__(self, path, mode, wrapper):
        self.path = path
        self.mode = mode
        self.wrapper = wrapper
        self.stream = None
        if self.mode == 'r':
            self.stream = open(path, "rb")
            self.wrapper.readHeader(self.stream)
            self._readSynaptic()
            self._readDendrites()
            self.stream.close()
            self.stream = None
        else:
            self.synaptic = {}
            self.dendrites = []

    def flush(self):
        if self.mode != 'w':
            return
        self.stream = open(self.path, "wb")
        self.wrapper.writeHeader(self.stream)
        self._writeSynaptic()
        self._writeDendrites()
        self.stream.flush()
        self.stream.close()
        self.stream = None

    def close(self):
        self.flush()

    def setSynaptic(self, synaptic):
        if self.mode != 'w':
            raise io.UnsupportedOperation("not writable")
        self.synaptic = synaptic

    def getSynaptic(self):
        return self.synaptic

    def setDendrites(self, dendrites):
        if self.mode != 'w':
            raise io.UnsupportedOperation("not writable")
        self.dendrites = dendrites

    def getDendrites(self):
        return self.dendrites

    def _writeStringS(self, string):
        self.stream.write(len(string.encode()).to_bytes(1, 'little'))
        self.stream.write(string.encode())

    def _readStringS(self):
        return self.stream.read(int.from_bytes(self.stream.read(1), 'little')).decode()

    def _writeULong(self, ulong):
        self.stream.write(ulong.to_bytes(4, 'little'))

    def _readULong(self):
        return int.from_bytes(self.stream.read(4), 'little')

    def _writeUByte(self, ubyte):
        self.stream.write(ubyte.to_bytes(1, 'little'))

    def _readUByte(self):
        return int.from_bytes(self.stream.read(1), 'little')

    def _writeDendrite(self, dendrite):
        self._writeStringS(dendrite["name"])
        self._writeULong(len(dendrite["activations"]))
        for activation in dendrite["activations"]:
            self._writeStringS(activation["excited"])
            self._writeUByte(activation["amount"])
            self._writeUByte(activation["mode"])

    def _readDendrite(self):
        return {
            "name": self._readStringS(),
            "activations": [{
                "excited": self._readStringS(),
                "amount": self._readUByte(),
                "mode": self._readUByte()
            } for _ in range(self._readULong())]
        }

    def _writeDendrites(self):
        self._writeULong(len(self.dendrites))
        for dendrite in self.dendrites:
            self._writeDendrite(dendrite)

    def _readDendrites(self):
        self.dendrites = [self._readDendrite() for _ in range(self._readULong())]

    def _writeSynaptic(self):
        self._writeULong(len(self.synaptic))
        for n, v in self.synaptic.items():
            self._writeStringS(n)
            self._writeUByte(v)

    def _readSynaptic(self):
        self.synaptic = {self._readStringS(): self._readUByte() for _ in range(self._readULong())}
