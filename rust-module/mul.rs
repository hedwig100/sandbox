// Use adder to bring the add module into scope
// You cannot use `mod adder;` in mul.rs 
// because adder is already declared in main.rs and that `mod adder;` in mul.rs
// means the adder is sub module of mul.rs
use crate::adder;

pub fn mul(a: i32, b: i32)  -> i32 {
    a * b
}

pub fn add_mul(a: i32, b: i32, c: i32) -> i32 {
    a + adder::add::add(b, c)
}