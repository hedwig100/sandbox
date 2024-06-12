#include "consistent_hash.h"
#include "hash.h"

#include <gtest/gtest.h>

using namespace ::hash;

TEST(ConsistentHashTest, CorrectlyComputesHashValue0) {
    const ConsistentHash consistent_hash;
    const std::string result = consistent_hash.hash(8);
    EXPECT_EQ(result, "parent");
}

TEST(ConsistentHashTest, AddNodeCorrectly) {
    ConsistentHash consistent_hash;
    consistent_hash.add_node(4, "192.0.0.1");
    consistent_hash.add_node(8, "192.0.0.2");
    consistent_hash.add_node(11, "192.0.0.3");

    EXPECT_EQ(consistent_hash.hash(0), "parent");
    EXPECT_EQ(consistent_hash.hash(2), "192.0.0.1");
    EXPECT_EQ(consistent_hash.hash(4), "192.0.0.1");
    EXPECT_EQ(consistent_hash.hash(6), "192.0.0.2");
    EXPECT_EQ(consistent_hash.hash(8), "192.0.0.2");
    EXPECT_EQ(consistent_hash.hash(10), "192.0.0.3");
    EXPECT_EQ(consistent_hash.hash(11), "192.0.0.3");
    EXPECT_EQ(consistent_hash.hash(34), "parent");
}

TEST(ConsistentHashTest, RemoveNodeCorrectly) {
    ConsistentHash consistent_hash;
    consistent_hash.add_node(4, "192.0.0.1");
    consistent_hash.add_node(8, "192.0.0.2");
    consistent_hash.add_node(11, "192.0.0.3");
    consistent_hash.add_node(19, "192.0.0.2");
    consistent_hash.remove_node_by_name("192.0.0.2");

    EXPECT_EQ(consistent_hash.hash(0), "parent");
    EXPECT_EQ(consistent_hash.hash(2), "192.0.0.1");
    EXPECT_EQ(consistent_hash.hash(4), "192.0.0.1");
    EXPECT_EQ(consistent_hash.hash(6), "192.0.0.3");
    EXPECT_EQ(consistent_hash.hash(8), "192.0.0.3");
    EXPECT_EQ(consistent_hash.hash(10), "192.0.0.3");
    EXPECT_EQ(consistent_hash.hash(11), "192.0.0.3");
    EXPECT_EQ(consistent_hash.hash(15), "parent");
    EXPECT_EQ(consistent_hash.hash(19), "parent");
    EXPECT_EQ(consistent_hash.hash(34), "parent");
}