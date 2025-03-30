#!/usr/bin/python3
from bcc import BPF
from time import sleep

program = r"""
BPF_HASH(uid_count);

int hello(struct bpf_raw_tracepoint_args *ctx) {
    u64 uid;
    u64 counter = 0;
    u64 *p;

    uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;
    p = uid_count.lookup(&uid);
    if (p != 0) {
        counter = *p;    
    }
    counter++;
    uid_count.update(&uid, &counter);
    return 0;
}
"""

b = BPF(text=program)
b.attach_raw_tracepoint(tp="sys_enter", fn_name="hello")

while True:
    sleep(2)
    s = ""
    for k, v in b["uid_count"].items():
        s += f"ID {k.value}: {v.value}\t"
    print(s)
