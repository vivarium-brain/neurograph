<div align="center"><h1>Neurograph</h1><p>Neurological data container format</p></div>

---
Neurograph, also known as a brain-scan, is a data format containing information used to reconstruct brain connectome. \
Each file contains a synaptic table used for storing starting neuron state and verifying dendrite table, and a dendrite
table used for storing connections between neurons in synaptic table.
---
# Structures
## Synaptic Table
Synaptic table contains starting neurons state and verifies integrity of dendrite table by checking if neurons specified
in dendrite inputs/outputs are correctly specified.

---
# Versions
## Version 1
- Created 23rd september 2024.
- Deprecated in favor of Version 2.

First neurograph container version. Highly space-inefficient. Kept packaged for legacy files support.
```
Version = 0x01
Structure {
    Header    (required)
    Synaptic  (required)
    Dendrites (required)
}

Synaptic {
    Count: ulong (4b uint)
    Neurite (xCount) {
        NameLength: ubyte (1b uint)
        NameString: bytes (xNameLength)
        Amount: ubyte (1b uint)
    }
}

Dendrites {
    Count: ulong (4b uint)
    Dendrite (xCount) {
        OwnerNameLength: ubyte (1b uint)
        OwnerNameSring: bytes (xOwnerNameLength)
        ConnectionsCount: ulong (4b uint)
        DendriteConnection (xConnectionsCount) {
            ConnectionNameLength: ubyte (1b uint)
            ConnectionNameSring: bytes (xConnectionNameLength)
            ConnectionAmount: ubyte (1b uint)
            ConnectionMode: ubyte (1b uint)
        }
    }
}
```

## Version 2
- Created 16th november 2024.
- Default writer version.

As of 16th november 2024 latest neurograph container, should be used for all future neurographs.
```
Version = 0x02
Structure {
    Header          (required)
    LZMA_Compressed (required) {
        IndexTable  (required)
        Synaptic    (required)
        Dendrites   (required)
    }
}

IndexTable {
    Count: ulong (4b uint)
    Names (xCount) {
        NameLength: ubyte (1b uint)
        NameString: bytes (xNameLength)
    }
}

Synaptic {
    Count: ulong (4b uint)
    Neurite (xCount) {
        Index: ulong (4b uint)
        Amount: ubyte (1b uint)
    }
}

Dendrites {
    Count: ulong (4b uint)
    Dendrite (xCount) {
        OwnerIndex: ulong (4b uint)
        ConnectionsCount: ulong (4b uint)
        DendriteConnection (xConnectionsCount) {
            ConnectionIndex: ulong (4b uint)
            ConnectionAmount: ubyte (1b uint)
            ConnectionMode: ubyte (1b uint)
        }
    }
}
```