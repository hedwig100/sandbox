mod semaphore;

use semaphore::Semaphore;
use std::collections::LinkedList;
use std::sync::{Arc, Mutex, Condvar};

#[derive(Clone)]
pub struct Sender<T> {
    sem: Arc<Semaphore>,
    buf: Arc<Mutex<LinkedList<T>>>,
    cond: Arc<Condvar>,// 読み込み側が待機するための条件変数
}

impl<T: Send> Sender<T> {
    pub fn send(&self, data: T) {
        self.sem.wait();
        let mut buf = self.buf.lock().unwrap();
        buf.push_back(data);
        self.cond.notify_one();
    }
}

pub struct Receiver<T> {
    sem: Arc<Semaphore>,
    buf: Arc<Mutex<LinkedList<T>>>,
    cond: Arc<Condvar>,// 読み込み側が待機するための条件変数
}

impl<T> Receiver<T> {
    pub fn recv(&self) -> T {
        let mut buf = self.buf.lock().unwrap();
        loop {
            if let Some(data) = buf.pop_front() {
                self.sem.post();
                return data;
            }
            buf = self.cond.wait(buf).unwrap();
        }
    }
}

pub fn channel<T>(max: isize) -> (Sender<T>, Receiver<T>) {
    let sem = Arc::new(Semaphore::new(max));
    let buf = Arc::new(Mutex::new(LinkedList::new()));
    let cond = Arc::new(Condvar::new());
    let sender = Sender{
        sem: sem.clone(),
        buf: buf.clone(),
        cond: cond.clone(),
    };
    let receiver = Receiver{
        sem,
        buf,
        cond,
    };
    (sender, receiver)
}

const NUM_LOOP: usize = 1000000;
const NUM_THREADS: usize = 8;

fn main() {
    let (sender, receiver) = channel(4);
    let mut v = Vec::new();

    let t = std::thread::spawn(move || {
        let mut cnt =0;
        while cnt < NUM_THREADS * NUM_LOOP {
            let data = receiver.recv();
            println!("recv: n = {:?}", data);
            cnt += 1;
        }
    });

    v.push(t);

    for i in 0..NUM_THREADS {
        let sender = sender.clone();
        let t = std::thread::spawn(move || {
            for j in 0..NUM_LOOP {
                sender.send((i,j));
            }
        });
        v.push(t);
    }

    for t in v {
        t.join().unwrap();
    }
}