include_directories(${PROJECT_SOURCE_DIR}/lib)

## kvs
add_executable(kvs
    kvs.cc
)

## main
add_executable(main
    main.cc
)