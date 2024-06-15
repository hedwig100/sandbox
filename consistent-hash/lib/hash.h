#ifndef _HASH_H
#define _HASH_H

#include <string>

namespace hash {

const int kHashSize = 100;

int hash(std::string str) {
    int hash_value = 0;
    for (const char &c : str) {
        hash_value = (kHashSize * hash_value + (c - '0')) % kHashSize;
    }
    return hash_value;
}

} // namespace hash

#endif // _HASH_H