import threading , time 

stop_event = threading.Event()

def slow_task():
    print("Starting slow task")
    while not stop_event.is_set():
        time.sleep(1)
        print("Still running...")
    print("Finished slow task")
    
thread_ = threading.Thread(target= slow_task)

thread_.start()
time.sleep(5)  # Let it run for 5 seconds
stop_event.set()  # Signal the thread to stop
thread_.join()  # Wait for the thread to finish
print("Thread has been stopped and joined successfully.")