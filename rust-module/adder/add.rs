use super::sub;

pub fn add(x: i32, y: i32) -> i32 {
    x + y
}

pub fn aaa() -> i32 {
    crate::adder::sub::sub(1, 2);
    4
}

#[allow(dead_code)]
pub fn bbb() -> i32 {
    sub::sub2(1, 2);
    4
}