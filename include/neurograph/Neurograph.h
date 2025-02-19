#ifndef NG_NEUROGRAPH_H
#define NG_NEUROGRAPH_H

#include <RWStream.h>

#include <string>
#include <fstream>
#include <unordered_map>
#include <stdint.h>

#define ng_weight int16_t
#define ng_activation int32_t
#define ng_uactivation uint32_t
#define ng_version uint16_t
#define ng_version_latest 1

namespace ng {
    class Neurograph {
        public:
            Neurograph(std::string filepath, std::ios_base::openmode openmode);
            ~Neurograph();
        private:
            // file data
            std::string filepath; // neurograph filename
            bool writemode; // was opened in writing mode
            ng_version version = ng_version_latest; // neurograph version
            // neurograph data
            bool flat;             // was saved as flat neurograph (no initial state info)
            ng_activation* initstate; // initial state
            ng_uactivation threshold; // neurite activation threshold
            std::string name   = ""; // neurograph name
            std::string author = ""; // neurograph author or credit info
            uint neurons;          // neuron count
            ng_weight* synmatrix;  // n*neurons+m = weight for neuron n to m
            std::string* synindex; // maps id -> name
            std::unordered_map<std::string, uint*> muscles = {}; // maps group -> neurons
            std::unordered_map<std::string, uint> musclessizes = {}; // maps group -> count

            // version reading functions
            void readBody(rws::RWStream<std::istream>& stream);
            void readV1(rws::RWStream<std::istream>& stream);

            // version writing functions
            void writeBody(rws::RWStream<std::ostream>& stream);
            void writeV1(rws::RWStream<std::ostream>& stream);

        public:
            bool         isFlat();
            ng_version   getVersion();
            void         setVersion(ng_version ver);

            void         setName(std::string name);
            std::string  getName();
            void         setAuthor(std::string author);
            std::string  getAuthor();

            void           setNeuriteCount(uint neurons);
            uint           getNeuriteCount();
            void           setSynapticMatrix(ng_weight synmatrix[]);
            ng_weight*     getSynapticMatrix();
            void           setSynapticIndex(std::string synindex[]);
            std::string*   getSynapticIndex();
            void           setInitialState(ng_activation initstate[]);
            void           unsetInitialState();
            ng_activation* getInitialState();
            void           setActivationThreshold(ng_uactivation threshold);
            ng_uactivation getActivationThreshold();

            void           setMuscleGroup(std::string group, uint count, uint neurons[]);
            uint*          getMuscleGroup(std::string group);
            uint           getMuscleGroupCount(std::string group);
            std::string*   getMuscleGroups();
            uint           getMuscleGroupsCount();

            void write();
            void read();
    };
}

#endif