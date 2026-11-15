#!/usr/bin/env bash
# =============================================================================
# Operating Systems Lab - dev container banner
# =============================================================================
cat <<'BANNER'

  Operating Systems Lab - Ubuntu dev container

    gcc        C labs (fork/exec, threads, mutex, IPC, file systems)
    python3.10 Scheduling simulations (FCFS/SJF, RR, priority) + pytest
    gdb/strace Tracing syscalls and process state

    Task  "OS Lab: build & run all"        compile + run every lab
    Task  "OS Lab: run tests"               pytest -q
    Task  "OS Lab: lint (flake8)"           flake8 over the repository
    Task  "OS Lab: trace a syscall"         strace on a compiled lab binary

BANNER
