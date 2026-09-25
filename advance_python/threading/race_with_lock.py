import threading

counter = 0
# 1. Create a lock object
counter_lock = threading.Lock()

def increment():
    global counter
    for _ in range(200_000):
        # 2. Acquire the lock before touching the shared resource
        with counter_lock:
            counter += 1 
        # 3. The lock is automatically released when exiting the 'with' block
        
threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()

print(counter) # Will ALWAYS print exactly 800000