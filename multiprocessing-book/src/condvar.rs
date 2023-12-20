use std::sync::{Arc, Condvar, Mutex};
use std::thread;

fn child(id: u32, p: Arc<(Mutex<bool>, Condvar)>) {
    let (ref lock, ref cvar) = *p;
    let _guard = cvar
        .wait_while(lock.lock().unwrap(), |started| !*started)
        .unwrap();

    // This section is executed after condvar is notified.
    println!("thread id: {}", id);
}

fn parent(p: Arc<(Mutex<bool>, Condvar)>) {
    let &(ref lock, ref cvar) = &*p;
    let mut started = lock.lock().unwrap();
    *started = true;
    cvar.notify_all();
}

fn main() {
    let pair0 = Arc::new((Mutex::new(false), Condvar::new()));
    let pair1 = pair0.clone();
    let pair2 = pair0.clone();

    let th0 = thread::spawn(move || child(0, pair0));
    let th1 = thread::spawn(move || child(1, pair1));
    let th2 = thread::spawn(move || parent(pair2));

    th0.join().unwrap();
    th1.join().unwrap();
    th2.join().unwrap();
}
