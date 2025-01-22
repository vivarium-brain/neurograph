<div align="center"><h1>Neurograph</h1><p>Brain connectome structure saving format</p></div>
[![badge](https://img.shields.io/badge/powered%20by-worm%20brains-0077ff?style=for-the-badge&logo=python&logoColor=%230077ff)](https://github.com/vivarium-brain/vivarium/blob/main/neurographs/worm.ng)

---

Neurograph, also unformally named a "brainscan", is a data format containing information used to reconstruct brain connectome. \
Each neurograph should contain at least a `name` header and a `synaptic` section, and may contain `index` section.

---
# Headers and Sections
## Headers
Headers are small data packets at the start of neurograph file used to give small amounts of data about the neurograph. \
Headers are not CRC-verified, have a maximum size of 255B and have a limited count of 255 headers per neurograph. \
Example of a header usage would be neurograph name, author, or creation/scanning date.
## Sections
Sections are data packets in the body of neurograph file used to store actual data. \
Sections are CRC-verified, have a maximum size of 4GiB and have unlimited count per neurograph. \
Example of a section usage would be connectome synaptic data or ID-to-name index table.
