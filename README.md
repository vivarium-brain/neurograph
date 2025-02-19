<div align="center"><h1>Neurograph</h1><p>Brain connectome structure saving format</p></div>

[![powered by worm brains](https://img.shields.io/badge/powered%20by-worm%20brains-0077ff?style=for-the-badge&logo=python&logoColor=%230077ff)](https://github.com/vivarium-brain/brainscans/blob/main/caenorhabditis_elegans)
[![built with existential horror](https://img.shields.io/badge/built%20with-existential%20horror-ff7700?style=for-the-badge)](https://qntm.org/mmacevedo)

---
Neurograph, also unformally named a "brainscan", is a data format containing information used to reconstruct brain connectome. \
Each neurograph should contain at least a `name` header and a `synaptic` section, and may contain `index` section.

---
# Headers and Sections
## Headers
Headers are small data packets at the start of neurograph file used to give small amounts of data about the neurograph. \
Headers are not CRC-verified and have a limited count of 255 headers per neurograph. \
Example of a header usage would be neurograph name, author, or creation/scanning date.
## Sections
Sections are data packets in the body of neurograph file used to store actual data. \
Sections are CRC-verified, have a maximum size of 4GiB and have unlimited count per neurograph. \
Example of a section usage would be connectome synaptic data or ID-to-name index table.

---
# Versions

## Base
Base for all modern neurograph formats. Contains a few starting structures that never change and are used to identify is file is a valid neurograph.
```
StringLPS {
    ubyte length;
    char[length] string;
}

Header {
    ubyte hid;   // 1 byte: header id
    char[] data; // header data...
}

Section {
    ubyte sid;       // 1 byte: section id
    ulong crc;       // 8 bytes: section crc
    uint size;       // 4 bytes: section size
    char[size] data; // section data...
}

HeaderName extends Header {
    StringLPS name;
}

NeurographBase {
    uint Signature = "NGRP";      // 4 bytes: always the same, used to identify neurograph
    ushort version;               // 2 bytes: neurograph version
    bool flags;                   // 1 byte: neurograph flags - flat|empty|empty|empty|empty|empty|empty|empty
    ubyte header_count;           // 1 byte: header count
    Header[header_count] headers; // headers...
    Section[] sections;           // sections...
}
```

## Version 1
Created 17th january 2025.

Rewritten Neurograph format to allow for partial backwards compability, easier introduction of new features or sections, and CRC-validated structures.
```
SEC_Synapse {
    ulong neurite_id;
    int weight;
}

SEC_Neurite {
    ulong neurite_id;
    ulong synapse_count;
    SEC_Synapse[synapse_count] synapses;
}

SynapticSection extends Section {
    ubyte sid = 0;
    ...
    ulong neurite_count;
    SEC_Neurite[neurite_count] neurites;
}

IndexSection extends Section {
    ulong neurite_count;
    StringLPS[neurite_count] name;
}

NeurographV1 extends NeurographBase {
    ushort version = 1;
    ...
    Header[header_count] headers;
    SynapticSection synaptic;
    IndexSection index;
}

```

---
# Legacy Versions
These are no longer supported and any information given above are not applicable for these.
Available through importing `Neurograph` from `neurograph.old`

## Version 1
- Created 23rd september 2024.

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
        OwnerNameString: bytes (xOwnerNameLength)
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

Higher space efficiency due to storing neurons with an index table and LZMA-compressed buffer.
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
