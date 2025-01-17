from .readerwriter import ReaderWriter
from .neurograph_v1 import Neurograph as Neurograph_v1

VERSIONS = {
    1: Neurograph_v1
}
VERSION_LATEST = 1

def openng(path, mode='r', flat=True, version=VERSION_LATEST):
    if mode == 'r':
        handle = ReaderWriter.fromFile(path, mode)
        assert handle.ReadData(4) == b"NRGP", "Invalid starting bytes"
        version = handle.ReadU16()
        flat = handle.ReadBool()
        if not VERSIONS.get(version):
            raise ValueError(f"Unknown neurograph version: {version} ({version:02x})")
        return VERSIONS[version](path, mode, flat, handle)
    if mode == 'w':
        handle = ReaderWriter.fromFile(path, mode)
        handle.WriteData(b"NRGP")
        handle.WriteU16(version)
        handle.WriteBool(flat)
        return VERSIONS[version](path, mode, flat, handle)


if __name__ == "__main__":
    neurograph = openng("test.ng1", 'w', True)
    neurograph.headers["name"] = ["DUMMY"]
    neurograph.sections["index"] = [[
        "0", "1", "2"
    ]]
    neurograph.sections["synaptic"] = [{
        0: {1: 10},
        1: {2: 10},
        2: {0: 10},
    }]
    neurograph.close()

    neurograph = openng("test.ng1", 'r')
    print(neurograph.headers)
    print(neurograph.sections)
    neurograph.close()