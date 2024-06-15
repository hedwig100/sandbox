#include "consistent_hash.h"
#include "hash.h"
#include "kv_store.h"

#include <gtest/gtest.h>
#include <string>
#include <utility>

using namespace ::hash;
using namespace ::kvs;

TEST(KeyValueStore, JustInsertDeleteItems) {
    DistributedKeyValueStore dkvs(/*defalut_address=*/"127.0.0.1");
    dkvs.insert_or_update("000", 6);
    dkvs.insert_or_update("001", 1);
    dkvs.insert_or_update("002", 2);

    EXPECT_EQ(dkvs.select("000").second, 6);
    EXPECT_EQ(dkvs.select("001").second, 1);
    EXPECT_EQ(dkvs.select("002").second, 2);

    dkvs.remove("001");
    dkvs.insert_or_update("002", 5);

    EXPECT_EQ(dkvs.select("000").second, 6);
    EXPECT_EQ(dkvs.select("001").second, 0);
    EXPECT_EQ(dkvs.select("002").second, 5);
}

TEST(KeyValueStore, AddNodeAfterInsertNode) {
    DistributedKeyValueStore dkvs(/*defalut_address=*/"127.0.0.1");
    dkvs.insert_or_update("00a", 6);
    dkvs.insert_or_update("0a0", 1);
    dkvs.insert_or_update("a00", 2);
    dkvs.insert_or_update("0ab", 3);
    dkvs.insert_or_update("ab0", 4);
    dkvs.insert_or_update("b0a", 5);

    dkvs.add_node("192.0.0.1");

    EXPECT_EQ(dkvs.select("00a").second, 6);
    EXPECT_EQ(dkvs.select("0a0").second, 1);
    EXPECT_EQ(dkvs.select("a00").second, 2);
    EXPECT_EQ(dkvs.select("0ab").second, 3);
    EXPECT_EQ(dkvs.select("ab0").second, 4);
    EXPECT_EQ(dkvs.select("b0a").second, 5);
}

TEST(KeyValueStore, RemoveNodeAfterInsertValues) {
    DistributedKeyValueStore dkvs(/*defalut_address=*/"127.0.0.1");
    dkvs.add_node("192.0.0.1");
    dkvs.add_node("192.0.0.2");
    dkvs.add_node("192.0.0.3");

    dkvs.insert_or_update("00a", 6);
    dkvs.insert_or_update("0a0", 1);
    dkvs.insert_or_update("a00", 2);
    dkvs.insert_or_update("0ab", 3);
    dkvs.insert_or_update("ab0", 4);
    dkvs.insert_or_update("b0a", 5);

    dkvs.remove_node("192.0.0.1");
    dkvs.remove_node("192.0.0.2");

    EXPECT_EQ(dkvs.select("00a").second, 6);
    EXPECT_EQ(dkvs.select("0a0").second, 1);
    EXPECT_EQ(dkvs.select("a00").second, 2);
    EXPECT_EQ(dkvs.select("0ab").second, 3);
    EXPECT_EQ(dkvs.select("ab0").second, 4);
    EXPECT_EQ(dkvs.select("b0a").second, 5);
}