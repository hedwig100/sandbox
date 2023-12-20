use std::sync::Arc;
use std::sync::RwLock;
use std::thread;

fn read(lock: Arc<RwLock<i32>>) {
    let r1 = lock.read().unwrap();
    println!("{}", *r1);
}

fn write(lock: Arc<RwLock<i32>>) {
    let mut w = lock.write().unwrap();
    *w = *w + 1;
    println!("Add 1");
}

fn main() {
    let write0 = Arc::new(RwLock::new(5));
    let write1 = write0.clone();
    let read0 = write0.clone();

    let c0 = thread::spawn(move || write(write0));
    let c1 = thread::spawn(move || read(read0));
    let c2 = thread::spawn(move || write(write1));

    c0.join().unwrap();
    c1.join().unwrap();
    c2.join().unwrap();
}
