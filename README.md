# Operating_Systems_Lab

Lab questions from 1 to 4 — C programs (system calls, threads, mutex, IPC, file systems) and Python
simulations (FCFS/SJF, round robin, priority scheduling).

## Run it in Ubuntu inside VS Code (dev container)

The whole lab runs in a **Linux (Ubuntu 22.04) container** opened in VS Code, so the C labs behave
exactly like they do on the lab machines — `fork`, `exec`, `pthread`, pipes and `strace` all work.

| File | Purpose |
| --- | --- |
| `.devcontainer/devcontainer.json` | Container definition, extensions, Python/C++ toolchain |
| `.devcontainer/Dockerfile` | Ubuntu 22.04 + gcc/g++ + Python 3.10 + make, gdb, strace |
| `.devcontainer/post-create.sh` | One-time bootstrap (toolchain check, `requirements.txt`) |
| `.devcontainer/post-start.sh` | Banner with the available commands |
| `Makefile` | `make` — compile, run, test and lint every lab |
| `.vscode/tasks.json` / `launch.json` | One-click tasks and debug configurations |

**Open it:** VS Code → `Ctrl+Shift+P` → **Dev Containers: Reopen in Container** (or *Open in
Container*). The first build takes a couple of minutes; after that the layer cache makes rebuilds
instant.

### Commands inside the container

```bash
make            # compile + run every lab
make build      # compile the C labs   (gcc -std=c17 -Wall -Wextra -O2 -g -pthread)
make run        # run every lab, transcripts land in <lab>/output/
make test       # pytest -q
make lint       # flake8 (same checks as the GitHub workflow)
make clean      # remove binaries and __pycache__
```

### One-click tasks

`Ctrl+Shift+P` → *Tasks: Run Task*

| Task | Does |
| --- | --- |
| `OS Lab: build & run all` | Compiles and runs every lab, capturing the transcript |
| `OS Lab: build all` / `OS Lab: run all` | One half only |
| `OS Lab: list labs` | Shows every source file that was discovered |
| `OS Lab: run tests` | `pytest -q` |
| `OS Lab: lint (flake8)` | The same checks the CI workflow runs |
| `OS Lab: trace a syscall` | Runs the system-calls lab under `strace` |
| `OS Lab: debug system_calls (gdb)` | The lab under `gdb` |

Debug configurations (`F5`): the two C labs under gdb, and the scheduling simulations under
debugpy.

## Layout convention

```
Lab1/Q1_System_Calls/
├── src/system_calls.c        # source
└── output/                   # compiled binary + captured transcript
    ├── system_calls          # binary (git-ignored)
    ├── process_output.txt    # written by the program itself
    └── terminal_output.txt   # transcript captured by `make run`
```

`make run` executes the C labs from inside their `output/` directory, so the files a lab creates
stay next to the rest of that lab's output.

## Lab 3 programs

Memory management and disk management questions, one program per question:

| Question | Program | Covers |
| --- | --- | --- |
| Q1 | `Lab3/Q1_Swapping_Address_Translation/src/swapping_address_translation.py` | First/best/worst fit allocation, base-limit address translation |
| Q2 | `Lab3/Q2_Paging_Segmentation/src/paging_segmentation.py` | Paging (page table, frame, offset) and segmentation (base/limit) |
| Q3 | `Lab3/Q3_FIFO_LRU/src/fifo_lru.py` | FIFO, LRU and optimal page replacement |
| Q4 | `Lab3/Q4_Device_Allocation/src/device_allocation.py` | Dedicated, shared and virtual devices, buffering |
| Q5 | `Lab3/Q5_FCFS_SSTF_SCAN_c-SCAN/src/disk_scheduling.py` | FCFS, SSTF, SCAN and C-SCAN disk scheduling, swap space bitmap |

`make run` executes every program and stores its transcript in the matching
`Lab3/Qn_*/output/` folder. `tests/test_lab3.py` checks the algorithms
(`make test`).

## Continuous integration

`.github/workflows/python-app.yml` runs on `ubuntu-latest` with Python 3.10 and performs the same
lint (`flake8`) and test (`pytest`) steps as `make lint` / `make test`.
