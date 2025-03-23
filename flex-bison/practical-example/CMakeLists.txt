cmake_minimum_required(VERSION 3.10)
project(SQLParser)

find_package(BISON REQUIRED)
find_package(FLEX REQUIRED)

BISON_TARGET(Parser
    parser.yy
    ${CMAKE_CURRENT_BINARY_DIR}/parser.cc
    DEFINES_FILE ${CMAKE_CURRENT_BINARY_DIR}/parser.h
)

FLEX_TARGET(Lexer
    lexer.l
    ${CMAKE_CURRENT_BINARY_DIR}/lexer.cc
)

ADD_FLEX_BISON_DEPENDENCY(Lexer Parser)

add_library(driver
    driver.cc
)
target_include_directories(driver
    PRIVATE ${CMAKE_CURRENT_BINARY_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
)

add_executable(sql_parser
    main.cc
    ${CMAKE_CURRENT_BINARY_DIR}/parser.cc
    ${CMAKE_CURRENT_BINARY_DIR}/lexer.cc
)
target_include_directories(sql_parser
    PRIVATE ${CMAKE_CURRENT_BINARY_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
)
target_link_libraries(sql_parser
    driver
)