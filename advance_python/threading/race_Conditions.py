-- Active: 1778384394026@@192.168.100.129@1433
import threading
counter = 0

def increment():
    global counter
    for _ in range(200_000):
        counter += 1 # NOT atomic: read, add 1, write back
        
threads = [threading.Thread(target=increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(counter) # Expected 800000, but usually prints something LESS, e.g.