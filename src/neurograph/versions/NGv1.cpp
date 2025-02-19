#include <neurograph/Neurograph.h>

namespace ng {
    void Neurograph::readV1(rws::RWStream<std::istream>& stream) {
        // headers
        this->name = stream.readStringNT();
        this->author = stream.readStringNT();

        // body

        // activation threshold
        this->threshold = stream.readU32();

        // neuron count
        this->neurons = stream.readU64();
        // synmatrix
        this->synmatrix = new ng_weight[this->neurons * this->neurons];
        for (int i = 0; i < this->neurons * this->neurons; i++) {
            this->synmatrix[i] = stream.readI16();
        }
        // synindex
        this->synindex = new std::string[this->neurons];
        for (int i = 0; i < this->neurons; i++) {
            this->synindex[i] = stream.readStringNT();
        }
        // init state
        if (!this->flat) {
            this->initstate = new ng_activation[this->neurons];
            for (int i = 0; i < this->neurons; i++) {
                this->initstate[i] = stream.readI32();
            }  
        }
        // muscle groups
        uint groups_count = stream.readU16();
        for (int i = 0; i < groups_count; i++) {
            std::string group = stream.readStringNT();
            uint count = stream.readU32();
            uint* group_neurons = new uint[count];
            for (int j = 0; j < count; j++) {
                group_neurons[j] = stream.readU32();
            }
            this->setMuscleGroup(group, count, group_neurons);
        }
    }

    void Neurograph::writeV1(rws::RWStream<std::ostream>& stream) {
        // headers
        stream.writeStringNT(this->name);
        stream.writeStringNT(this->author);

        // body

        // activation threshold
        stream.writeU32(this->threshold);

        // neuron count
        stream.writeU64(this->neurons);
        // synmatrix
        for (int i = 0; i < this->neurons * this->neurons; i++) {
            stream.writeI16(this->synmatrix[i]);
        }
        // synindex
        for (int i = 0; i < this->neurons; i++) {
            stream.writeStringNT(this->synindex[i]);
        }
        // init state
        if (!this->flat) {
            for (int i = 0; i < this->neurons; i++) {
                stream.writeI32(this->initstate[i]);
            }  
        }
        // muscle groups
        stream.writeU16(this->getMuscleGroupsCount());
        std::string* groups = this->getMuscleGroups();
        for (int i = 0; i < this->getMuscleGroupsCount(); i++) {
            std::string group = groups[i];
            stream.writeStringNT(group);
            uint count = this->getMuscleGroupCount(group);
            stream.writeU32(count);
            uint* group_neurons = this->getMuscleGroup(group);
            for (int j = 0; j < count; j++) {
                stream.writeU32(group_neurons[j]);
            }
        }
        // getMuscleGroups (unfortunately) returns a memory pointer that we need to
        // manually deallocate.
        // TODO: fix!!!
        delete[] groups;
    }
}