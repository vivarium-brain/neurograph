#include <neurograph/Neurograph.h>
#include <neurograph/exceptions.h>

#include <RWStream.h>

#include <fstream>
#include <iostream>

namespace ng {
    Neurograph::Neurograph(std::string filepath, std::ios_base::openmode openmode) {
        this->filepath = filepath;
        this->writemode = openmode == std::ios::out;

        try{
            this->read();
        } catch(const std::exception& e) {
            if (this->writemode) return;
            throw e;
        }
    }
    Neurograph::~Neurograph() {
        if (this->writemode)
            this->write();
    }

    void Neurograph::read() {
        std::ifstream ngfile (this->filepath, std::ios::binary);
        if (!ngfile)
            throw ng::FileOpeningError();

        rws::RWStream stream = rws::RWStream<std::istream>(ngfile, std::ios::in);

        char sig[4];
        ngfile.read(sig, 4);

        bool invalidsig = sig[0] != 'N' ||
                          sig[1] != 'R' ||
                          sig[2] != 'G' ||
                          sig[3] != 'P';

        if (invalidsig) {
            ngfile.close();
            throw ng::InvalidSignature();
        }

        this->version = stream.readI16();
        this->flat = stream.readBool();

        this->readBody(stream);

        ngfile.close();
    }
    void Neurograph::write() {
        std::ofstream ngfile (this->filepath, std::ios::binary);
        if (!ngfile)
            throw ng::FileOpeningError();

        rws::RWStream stream = rws::RWStream<std::ostream>(ngfile, std::ios::out);
        ngfile.write("NRGP", 4);
        stream.writeI16(this->version);
        stream.writeBool(this->flat);
        this->writeBody(stream);
        ngfile.flush();
        ngfile.close();
    }

    void Neurograph::readBody(rws::RWStream<std::istream>& stream) {
        switch (this->version) {
            case 1:
                this->readV1(stream);
                break;
            
            default:
                throw ng::VersionNotSupported();
        }
    }
    void Neurograph::writeBody(rws::RWStream<std::ostream>& stream) {
        switch (this->version) {
            case 1:
                this->writeV1(stream);
                break;
            
            default:
                throw ng::VersionNotSupported();
        }
    }

    bool       Neurograph::isFlat()     {return this->flat;}
    ng_version Neurograph::getVersion() {return this->version;}
    void       Neurograph::setVersion(ng_version ver) {
        if(!this->writemode)
            throw ng::NotInWritingMode();
        this->version = ver;
    }

    void        Neurograph::setName(std::string name)     {this->name = name;}
    std::string Neurograph::getName()                     {return this->name;}
    void        Neurograph::setAuthor(std::string author) {this->author = author;}
    std::string Neurograph::getAuthor()                   {return this->author;}

    void Neurograph::setNeuriteCount(uint neurons) {
        this->neurons = neurons;
        this->synmatrix = new ng_weight[this->neurons * this->neurons];
    }
    uint Neurograph::getNeuriteCount() {return this->neurons;}

    void       Neurograph::setSynapticMatrix(ng_weight synmatrix[]) {this->synmatrix = synmatrix;}
    ng_weight* Neurograph::getSynapticMatrix() {return this->synmatrix;}
    void         Neurograph::setSynapticIndex(std::string synindex[]) {this->synindex = synindex;}
    std::string* Neurograph::getSynapticIndex() {return this->synindex;}

    void Neurograph::setInitialState(ng_activation initstate[]) {this->flat = false; this->initstate = initstate;}
    void Neurograph::unsetInitialState() {this->flat = true;}
    ng_activation* Neurograph::getInitialState() {return this->initstate;}

    void Neurograph::setActivationThreshold(ng_uactivation threshold) {this->threshold = threshold;}
    ng_uactivation Neurograph::getActivationThreshold() {return this->threshold;}

    void Neurograph::setMuscleGroup(std::string group, uint count, uint neurons[]) {
        (this->muscles)[group] = neurons;
        (this->musclessizes)[group] = count;
    }
    uint* Neurograph::getMuscleGroup(std::string group) {
        return (this->muscles)[group];
    }
    uint Neurograph::getMuscleGroupCount(std::string group) {
        return (this->musclessizes)[group];
    }
    std::string* Neurograph::getMuscleGroups() {
        std::string* groups = new std::string[this->getMuscleGroupsCount()];
        int i = 0;
        for (const std::pair<const std::string, uint*>&p : (this->muscles)) {
            groups[i] = p.first;
            i++;
        }
        return groups;
    }
    uint Neurograph::getMuscleGroupsCount() {
        return (this->muscles).size();
    }
}

