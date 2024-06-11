#ifndef _HASH_H
#define _HASH_H

#include <string>

namespace hash {

const int kHashSize = 100;

int hash(std::string str) { return std::stoi(str) % kHashSize; }

} // namespace hash

#endif // _HASH_H