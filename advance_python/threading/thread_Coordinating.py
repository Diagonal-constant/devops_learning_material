import threading, time
ready = threading.Event()
shutdown = threading.Event()

def worker(worker_id):
    print(f"Worker {worker_id} waiting for ready signal...")
    ready.wait() # blocks here until main thread calls ready.set()
    print(f"Worker {worker_id} started")
    while not shutdown.is_set():
        time.sleep(0.3)
    # do periodic work
    print(f"Worker {worker_id} shutting down cleanly")
    
threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for t in threads: t.start()
time.sleep(1)
print("Main: releasing workers")
ready.set() # all 3 workers unblock at once
time.sleep(1.5)
print("Main: signaling shutdown")
shutdown.set()
for t in threads: t.join()