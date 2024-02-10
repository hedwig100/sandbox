use nix::sys::mman::{mprotect, ProtFlags};
use std::alloc::Layout;
use std::collections::HashSet;
use std::collections::LinkedList;
use std::ffi::c_void;
use std::ptr;

// Page size
const PAGE_SIZE: usize = 4 * 1024;

// Context of the main function
static mut CTX_MAIN: Option<Box<Registers>> = None;

// Unnecessary stack
static mut UNUSED_STACK: (*mut u8, Layout) = (std::ptr::null_mut(), Layout::new::<u8>());

// Queue of threds
static mut CONTEXTS: LinkedList<Box<Context>> = LinkedList::new();

// Set of thread Ids
static mut ID: *mut HashSet<u64> = ptr::null_mut();

fn get_id() -> u64 {
    loop {
        let rnd = rand::random::<u64>();
        unsafe {
            if !(*ID).contains(&rnd) {
                (*ID).insert(rnd);
                return rnd;
            }
        }
    }
}

#[repr(C)]
struct Registers {
    rbx: u64,
    rbp: u64,
    r12: u64,
    r13: u64,
    r14: u64,
    r15: u64,
    rsp: u64,
    rdx: u64,
}

impl Registers {
    fn new(rsp: u64) -> Self {
        Registers {
            rbx: 0,
            rbp: 0,
            r12: 0,
            r13: 0,
            r14: 0,
            r15: 0,
            rsp,
            rdx: entry_point as u64,
        }
    }
}

extern "C" {
    fn set_context(ctx: *mut Registers) -> u64;
    fn switch_context(ctx: *const Registers) -> !;
}

type Entry = fn();

// Context
struct Context {
    regs: Registers,
    stack: *mut u8,
    stack_layout: Layout,
    entry: Entry,
    id: u64, // Thread ID
}

impl Context {
    fn get_regs_mut(&mut self) -> *mut Registers {
        &mut self.regs
    }

    fn get_regs(&self) -> *const Registers {
        &self.regs
    }

    fn new(func: Entry, stack_size: usize, id: u64) -> Self {
        let layout = Layout::from_size_align(stack_size, PAGE_SIZE).unwrap();
        let stack = unsafe { std::alloc::alloc(layout) };
        unsafe { mprotect(stack as *mut c_void, PAGE_SIZE, ProtFlags::PROT_NONE).unwrap() };
        let regs = Registers::new(stack as u64 + stack_size as u64);
        Context {
            regs,
            stack,
            stack_layout: layout,
            entry: func,
            id,
        }
    }
}

pub fn spawn(func: Entry, stack_size: usize) -> u64 {
    unsafe {
        let id = get_id();
        CONTEXTS.push_back(Box::new(Context::new(func, stack_size, id)));
        schedule();
        id
    }
}

pub fn schedule() {
    unsafe {
        if CONTEXTS.len() == 1 {
            return;
        }

        let mut ctx = CONTEXTS.pop_front().unwrap();
        let regs = ctx.get_regs_mut();
        CONTEXTS.push_back(ctx);
        if set_context(regs) == 0 {
            let next = CONTEXTS.front().unwrap();
            switch_context(next.get_regs());
        }

        rm_unused_stack();
    }
}

extern "C" fn entry_point() {
    unsafe {
        let ctx = CONTEXTS.front().unwrap();
        (ctx.entry)();

        let ctx = CONTEXTS.pop_front().unwrap();
        (*ID).remove(&ctx.id);

        UNUSED_STACK = (ctx.stack, ctx.stack_layout);
        match CONTEXTS.front() {
            Some(next) => switch_context(next.get_regs()),
            None => {
                if let Some(main) = &CTX_MAIN {
                    switch_context(&**main as *const Registers);
                }
            }
        }
        panic!("Unreachable");
    }
}

pub fn spawn_from_main(func: Entry, stack_size: usize) {
    unsafe {
        if CTX_MAIN.is_some() {
            panic!("spawn_from_main is called twice.");
        }

        CTX_MAIN = Some(Box::new(Registers::new(0)));
        if let Some(ctx) = &mut CTX_MAIN {
            let mut ids = HashSet::new();
            ID = &mut ids as *mut HashSet<u64>;

            if set_context(&mut **ctx as *mut Registers) == 0 {
                CONTEXTS.push_back(Box::new(Context::new(func, stack_size, get_id())));
                let first = CONTEXTS.front().unwrap();
                switch_context(first.get_regs());
            }

            rm_unused_stack();
            CTX_MAIN = None;
            CONTEXTS.clear();

            ID = ptr::null_mut();
            ids.clear();
        }
    }
}

unsafe fn rm_unused_stack() {
    if UNUSED_STACK.0.is_null() {
        return;
    }
    mprotect(
        UNUSED_STACK.0 as *mut c_void,
        PAGE_SIZE,
        ProtFlags::PROT_READ | ProtFlags::PROT_WRITE,
    )
    .unwrap();
    std::alloc::dealloc(UNUSED_STACK.0, UNUSED_STACK.1);
    UNUSED_STACK = (std::ptr::null_mut(), Layout::new::<u8>());
}
