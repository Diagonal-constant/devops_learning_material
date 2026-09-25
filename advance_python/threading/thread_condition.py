import threading 
import time 
import random 
from collections import deque 

queue = deque()

max_size =5 
lock = threading.Lock()
condition = threading.Condition(lock)

def producer():
    for i in range(10):
        print("it is time to sleep producer")
        time.sleep(random.uniform(0.1, 0.5)) # simulate work
        with condition:
            while len(queue) >= max_size:
                print("kitchen full, producer is waiting..")
                condition.wait() # wait until a slot is free
            queue.append(i)
            print(f"Produced {i}, queue size is now {len(queue)}")
            condition.notify() # notify a waiting consumer
        #lock is realesed automatically when the with block ends 
        
def consumer():
    for _ in range(10):
        with condition:
            while len(queue) == 0:
                print("kitchen empty, consumer is waiting..")
                condition.wait() # wait until an item is available
            item = queue.popleft()
            print(f"Consumed {item}, queue size is now {len(queue)}")
            condition.notify() # notify a waiting producer
        #lock is realesed automatically when the with block ends
        print("it is time to sleep consumer ")
        time.sleep(random.uniform(0.1, 0.5)) # simulate work

threads = [threading.Thread(target=producer), threading.Thread(target=consumer)]
for t in threads: t.start()
for t in threads: t.join()
