#include "consistent_hash.h"
#include "hash.h"

#include <gtest/gtest.h>

using namespace ::hash;

TEST(ConsistentHashTest, CorrectlyComputesHashValue0) {
    const ConsistentHash consistent_hash;
    const std::string input  = "123";
    const std::string result = consistent_hash.hash(input);
    EXPECT_EQ(result, "parent");
}