enable_testing()
include(GoogleTest)

## consistent_hash_test
add_executable(consistent_hash_test
    consistent_hash_test.cc
)
target_link_libraries(consistent_hash_test
    GTest::gtest_main
)
gtest_discover_tests(consistent_hash_test)