use std::cell::UnsafeCell;
use std::collections::HashMap;
use std::collections::HashSet;
use std::sync::atomic::{fence, AtomicU64, Ordering};

const STRIPE_SIZE: usize = 8; // 8-byte stripes
const MEM_SIZE: usize = 512; // 512-byte memory

pub struct Memory {
    mem: Vec<u8>,
    lock_ver: Vec<AtomicU64>,
    global_clock: AtomicU64,

    shift_size: u32,
}

impl Memory {
    pub fn new() -> Self {
        let mem = [0].repeat(MEM_SIZE);

        let shift = STRIPE_SIZE.trailing_zeros();
        let mut lock_ver = Vec::with_capacity(MEM_SIZE >> shift);
        for _ in 0..(MEM_SIZE >> shift) {
            lock_ver.push(AtomicU64::new(0));
        }

        Memory {
            mem,
            lock_ver,
            global_clock: AtomicU64::new(0),
            shift_size: shift,
        }
    }

    fn inc_global_clock(&self) -> u64 {
        self.global_clock.fetch_add(1, Ordering::AcqRel)
    }

    fn get_addr_ver(&self, addr: usize) -> u64 {
        let idx = addr >> self.shift_size;
        let n = self.lock_ver[idx].load(Ordering::Relaxed);

        // lower 63-bits of n is the version number
        n & !(1 << 63)
    }

    fn test_not_modify(&self, addr: usize, rv: u64) -> bool {
        let idx = addr >> self.shift_size;
        let n = self.lock_ver[idx].load(Ordering::Relaxed);

        // Check if the version number is lower than rv
        // and the lock bit is not set.
        n <= rv
    }

    fn lock_addr(&mut self, addr: usize) -> bool {
        let idx = addr >> self.shift_size;
        self.lock_ver[idx]
            .fetch_update(Ordering::Relaxed, Ordering::Relaxed, |n| {
                if n & (1 << 63) == 0 {
                    // lock bit is not set
                    Some(n | (1 << 63))
                } else {
                    // lock bit is set
                    None
                }
            })
            .is_ok()
    }

    fn unlock_addr(&mut self, addr: usize) {
        let idx = addr >> self.shift_size;
        self.lock_ver[idx].fetch_and(!(1 << 63), Ordering::Relaxed);
    }
}

pub struct ReadTrans<'a> {
    read_ver: u64,
    is_abort: bool,
    mem: &'a Memory,
}

impl<'a> ReadTrans<'a> {
    pub fn new(mem: &'a Memory) -> Self {
        ReadTrans {
            read_ver: mem.global_clock.load(Ordering::Acquire),
            is_abort: false,
            mem,
        }
    }

    pub fn load(&mut self, addr: usize) -> Option<[u8; STRIPE_SIZE]> {
        if self.is_abort {
            return None;
        }

        assert_eq!(addr & (STRIPE_SIZE - 1), 0);
        if !self.mem.test_not_modify(addr, self.read_ver) {
            self.is_abort = true;
            return None;
        }
        fence(Ordering::Acquire);

        // Copy memory
        let mut mem = [0; STRIPE_SIZE];
        for (dst, src) in mem
            .iter_mut()
            .zip(self.mem.mem[addr..addr + STRIPE_SIZE].iter())
        {
            *dst = *src;
        }

        fence(Ordering::SeqCst);
        if !self.mem.test_not_modify(addr, self.read_ver) {
            self.is_abort = true;
            return None;
        }

        Some(mem)
    }
}

pub struct WriteTrans<'a> {
    read_ver: u64,
    read_set: HashSet<usize>,
    write_set: HashMap<usize, [u8; STRIPE_SIZE]>,
    locked: Vec<usize>,
    is_abort: bool,
    mem: &'a mut Memory,
}

impl<'a> Drop for WriteTrans<'a> {
    fn drop(&mut self) {
        for addr in self.locked.iter() {
            self.mem.unlock_addr(*addr);
        }
    }
}

impl<'a> WriteTrans<'a> {
    fn new(mem: &'a mut Memory) -> Self {
        WriteTrans {
            read_set: HashSet::new(),
            write_set: HashMap::new(),
            locked: Vec::new(),
            is_abort: false,

            read_ver: mem.global_clock.load(Ordering::Acquire),
            mem,
        }
    }

    pub fn store(&mut self, addr: usize, val: [u8; STRIPE_SIZE]) {
        assert_eq!(addr & (STRIPE_SIZE - 1), 0);
        self.write_set.insert(addr, val);
    }

    pub fn load(&mut self, addr: usize) -> Option<[u8; STRIPE_SIZE]> {
        if self.is_abort {
            return None;
        }
        self.read_set.insert(addr);

        if let Some(m) = self.write_set.get(&addr) {
            return Some(*m);
        }

        if !self.mem.test_not_modify(addr, self.read_ver) {
            self.is_abort = true;
            return None;
        }
        fence(Ordering::Acquire);

        let mut mem = [0; STRIPE_SIZE];
        for (dst, src) in mem
            .iter_mut()
            .zip(self.mem.mem[addr..addr + STRIPE_SIZE].iter())
        {
            *dst = *src;
        }

        fence(Ordering::SeqCst);
        if !self.mem.test_not_modify(addr, self.read_ver) {
            self.is_abort = true;
            return None;
        }

        Some(mem)
    }

    fn lock_write_set(&mut self) -> bool {
        for (addr, _) in self.write_set.iter() {
            if self.mem.lock_addr(*addr) {
                self.locked.push(*addr);
            } else {
                return false;
            }
        }
        true
    }

    fn validate_read_set(&self) -> bool {
        for addr in self.read_set.iter() {
            if self.write_set.contains_key(addr) {
                let ver = self.mem.get_addr_ver(*addr);
                if ver > self.read_ver {
                    return false;
                }
            } else if !self.mem.test_not_modify(*addr, self.read_ver) {
                return false;
            }
        }
        true
    }

    fn commit(&mut self, ver: u64) {
        for (addr, val) in self.write_set.iter() {
            let addr = *addr;
            for (dst, src) in self.mem.mem[addr..addr + STRIPE_SIZE].iter_mut().zip(val) {
                *dst = *src;
            }
        }
        fence(Ordering::Release);

        for (addr, _) in self.write_set.iter() {
            let idx = addr >> self.mem.shift_size;
            self.mem.lock_ver[idx].store(ver, Ordering::Relaxed);
        }
        self.locked.clear();
    }
}

pub enum STMResult<T> {
    Ok(T),
    Retry,
    Abort,
}

pub struct STM {
    mem: UnsafeCell<Memory>,
}

unsafe impl Sync for STM {}
unsafe impl Send for STM {}

impl STM {
    pub fn new() -> Self {
        STM {
            mem: UnsafeCell::new(Memory::new()),
        }
    }

    pub fn read_transaction<F, R>(&self, f: F) -> Option<R>
    where
        F: Fn(&mut ReadTrans) -> STMResult<R>,
    {
        let mut tr = ReadTrans::new(unsafe { &*self.mem.get() });
        loop {
            match f(&mut tr) {
                STMResult::Ok(val) => {
                    if tr.is_abort {
                        continue;
                    } else {
                        return Some(val);
                    }
                }
                STMResult::Retry => {
                    if tr.is_abort {
                        continue;
                    }
                    return None;
                }
                STMResult::Abort => {
                    return None;
                }
            }
        }
    }

    pub fn write_transaction<F, R>(&self, f: F) -> Option<R>
    where
        F: Fn(&mut WriteTrans) -> STMResult<R>,
    {
        loop {
            // 1. Create a new transaction
            let mut tr = WriteTrans::new(unsafe { &mut *self.mem.get() });

            // 2. Execute the transaction speculatively
            let result;
            match f(&mut tr) {
                STMResult::Ok(val) => {
                    if tr.is_abort {
                        continue;
                    }
                    result = val;
                }
                STMResult::Retry => {
                    if tr.is_abort {
                        continue;
                    }
                    return None;
                }
                STMResult::Abort => {
                    return None;
                }
            };

            // 3. lock write set
            if !tr.lock_write_set() {
                continue;
            }

            // 4. increment global clock
            let ver = 1 + tr.mem.inc_global_clock();

            // 5. validate read set
            if tr.read_ver + 1 != ver && !tr.validate_read_set() {
                continue;
            }

            // 6. commit
            tr.commit(ver);

            return Some(result);
        }
    }
}
