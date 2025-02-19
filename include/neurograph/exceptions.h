#ifndef NG_EXCEPTIONS_H
#define NG_EXCEPTIONS_H

#include <exception>
namespace ng {
    class FileOpeningError : public std::exception
        { public: const char* what() { return "Failed to open file"; } };
    class InvalidSignature : public std::exception
        { public: const char* what() { return "File has invalid signature"; } };
    class NotInWritingMode : public std::exception
        { public: const char* what() { return "Not open in writing mode"; } };
    class IsInWritingMode : public std::exception
        { public: const char* what() { return "Open in writing mode"; } };
    class VersionNotSupported : public std::exception
        { public: const char* what() { return "Version not supported"; } };
}

#endif