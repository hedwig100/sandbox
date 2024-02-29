#!/bin/bash 
cd "$(dirname "$0")"

assert() {
    expected="$1"
    input="$2"

    ../../target/debug/compiler "$input" > tmp.s
    cc -o tmp tmp.s
    ./tmp
    actual="$?"

    if [ "$actual" = "$expected" ]; then
        echo "$input => $actual"
    else
        echo "$input => $expected expected, but got $actual"
        exit 1
    fi
}

cargo build --bin compiler

assert 0 0
assert 42 42

echo OK
