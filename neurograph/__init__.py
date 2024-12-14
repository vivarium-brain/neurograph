from readerwriter import ReaderWriter
from neurograph_v1 import Neurograph as Neurograph_v1

VERSIONS = {
    1: Neurograph_v1
}
VERSION_LATEST = 1

def openng(path, mode='r', version=VERSION_LATEST):
    if mode == 'r':
        handle = ReaderWriter(path, mode)
        assert handle.ReadData(4) == b"NRGP", "Invalid starting bytes"
        version = handle.ReadUShort()
        if not VERSIONS.get(version):
            raise ValueError(f"Unknown neurograph version: {version} ({version:02x})")
        return VERSIONS[version](path, mode, handle)
    if mode == 'w':
        handle = ReaderWriter(path, mode)
        handle.WriteData(b"NRGP")
        handle.WriteUShort(version)
        return VERSIONS[version](path, mode, handle)


if __name__ == "__main__":
    neurograph = openng("test.ng1", 'w')
    neurograph.headers["name"] = ["hello world"]
    neurograph.close()

    neurograph = openng("test.ng1", 'r')
    print(neurograph.headers)
    neurograph.close()