// Declare a module named adder (folder module)
mod adder;

// Declare a module named mul (file module)
mod mul;

// Use adder::add to bring the add module into scope
use crate::adder::add;


fn main() {
    println!("{}", add::add(1, 2));   
    println!("{}", adder::sub::sub(1, 2));
    println!("{}", mul::mul(1, 2));
    println!("{}", mul::add_mul(1, 2,5));
    println!("Hello, world!");
}
