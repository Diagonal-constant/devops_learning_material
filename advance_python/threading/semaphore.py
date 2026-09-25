import threading, time

MAX_CONCURRENT_REQUESTS = 3
semaphore = threading.Semaphore(MAX_CONCURRENT_REQUESTS)
def call_api(i):
    with semaphore:
        print(f"[{i}] calling API ({threading.active_count()-1} threads total)")
        time.sleep(1) # simulate the request
        print(f"[{i}] done")
        
        
threads = [threading.Thread(target=call_api, args=(i,)) for i in range(10)]
for t in threads: t.start()
for t in threads: t.join()
# At most 3 threads are ever inside the "with semaphore" block at once.