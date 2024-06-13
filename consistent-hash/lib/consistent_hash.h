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

    Node *next_mut() { return next_; }

    void set_next(Node *node) { next_ = node; }

  private:
    int id_;
    std::string name_;
    Node *next_;
};

class ConsistentHash {
  public:
    ConsistentHash() { head_ = new Node(0, "parent"); }
    ConsistentHash(const std::string &default_node_name) {
        head_ = new Node(0, default_node_name);
    }

    /// Computes the hash of the input string
    /// as a consistent hash.
    /// The `input_id` should be hashed key via hash::hash().
    const std::string &hash(const int input_id) const {
        for (const Node *node = head_; node; node = node->next()) {
            if (input_id <= node->id()) { return node->name(); }
        }
        return head_->name();
    }

    /// Adds a node to the consistent hash ring.
    /// The requirement 0 <= id < hash::kHashSize should be satisfied.
    void add_node(int id, const std::string &name) {
        Node *new_node  = new Node(id, name);
        Node *prev_node = nullptr;
        for (Node *node = head_; node; node = node->next_mut()) {
            if (id < node->id()) {
                new_node->set_next(node);
                prev_node->set_next(new_node);
                return;
            }
            prev_node = node;
        }
        prev_node->set_next(new_node);
        return;
    }

    /// Removes nodes whose name is `name`.
    void remove_node_by_name(const std::string &name) {
        Node *prev_node = nullptr;
        for (Node *node = head_; node; node = node->next_mut()) {
            if (node->name() == name) {
                prev_node->set_next(node->next_mut());
                delete node;
                node = prev_node;
            } else {
                prev_node = node;
            }
        }
    }

  private:
    Node *head_;
};

} // namespace hash

#endif // _CONSISTENT_HASH_H