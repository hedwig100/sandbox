use std::sync::Arc;
use std::{thread, time};

mod tl2;

#[macro_export]
macro_rules! load {
    ($t: ident, $a:expr) => {
        if let Some(v) = ($t).load($a) {
            v
        } else {
            return tl2::STMResult::Retry;
        }
    };
}

#[macro_export]
macro_rules! store {
    ($t: ident, $a:expr, $v:expr) => {
        ($t).store($a, $v);
    };
}

const NUM_PHILOSOPHERS: usize = 8;

fn philosopher(stm: Arc<tl2::STM>, n: usize) {
    let left = NUM_PHILOSOPHERS * n;
    let right = NUM_PHILOSOPHERS * ((n + 1) % NUM_PHILOSOPHERS);

    for t in 0..5 {
        println!("Philosopher {} is thinking {} times", n, t);
        while !stm
            .write_transaction(|tr| {
                let mut f1 = load!(tr, left);
                let mut f2 = load!(tr, right);
                if f1[0] == 0 && f2[0] == 0 {
                    f1[0] = 1;
                    f2[0] = 1;
                    store!(tr, left, f1);
                    store!(tr, right, f2);
                    tl2::STMResult::Ok(true)
                } else {
                    tl2::STMResult::Ok(false)
                }
            })
            .unwrap()
        {}

        stm.write_transaction(|tr| {
            let mut f1 = load!(tr, left);
            let mut f2 = load!(tr, right);
            f1[0] = 0;
            f2[0] = 0;
            store!(tr, left, f1);
            store!(tr, right, f2);
            tl2::STMResult::Ok(())
        });
    }
}

fn observer(stm: Arc<tl2::STM>) {
    for _ in 0..3 {
        let chopsticks = stm
            .read_transaction(|tr| {
                let mut chopsticks = [0; NUM_PHILOSOPHERS];
                for i in 0..NUM_PHILOSOPHERS {
                    chopsticks[i] = load!(tr, i * NUM_PHILOSOPHERS)[0];
                }
                tl2::STMResult::Ok(chopsticks)
            })
            .unwrap();

        println!("{:?}", chopsticks);

        let mut n = 0;
        for c in &chopsticks {
            if *c == 1 {
                n += 1;
            }
        }

        if n & 1 != 0 {
            panic!("inconsistent");
        }

        let us = time::Duration::from_micros(100);
        thread::sleep(us);
    }
}

fn main() {
    let stm = Arc::new(tl2::STM::new());

    let mut handles = vec![];

    for i in 0..NUM_PHILOSOPHERS {
        let stm = stm.clone();
        handles.push(thread::spawn(move || philosopher(stm, i)));
    }

    handles.push(thread::spawn(move || observer(stm)));

    for h in handles {
        h.join().unwrap();
    }
}
