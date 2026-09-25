import threading, time

def slow_task():
    time.sleep(3)
    print("Finished slow task")
    
t = threading.Thread(target=slow_task,daemon=True)
t.start()
t.join(timeout=5.0)
if t.is_alive():
    print("Still running after 1s — did not finish in time, thread was NOT killed")
else:
    print("Finished within 1s")