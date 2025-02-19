#ifndef NG_READERWRITER_H
#define NG_READERWRITER_H

#include <neurograph/exceptions.h>

#include <iostream>
#include <stdint.h>

namespace rws {
    template <typename T> class RWStream {
        public:
            RWStream() : handle(T()) {
                this->writemode = true;
            }
            RWStream(T& stream, std::ios_base::openmode mode) : handle(stream) {
                this->writemode = mode == std::ios::out;
            }
        private:
            bool writemode;
            T& handle;

        public:
            bool isWriting();

               uint8_t  readU8      (); void writeU8      (   uint8_t  var);
               uint16_t readU16     (); void writeU16     (   uint16_t var);
               uint32_t readU32     (); void writeU32     (   uint32_t var);
               uint64_t readU64     (); void writeU64     (   uint64_t var);
                int8_t  readI8      (); void writeI8      (    int8_t  var);
                int16_t readI16     (); void writeI16     (    int16_t var);
                int32_t readI32     (); void writeI32     (    int32_t var);
                int64_t readI64     (); void writeI64     (    int64_t var);

                  float readFloat   (); void writeFloat   (      float var);
                 double readDouble  (); void writeDouble  (     double var);

                   bool readBool    (); void writeBool    (       bool var);
                   
            std::string readStringNT(); void writeStringNT(std::string var);
            std::string readStringLP(); void writeStringLP(std::string var);
    };

    template <typename T> bool RWStream<T>::isWriting() { return this->writemode; }
    template <typename T> uint8_t  RWStream<T>::readU8 () { 
        if (this->isWriting()) throw ng::IsInWritingMode();
        uint8_t  num; this->handle.read((char*)&num, 1); return num; 
    }
    template <typename T> uint16_t RWStream<T>::readU16()  { 
        if (this->isWriting()) throw ng::IsInWritingMode();
        uint16_t num; this->handle.read((char*)&num, 2); return num; 
    }
    template <typename T> uint32_t RWStream<T>::readU32()  { 
        if (this->isWriting()) throw ng::IsInWritingMode();
        uint32_t num; this->handle.read((char*)&num, 4); return num; 
    }
    template <typename T> uint64_t RWStream<T>::readU64()  { 
        if (this->isWriting()) throw ng::IsInWritingMode();
        uint64_t num; this->handle.read((char*)&num, 8); return num; 
    }

    template <typename T> void RWStream<T>::writeU8 (uint8_t  var)  { 
        if (!this->isWriting()) throw ng::NotInWritingMode();
        this->handle.write((char*)&var, 1);
    }
    template <typename T> void RWStream<T>::writeU16(uint16_t var)  { 
        if (!this->isWriting()) throw ng::NotInWritingMode();
        this->handle.write((char*)&var, 2);
    }
    template <typename T> void RWStream<T>::writeU32(uint32_t var)  { 
        if (!this->isWriting()) throw ng::NotInWritingMode();
        this->handle.write((char*)&var, 4);
    }
    template <typename T> void RWStream<T>::writeU64(uint64_t var)  { 
        if (!this->isWriting()) throw ng::NotInWritingMode();
        this->handle.write((char*)&var, 8);
    }

    template <typename T> int8_t  RWStream<T>::readI8 () { 
        if (this->isWriting()) throw ng::IsInWritingMode();
        int8_t  num; this->handle.read((char*)&num, 1); return num; 
    }
    template <typename T> int16_t RWStream<T>::readI16()  { 
        if (this->isWriting()) throw ng::IsInWritingMode();
        int16_t num; this->handle.read((char*)&num, 2); return num; 
    }
    template <typename T> int32_t RWStream<T>::readI32()  { 
        if (this->isWriting()) throw ng::IsInWritingMode();
        int32_t num; this->handle.read((char*)&num, 4); return num; 
    }
    template <typename T> int64_t RWStream<T>::readI64()  { 
        if (this->isWriting()) throw ng::IsInWritingMode();
        int64_t num; this->handle.read((char*)&num, 8); return num; 
    }

    template <typename T> void RWStream<T>::writeI8 (int8_t  var)  { 
        if (!this->isWriting()) throw ng::NotInWritingMode();
        this->handle.write((char*)&var, 1);
    }
    template <typename T> void RWStream<T>::writeI16(int16_t var)  { 
        if (!this->isWriting()) throw ng::NotInWritingMode();
        this->handle.write((char*)&var, 2);
    }
    template <typename T> void RWStream<T>::writeI32(int32_t var)  { 
        if (!this->isWriting()) throw ng::NotInWritingMode();
        this->handle.write((char*)&var, 4);
    }
    template <typename T> void RWStream<T>::writeI64(int64_t var)  { 
        if (!this->isWriting()) throw ng::NotInWritingMode();
        this->handle.write((char*)&var, 8);
    }

    template <typename T> bool RWStream<T>::readBool() {
        return this->readU8() == 255;
    }
    template <typename T> void RWStream<T>::writeBool(bool var) {
        this->writeU8(var ? 255 : 0);
    }

    template <typename T> float RWStream<T>::readFloat() { 
        if (this->isWriting()) throw ng::IsInWritingMode();
        float num; this->handle.read((char*)&num, 4); return num; 
    }
    template <typename T> void RWStream<T>::writeFloat(float var)  { 
        if (!this->isWriting()) throw ng::NotInWritingMode();
        this->handle.write((char*)&var, 4);
    }
    template <typename T> double RWStream<T>::readDouble() { 
        if (this->isWriting()) throw ng::IsInWritingMode();
        float num; this->handle.read((char*)&num, 8); return num; 
    }
    template <typename T> void RWStream<T>::writeDouble(double var)  { 
        if (!this->isWriting()) throw ng::NotInWritingMode();
        this->handle.write((char*)&var, 8);
    }

    template <typename T> std::string RWStream<T>::readStringNT() {
        std::string str = "";
        char buffer = ' ';
        while (buffer != 0) {
            this->handle.read(&buffer, 1);
            if (buffer == 0) break;
            str.push_back(buffer);
        }
        return str;
    }
    template <typename T> void RWStream<T>::writeStringNT(std::string var) {
        char zero = 0;
        this->handle.write(&var[0], var.size());
        this->handle.write(&zero, 1);
    }
    template <typename T> std::string RWStream<T>::readStringLP() {
        uint16_t length = this->readU16();
        char str[length+1]; str[length] = 0; 
        this->handle.read(str, length);
        return std::string (str);
    }
    template <typename T> void RWStream<T>::writeStringLP(std::string var) {
        this->writeU16(var.length());
        this->handle.write(&var[0], var.length());
    }
}

#endif
