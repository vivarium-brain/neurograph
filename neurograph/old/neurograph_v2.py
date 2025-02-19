import io
import lzma


class GoogerNeurographV2:
    def __init__(self, path, mode, wrapper):
        self.path = path
        self.mode = mode
        self.wrapper = wrapper
        self.stream = None
        if self.mode == 'r':
            self._read()
        else:
            self.synaptic = {}
            self.dendrites = []
            self.index_table = []

    def _write(self):
        self.stream = io.BytesIO()
        self._writeIndexTable()
        self._writeSynaptic()
        self._writeDendrites()
        self.stream.seek(0)
        compressed = lzma.compress(self.stream.read(), preset=1)
        self.stream.close()
        self.stream = open(self.path, "wb")
        self.wrapper.writeHeader(self.stream)
        self.stream.write(compressed)
        self.stream.flush()
        self.stream.close()
        self.stream = None

    def _read(self):
        self.stream = open(self.path, "rb")
        self.wrapper.readHeader(self.stream)
        compressed = self.stream.read()
        self.stream.close()
        self.stream = io.BytesIO(lzma.decompress(compressed))
        self._readIndexTable()
        self._readSynaptic()
        self._readDendrites()
        self.stream.close()
        self.stream = None

    def flush(self):
        if self.mode != 'w':
            return
        self._write()

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
        # neuron is disembodied (not in synaptic table)
        if not dendrite["name"] in self.index_table:
            return
        self._writeULong(self.index_table.index(dendrite["name"]))
        self._writeULong(len(dendrite["activations"]))
        for activation in dendrite["activations"]:
            # neuron is disembodied (not in synaptic table)
            if not activation["excited"] in self.index_table:
                continue
            self._writeULong(self.index_table.index(activation["excited"]))
            self._writeUByte(activation["amount"])
            self._writeUByte(activation["mode"])

    def _readDendrite(self):
        return {
            "name": self.index_table[self._readULong()],
            "activations": [{
                "excited": self.index_table[self._readULong()],
                "amount": self._readUByte(),
                "mode": self._readUByte()
            } for _ in range(self._readULong())]
        }

    def _writeIndexTable(self):
        self.index_table = []
        self._writeULong(len(self.synaptic))
        for n, v in self.synaptic.items():
            self._writeStringS(n)
            self.index_table.append(n)

    def _readIndexTable(self):
        self.index_table = [self._readStringS() for _ in range(self._readULong())]

    def _writeDendrites(self):
        self._writeULong(len(self.dendrites))
        for dendrite in self.dendrites:
            self._writeDendrite(dendrite)

    def _readDendrites(self):
        self.dendrites = [self._readDendrite() for _ in range(self._readULong())]

    def _writeSynaptic(self):
        self._writeULong(len(self.synaptic))
        for n, v in self.synaptic.items():
            self._writeULong(self.index_table.index(n))
            self._writeUByte(v)

    def _readSynaptic(self):
        self.synaptic = {self.index_table[self._readULong()]: self._readUByte() for _ in range(self._readULong())}
