import time 
import threading 
from numba import njit 

@njit(nogil=True)
def cpu_bound(n):
    x = 0
    for i in range(n):
        x += i * i
    return x
N = 40_000_0000

start_time = time.perf_counter()
print(f'starting time {start_time}')

output = cpu_bound(N)
output = cpu_bound(N)

end_time = time.perf_counter()

print(f'end time {end_time}')
print(f'time taken {end_time-start_time}')

## multi threading 

start_time = time.perf_counter()
print(f'starting time {start_time}')

thread1 = threading.Thread(target=cpu_bound, args=(N,))
thread2 = threading.Thread(target=cpu_bound, args=(N,))
thread1.start()
thread2.start()
thread1.join()
print(f'thread1 completed time {time.perf_counter()}')
thread2.join()
print(f'thread2 completed time {time.perf_counter()} and total time taken {time.perf_counter()-start_time}')  