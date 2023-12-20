use std::sync::{Arc, Mutex};
use std::thread;

// Mutexの使用例
// Arc<Mutex<T>> が複数スレッドで使うときの基本形
// 下みたいにlock()してから使う. ロックはスコープを抜けると自動的に解除される.
fn some_func(lock: Arc<Mutex<(i32, i32)>>) {
    loop {
        let mut guard = lock.lock().unwrap();
        let (ref mut a, _) = *guard;
        *a += 1;
        println!("{}", a);
    }
}

fn main() {
    let lock0 = Arc::new(Mutex::new((0, 1)));
    let lock1 = lock0.clone();

    let th0 = thread::spawn(move || {
        some_func(lock0);
    });
    let th1 = thread::spawn(move || {
        some_func(lock1);
    });

    th0.join().unwrap();
    th1.join().unwrap();
}
