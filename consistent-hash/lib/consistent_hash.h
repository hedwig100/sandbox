#ifndef _CONSISTENT_HASH_H
#define _CONSISTENT_HASH_H

#include "hash.h"
#include <memory>

namespace hash {

/// A node in the consistent hash ring.
/// The `id` corresponds to the hash value.
/// The `name` is the name of the node.
class Node {
  public:
    Node(int id, const std::string &name)
        : id_(id), name_(name), next_(nullptr) {}

    int id() const { return id_; }
    const std::string &name() const { return name_; }
    const Node *next() const { return next_; }

  private:
    int id_;
    std::string name_;
    Node *next_;
};

class ConsistentHash {
  public:
    ConsistentHash() { head_ = new Node(0, "parent"); }

    /// Computes the hash of the input string
    /// as a consistent hash.
    const std::string &hash(const std::string &str) const {
        int input_hash = hash::hash(str);
        for (const Node *node = head_; node; node = node->next()) {
            if (input_hash <= node->id()) { return node->name(); }
        }
        return head_->name();
    }

    /// Adds a node to the consistent hash ring.
    void add_node(int id, const std ::string &name) {
        Node *new_node = new Node(id, name);
        for (const Node *node = head_; node; node = node->next()) {
            if (id > node->id()) { return; } // TODO: Implement this.
        }
    }

  private:
    Node *head_;
};

} // namespace hash

#endif // _CONSISTENT_HASH_H