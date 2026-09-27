"""
Blocking (Synchronous) Methods:
pool.apply(func, args=()): Runs a single task in the pool. It blocks the main process until that task finishes. (Rarely used because it eliminates parallelism).

pool.map(func, iterable): Parallel version of Python's built-in map(). It breaks the iterable into chunks, distributes them across workers, and blocks until every task is done. Returns an ordered list of results.

pool.starmap(func, iterable_of_tuples): Same as map(), but accepts functions with multiple arguments by unpacking tuples: func(*args).

"""
import multiprocessing as mp 
from multiprocessing import Pool
import os
import time 

def square_number(n):
    """Takes a number, squares it. Simulates some work."""
    print(f"  Worker processing: {n}")
    time.sleep(0.5)  # Simulate some real work
    return n * n

def multiply(a, b):
    """Multiplies two numbers."""
    print(f"  Multiplying: {a} × {b}")
    return a * b


if __name__ == '__main__':
    # ----------------------------
    # 1A. pool.map() - Most Common
    # ----------------------------
    print("\n1A. pool.map() - Like ordering pizza for a party (wait for ALL)")
    print("\n All workers run at once. Main program blocks until every task finishes. Best when you need all results at the end.")
    
    """
        Time        Worker 1        Worker 2        Worker 3
    ------------------------------------------------------
    0.0s        Processing: 1   Processing: 2   Processing: 3   <-- Wave 1
    0.5s        Done (1*1=1)    Done (2*2=4)    Done (3*3=9)
                
    0.5s        Processing: 4   Processing: 5   (Idle)          <-- Wave 2
    1.0s        Done (4*4=16)   Done (5*5=25)

    1.0s --> Main Process collects: [1, 4, 9, 16, 25]
    
    """
    
    
    print("-" * 70)
    
    start = time.time()
    
    with Pool(processes=3) as pool:  # Create 3 workers
        numbers = [1, 2, 3, 4, 5]
        results = pool.map(square_number, numbers)
        # ⬆️ CODE BLOCKS HERE - Waits for all results before continuing
    
    elapsed = time.time() - start
    print(f"\nResults: {results}")
    print(f"Time taken: {elapsed:.2f} seconds")
    print("✓ Got all results at once!")
    


if __name__ == '__main__':
    
    print("\n\n1B. pool.apply() - Only 1 worker at a time (Don't use this!)")
    print("-" * 70)
    start = time.time()
    
    with Pool(processes=3) as pool:  # Even though we have 3 workers...
        # apply() only uses 1 worker at a time
        result1 = pool.apply(square_number, args=(1,))  # Blocks here
        result2 = pool.apply(square_number, args=(2,))  # Then blocks here
        result3 = pool.apply(square_number, args=(3,))  # Then blocks here
    
    elapsed = time.time() - start
    print(f"Results: {result1}, {result2}, {result3}")
    print(f"Time taken: {elapsed:.2f} seconds")
    print("✗ VERY SLOW! Only 1 worker works at a time. Don't use this!")

# ----------------------------
# 1C. pool.starmap() - Multiple arguments
# ----------------------------

if __name__ == '__main__':
    print("\n\n1C. pool.starmap() - When function needs multiple arguments")
    print("-" * 70)
    start = time.time()
    
    with Pool(processes=2) as pool:
        # Each tuple gets unpacked as arguments
        pairs = [(2, 3), (4, 5), (6, 7)]
        results = pool.starmap(multiply, pairs)
    
    elapsed = time.time() - start
    print(f"Results: {results}")
    print(f"Time taken: {elapsed:.2f} seconds")
    print("✓ starmap unpacks tuples: (2,3) → multiply(2, 3)")



