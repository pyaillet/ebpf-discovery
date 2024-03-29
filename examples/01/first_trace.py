#!/usr/bin/env python

from bcc import BPF
import os

print('Launching in background, pid: ', os.getpid())

# This may not work for 4.17 on x64, you need replace kprobe__sys_clone with kprobe____x64_sys_clone
BPF(text='''
int kprobe__sys_clone(void *ctx) {
  bpf_trace_printk("Hello, eBPF!\\n");
  return 0;
}
''').trace_print()
