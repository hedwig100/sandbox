enable_testing()
include(GoogleTest)

## add_test
add_executable(add_test
    add_test.cc
)
target_link_libraries(add_test
    GTest::gtest_main
)
gtest_discover_tests(add_test)