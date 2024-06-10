#include "add.h"

#include <gtest/gtest.h>

using namespace arithmetic;

TEST(AddTest, Add) {
    EXPECT_EQ(3, add(1, 2));
    EXPECT_EQ(5, add(2, 3));
    EXPECT_EQ(7, add(3, 4));
}