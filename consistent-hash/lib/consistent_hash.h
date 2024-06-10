#ifndef _CONSISTENT_HASH_H
#define _CONSISTENT_HASH_H

#include "hash.h"
#include <memory>

namespace hash {

class Node {
  public:
    Node(int id): id(id) {
    }

  private:
    int id;
    std::unique_ptr<Node> next;
};

}


#endif // _CONSISTENT_HASH_H 