use futures::future::{BoxFuture, FutureExt};
use futures::task::{waker_ref, ArcWake};
use std::future::Future;
use std::pin::Pin;
use std::sync::mpsc::{sync_channel, Receiver, SyncSender};
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll};

struct Task {
    // The future it owns
    future: Mutex<BoxFuture<'static, ()>>,

    // Send myself to the executor
    sender: SyncSender<Arc<Task>>,
}

impl ArcWake for Task {
    fn wake_by_ref(arc_self: &Arc<Self>) {
        let cloned = arc_self.clone();
        arc_self.sender.send(cloned).expect("too many tasks queued");
    }
}

struct Executor {
    sender: SyncSender<Arc<Task>>,
    receiver: Receiver<Arc<Task>>,
}

impl Executor {
    fn new() -> Self {
        let (sender, receiver) = sync_channel(10000);
        Executor { sender, receiver }
    }

    fn get_spawner(&self) -> Spawner {
        Spawner {
            sender: self.sender.clone(),
        }
    }

    fn run(&self) {
        while let Ok(task) = self.receiver.recv() {
            let mut future = task.future.lock().unwrap();
            let waker = waker_ref(&task);
            let mut context = std::task::Context::from_waker(&waker);
            let _ = future.as_mut().poll(&mut context);
        }
    }
}

struct Spawner {
    sender: SyncSender<Arc<Task>>,
}

impl Spawner {
    fn spawn(&self, future: impl Future<Output = ()> + 'static + Send) {
        let task = Arc::new(Task {
            future: Mutex::new(future.boxed()),
            sender: self.sender.clone(),
        });

        self.sender.send(task).expect("too many tasks queued");
    }
}

struct Hello {
    state: StateHello,
}

#[allow(clippy::upper_case_acronyms)]
enum StateHello {
    HELLO,
    WORLD,
    END,
}

impl Hello {
    fn new() -> Self {
        Hello {
            state: StateHello::HELLO,
        }
    }
}

impl Future for Hello {
    type Output = ();

    fn poll(mut self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<()> {
        match self.state {
            StateHello::HELLO => {
                print!("Hello, ");
                self.state = StateHello::WORLD;
                _cx.waker().wake_by_ref();
                Poll::Pending
            }
            StateHello::WORLD => {
                println!("World!");
                self.state = StateHello::END;
                _cx.waker().wake_by_ref();
                Poll::Pending
            }
            StateHello::END => Poll::Ready(()),
        }
    }
}

fn main() {
    let executor = Executor::new();
    let spawner = executor.get_spawner();
    spawner.spawn(Hello::new());
    executor.run();
}
