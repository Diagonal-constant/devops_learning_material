import multiprocessing
import os
import time
import psutil

# Global list to test memory isolation
shared_data = []

def print_process_stats(label):
    process = psutil.Process(os.getpid())
    # Memory in megabytes (RSS = Resident Set Size)
    mem_mb = process.memory_info().rss / (1024 * 1024)
    # CPU Core assigned to this process
    cpu_num = process.cpu_num() if hasattr(process, "cpu_num") else "N/A"

    print(
        f"[{label}] PID: {os.getpid()} | RAM: {mem_mb:.2f} MB | Running on CPU Core: {cpu_num}"
    )
    
    
def heavy_calculation(name, numbers):
    """A CPU-bound task that modifies a list and prints process info."""
    print(f"[Child {name}] PID: {os.getpid()} | Parent PID: {os.getppid()}")
    print_process_stats(f"Child {name}")
    # Simulate CPU work
    total = sum(n * n for n in numbers)
    
    # Try modifying the global variable
    shared_data.append(total)
    
    print(f"[Child {name}] Finished calculation: {total}")
    print(f"[Child {name}] Local shared_data content: {shared_data}")

if __name__ == "__main__":
    # 1. Always set start method safely inside the __main__ block
    # Using 'spawn' ensures consistent behavior across Linux, macOS, and Windows.
    multiprocessing.set_start_method("spawn", force=True)

    print(f"[Main Process] PID: {os.getpid()}")
    
    start_time = time.time()

    # Define inputs for 2 tasks
    numbers1 = list(range(1, 5_000_000))
    numbers2 = list(range(5_000_000, 10_000_000))

    # 2. Instantiate Process objects
    p1 = multiprocessing.Process(target=heavy_calculation, args=("A", numbers1))
    p2 = multiprocessing.Process(target=heavy_calculation, args=("B", numbers2))

    # 3. Start the processes
    p1.start()
    p2.start()

    print("[Main Process] Both child processes have been launched in parallel...")

    # 4. Wait for both processes to complete
    p1.join()
    p2.join()

    print(f"\n[Main Process] Total time taken: {time.time() - start_time:.2f} seconds")
    
    # 5. Observe Memory Isolation
    # The parent process's 'shared_data' remains empty because children operated in isolated memory!
    print(f"[Main Process] Final shared_data in main: {shared_data}")

