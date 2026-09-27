## Questions

```text
[Main Process] PID: 25184
[Child A] PID: 25195 | Parent PID: 25184
[Main Process] Both child processes have been launched in parallel...
[Child B] PID: 25214 | Parent PID: 25184
[Child A] Finished calculation: 41666654166667500000
[Child A] Local shared_data content: [41666654166667500000]
[Child B] Finished calculation: 291666629166667500000
[Child B] Local shared_data content: [291666629166667500000]

[Main Process] Total time taken: 0.57 seconds
[Main Process] Final shared_data in main: []

```

This is the output of my terminal, and I have a few questions:

* Why does `[Main Process] Both child processes have been launched in parallel...` print before starting Process B?
* For the `shared_data` list, are both processes storing the data in the same list, or does each one have a separate copy for itself? Why is `shared_data` in the main process empty?
* How much memory and CPU are allocated for each process, and how can I measure/get that?

---

## Answer

Here are the answers to your questions based on your exact execution output:

---

### 1. Why `[Main Process] Both child processes...` printed before `[Child B]` started

This happens because **process creation is asynchronous**.

When you execute:

```python
p1.start()
p2.start()
print("[Main Process] Both child processes have been launched in parallel...")

```

1. **`p1.start()`** asks the operating system to spawn Process A. The OS starts initializing Process A in the background.
2. **`p2.start()`** asks the OS to spawn Process B.
3. The **Main Process does not wait** for Process A or B to finish booting up. It immediately moves to the next line of code and prints `[Main Process] Both child processes...`.
4. Meanwhile, the OS is still spinning up Process A and Process B. In your run, Process A finished booting up slightly faster than Process B, but the Main Process printed its line before Process B was fully ready to execute its first `print()`.

---

### 2. How `shared_data` works across processes

**Each process gets its own completely separate copy of `shared_data`.**

Because you are using `spawn` (and multiprocessing in general), memory is totally isolated between processes:

```text
[Main Process]       --> Has shared_data = [] (Original)
       │
       ├──> [Child A] --> Gets a COPY of shared_data = []
       │                  Appends its total -> shared_data = [41666654166667500000]
       │
       └──> [Child B] --> Gets a COPY of shared_data = []
                          Appends its total -> shared_data = [291666629166667500000]

```

* **Child A** appends to its own private copy in memory.
* **Child B** appends to its own private copy in memory.
* **Main Process** never touches either child's memory space, so its `shared_data` remains completely untouched: `[]`.

To pass data back from child processes to the main process, you must use **Inter-Process Communication (IPC)** like `multiprocessing.Queue`, `Pipe`, or `Return values from Pools`.

---

### 3. How CPU and Memory are allocated & how to measure them

#### CPU Allocation

The OS kernel scheduler automatically decides which CPU core handles each process. If you have multiple CPU cores, the OS will distribute the Main process, Child A, and Child B across available cores.

#### Memory Allocation

Each process allocates its own RAM space for the Python interpreter instance plus all local variables (like `numbers1` and `numbers2`).

#### How to Measure Memory and CPU in Python

You can use the `psutil` and `os` libraries inside each process to inspect exact RSS memory usage (RAM) and CPU utilization:

```python
import os
import psutil

process = psutil.Process(os.getpid())
memory_mb = process.memory_info().rss / (1024 * 1024)
cpu_percent = process.cpu_percent(interval=0.1)

print(f"PID: {os.getpid()} | Memory Used: {memory_mb:.2f} MB | CPU: {cpu_percent}%")

```