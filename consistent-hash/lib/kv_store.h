#ifndef _KV_STORE_H
#define _KV_STORE_H

#include <map>
#include <random>
#include <string>

#include "consistent_hash.h"
#include "hash.h"

namespace kvs {

class DistributedKeyValueStore {
  public:
    DistributedKeyValueStore(const std::string &default_address) {
        consistent_hash =
            hash::ConsistentHash(/*default_node_name=*/default_address);
    }

    /// Inserts the (`key`, `value`) pair when there is no item
    /// with key of `key`. Otherwise, it updates the `key` with the
    /// value of `value`.
    void insert_or_update(const std::string &key, int value) {
        address_key_values[consistent_hashing(key)][key] = value;
    }

    /// Returns the address the item exists and
    /// the value of item whose key is `key`.
    std::pair<std::string, int> select(const std::string &key) {
        const std::string address = consistent_hashing(key);
        return std::make_pair(address, address_key_values[address][key]);
    }

    /// Removes the item of key `key`.
    void remove(const std::string &key) {
        address_key_values[consistent_hashing(key)].erase(key);
    }

    /// Adds the node whose address is `address`.
    void add_node(const std::string &address) {
        int node_id = random(hash::kHashSize);
        consistent_hash.add_node(node_id, address);

        // (TODO): Move items to the address
        address_key_values[]
    }

    /// Removes the node whose address is `address`.
    void remove_node(const std::string &address) {}

  private:
    const std::string &consistent_hashing(const std::string &input) {
        return consistent_hash.hash(hash::hash(input));
    }

    int random(const int upper_bound) {
        static std::mt19937 mt32(0);
        return mt32() % upper_bound;
    }

  private:
    std::map<std::string, std::map<std::string, int>> address_key_values;
    hash::ConsistentHash consistent_hash;
};

} // namespace kvs

#endif
