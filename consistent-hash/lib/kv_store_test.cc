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
    dkvs.insert_or_update("fender", 1);
    dkvs.insert_or_update("yamaha", 2);
    dkvs.insert_or_update("gibson", 3);
    dkvs.insert_or_update("tokai", 4);
    dkvs.insert_or_update("epiphone", 5);
    dkvs.insert_or_update("marshal", 6);
    dkvs.insert_or_update("red", 7);
    dkvs.insert_or_update("black", 8);
    dkvs.insert_or_update("green", 9);
    dkvs.insert_or_update("yellow", 10);
    dkvs.insert_or_update("white", 11);
    dkvs.insert_or_update("gold", 12);

    dkvs.add_node("192.0.0.1");
    dkvs.add_node("192.0.0.2");
    dkvs.add_node("192.0.0.3");
    dkvs.add_node("192.0.0.4");

    EXPECT_EQ(dkvs.select("fender").second, 1);
    EXPECT_EQ(dkvs.select("yamaha").second, 2);
    EXPECT_EQ(dkvs.select("gibson").second, 3);
    EXPECT_EQ(dkvs.select("tokai").second, 4);
    EXPECT_EQ(dkvs.select("epiphone").second, 5);
    EXPECT_EQ(dkvs.select("marshal").second, 6);
    EXPECT_EQ(dkvs.select("red").second, 7);
    EXPECT_EQ(dkvs.select("black").second, 8);
    EXPECT_EQ(dkvs.select("green").second, 9);
    EXPECT_EQ(dkvs.select("yellow").second, 10);
    EXPECT_EQ(dkvs.select("white").second, 11);
    EXPECT_EQ(dkvs.select("gold").second, 12);
}

TEST(KeyValueStore, RemoveNodeAfterInsertValues) {
    DistributedKeyValueStore dkvs(/*defalut_address=*/"127.0.0.1");
    dkvs.add_node("192.0.0.1");
    dkvs.add_node("192.0.0.2");
    dkvs.add_node("192.0.0.3");
    dkvs.add_node("192.0.0.4");
    dkvs.add_node("192.0.0.5");
    dkvs.add_node("192.0.0.6");
    dkvs.add_node("192.0.0.7");
    dkvs.add_node("192.0.0.8");
    dkvs.add_node("192.0.0.9");
    dkvs.add_node("192.0.0.10");

    dkvs.insert_or_update("fender", 1);
    dkvs.insert_or_update("yamaha", 2);
    dkvs.insert_or_update("gibson", 3);
    dkvs.insert_or_update("tokai", 4);
    dkvs.insert_or_update("epiphone", 5);
    dkvs.insert_or_update("marshal", 6);
    dkvs.insert_or_update("red", 7);
    dkvs.insert_or_update("black", 8);
    dkvs.insert_or_update("green", 9);
    dkvs.insert_or_update("yellow", 10);
    dkvs.insert_or_update("white", 11);
    dkvs.insert_or_update("gold", 12);

    dkvs.remove_node("192.0.0.1");
    dkvs.remove_node("192.0.0.3");
    dkvs.remove_node("192.0.0.5");
    dkvs.remove_node("192.0.0.7");
    dkvs.remove_node("192.0.0.9");

    EXPECT_EQ(dkvs.select("fender").second, 1);
    EXPECT_EQ(dkvs.select("yamaha").second, 2);
    EXPECT_EQ(dkvs.select("gibson").second, 3);
    EXPECT_EQ(dkvs.select("tokai").second, 4);
    EXPECT_EQ(dkvs.select("epiphone").second, 5);
    EXPECT_EQ(dkvs.select("marshal").second, 6);
    EXPECT_EQ(dkvs.select("red").second, 7);
    EXPECT_EQ(dkvs.select("black").second, 8);
    EXPECT_EQ(dkvs.select("green").second, 9);
    EXPECT_EQ(dkvs.select("yellow").second, 10);
    EXPECT_EQ(dkvs.select("white").second, 11);
    EXPECT_EQ(dkvs.select("gold").second, 12);
}