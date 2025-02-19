#include <neurograph/Neurograph.h>
#include <RWStream.h>

#include <iostream>
#include <fstream>

void test_write() {
    ng::Neurograph neurograph = ng::Neurograph("test.ng", std::ios::out);
    neurograph.setName("DUMMY");
    neurograph.setAuthor("googer_");

    ng_weight synmatrix[] = {
         0, 10,  0, // neuron #1 activates #2
         0,  0, 10, //        #2 activates #3
        10,  0,  0  //    and #3 activates #1
    };
    std::string synindex[] = {
        "T1", "T2", "T3"
    };
    ng_activation initstate[] = {10, 0, 0};
    uint musleft[] = {1};
    uint musright[] = {3};
    neurograph.setNeuriteCount(3);
    neurograph.setSynapticMatrix(synmatrix);
    neurograph.setSynapticIndex(synindex);
    //neurograph.unsetInitialState();
    neurograph.setInitialState(initstate);
    neurograph.setActivationThreshold(10);
    neurograph.setMuscleGroup("left",  1, musleft);
    neurograph.setMuscleGroup("right", 1, musright);

    neurograph.write();
}
void test_read() {
    ng::Neurograph neurograph = ng::Neurograph("test.ng", std::ios::in);
    std::cout << "Name:      " << neurograph.getName() << std::endl;
    std::cout << "Author:    " << neurograph.getAuthor() << std::endl;
    std::cout << "Threshold: " << neurograph.getActivationThreshold() << std::endl;
    std::cout << "Flat:      " << (neurograph.isFlat() ? "yes" : "no") << std::endl;
    uint neurons = neurograph.getNeuriteCount();
    std::cout << "Neurons: " << neurons << std::endl;
    ng_weight* synmatrix = neurograph.getSynapticMatrix();
    std::string* synindex = neurograph.getSynapticIndex();

    std::cout << "Synaptic Matrix: " << std::endl;
    for (int i=0; i < neurons; i++) {
        std::cout << "  Neuron #" << i+1 << " (" << synindex[i] << "): ";
        for (int j=0; j < neurons; j++) {
            std::cout << synmatrix[i * neurons + j] << " ";
        }
        std::cout << std::endl;
    }
    if (!neurograph.isFlat()) {
        std::cout << "Initial State: " << std::endl;
        ng_activation* initstate = neurograph.getInitialState();
        for (int i=0; i < neurons; i++) {
            std::cout << "  Neuron #" << i+1 <<
                         " (" << synindex[i] << "): " <<
                         initstate[i] << std::endl;
        }
    }
    std::cout << "Muscles: " << std::endl;
    std::string* groups = neurograph.getMuscleGroups();
    for (int i = 0; i < neurograph.getMuscleGroupsCount(); i++) {
        std::string group = groups[i];
        std::cout << "  Group #" << i+1 << " (" << group << "):" << std::endl << "    ";
        uint count = neurograph.getMuscleGroupCount(group);
        uint* group_neurons = neurograph.getMuscleGroup(group);
        for (int j = 0; j < count; j++) {
            std::cout << group_neurons[j] << " ";
        }
        std::cout << std::endl;
    }
    // getMuscleGroups (unfortunately) returns a memory pointer that we need to
    // manually deallocate.
    // TODO: fix!!!
    delete[] groups;
}

int main() {
    std::cout << "testing write" << std::endl;
    test_write();
    std::cout << "testing write: OK" << std::endl << "testing read" << std::endl;
    test_read();
    std::cout << "testing read: OK" << std::endl;

    return 0;
}