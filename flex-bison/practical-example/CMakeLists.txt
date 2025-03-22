cmake_minimum_required(VERSION 3.21)

project(Calc VERSION 1.0 LANGUAGES CPP)

find_package(FLEX 2.6 REQUIRED)
find_package(BISON 3.0 REQUIRED)

flex_target(my_lexer
    lexer.l
    lexer.yy.cc
    DEFINES_FILE lexer.yy.h
)

bison_target(my_parser
    parser.y
    parser.tab.cc
    DEFINES_FILE parser.tab.h
)

add_flex_bison_dependency(my_lexer my_parser)

include_directories(${CMAKE_CURRENT_BINARY_DIR})

add_library(utils
    utils.cc
)

add_executable(calc 
    main.cc
    ${FLEX_my_lexer_OUTPUTS}
    ${BISON_my_parser_OUTPUTS}
)
target_link_libraries(calc
    ${FLEX_LIBRARIES}
    ${BISON_LIBRARIES}
)