"""
Non-Blocking (Asynchronous) Methods:
pool.apply_async(func, args=(), callback=None): Submits a single task and immediately returns an AsyncResult object without blocking. You call .get() on the result later when you need the output.

pool.map_async(func, iterable): Asynchronous version of map(). Returns an AsyncResult object immediately.

pool.imap(func, iterable) / pool.imap_unordered(func, iterable): Memory-Efficient Generators. Instead of waiting for all tasks to complete and returning a giant list in memory, imap yields results one by one as workers finish them. imap_unordered yields whichever result finishes first, ignoring input order for maximum speed.

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

def slow_square(n):
    time.sleep(1)  # Takes 1 second per item
    return n * n


# ----------------------------
# 2A. pool.apply_async() - Single task, get result later
# ----------------------------

if __name__ == '__main__':
    print("\n2A. pool.apply_async() - Start 1 task, do other stuff, check result later")
    print("-" * 70)

    starttime = time.time()

    numbers = [5, 6, 9]
    async_results = []

    with Pool(processes=3) as pool:
        # Submit all tasks asynchronously (non-blocking)
        for num in numbers:
            result_obj = pool.apply_async(square_number, args=(num,))
            async_results.append(result_obj)

        print("All tasks submitted! Main program continues working...")
        
        # Do other work in main process here...
        time.sleep(0.2)
        print("Main process doing other work...")

        # Collect results when ready (this step blocks until results finish)
        results = [res.get() for res in async_results]

    print(f"\nFinal Results: {results}")
    print(f"Time taken: {time.time() - starttime:.2f} seconds")
    
    
# 2B. pool.map_async() - Multiple tasks, get all results later
# ----------------------------

"""
in case of map_async() and starmap_async(), the main process can continue doing other work while the worker processes are busy. The results are collected later when needed.
and the main process get blocked only when it calls async_result.get() to retrieve the results, which happens after all worker processes have completed their tasks.

Worker 1 (Fast):   |--- 0.2s ---| (Done, saved to internal buffer)
Worker 2 (Heavy):  |-------------------- 2.0s --------------------| (Done)
Worker 3 (Fast):   |--- 0.3s ---| (Done, saved to internal buffer)

Main Process:      ================= async_result.get() BLOCKS =================> Returns [Res1, Res2, Res3] at 2.0s
"""


if __name__ == '__main__':
    print("\n\n2B. pool.map_async() - Start multiple tasks, get results later")
    print("-" * 70)

    with Pool(processes=3) as pool:
        numbers = [10, 20, 30, 40]
        
        # Start ALL tasks but don't wait
        async_result = pool.map_async(square_number, numbers)
        print("All tasks started! Main program continues...")
        
        # Do other stuff
        print("Main program doing other work for 2 seconds...")
        time.sleep(2)
        
        # NOW get all results
        results = async_result.get()  # ⬅️ Get all results at once
        print(f"Got all results: {results}")


if __name__ == '__main__':
    args_list = [(5, 2), (6, 3), (9, 4)]

    with Pool(processes=3) as pool:
        async_result = pool.starmap_async(multiply, args_list)

        print("Multi-arg batch started! Main process continues...")

        results = async_result.get()

    print(f"\nFinal Results: {results}")  # [10, 18, 36]
    

"""

the imap and imap_unordered methods are memory-efficient because they yield results one by one as soon as each worker finishes its task, rather than waiting for all tasks to complete and returning a large list in memory. This is particularly useful when dealing with large datasets or long-running tasks.
the worker start working in parallel in the background here 'iterator = pool.imap(slow_square, numbers)' , while the main process can continue doing other work. The main process only blocks when it tries to retrieve results from the iterator, which happens after all worker processes have completed their tasks.
the below table illustrates the non-blocking behavior of the main process while workers are processing tasks in parallel. The main process can continue doing other work while the workers are busy, and it only blocks when it tries to retrieve results from the iterator.

Time    Worker Status (Parallel Background)      Loop Action in Main Process
-----------------------------------------------------------------------------------------------------
0.0s    All workers start processing.            Loop enters, asks for Item 1.
        Worker 1 working (1s task)...            LOOP BLOCKS waiting for Item 1...
        Worker 2 working (2s task)...
        Worker 3 working (0.5s task)...

0.5s    Worker 3 FINISHES Item 3!                Loop is STILL BLOCKED waiting for Item 1.
                                                 (Item 3 is buffered in memory).

1.0s    Worker 1 FINISHES Item 1!                Loop UNBLOCKS -> Prints Item 1!
                                                 Loop immediately asks for Item 2...
                                                 LOOP BLOCKS waiting for Item 2...

2.0s    Worker 2 FINISHES Item 2!                Loop UNBLOCKS -> Prints Item 2!
                                                 Loop immediately asks for Item 3...
                                                 Item 3 is ALREADY finished!
                                                 Loop DOES NOT BLOCK -> Prints Item 3 instantly!

"""


if __name__ == '__main__':
    with mp.Pool(processes=3) as pool:
        numbers = [1, 2, 3]

        # 1. Workers start executing immediately in the background
        iterator = pool.imap(slow_square, numbers)

        print("Main process: Started workers. Now doing other work...")

        # 2. Main process does heavy/other work for 2 seconds
        # Meanwhile, all 3 workers finish their 1-second tasks in parallel!
        time.sleep(2)

        print("Main process: Done with other work. Reading results now...\n")

        # 3. Because 2 seconds have passed, all worker results are already finished!
        start_time = time.time()
        for result in iterator:
            print(f"Got result: {result}")
        
        print(f"\nLoop completed in {time.time() - start_time:.4f} seconds!")
        
# ----------------------------
# 2D. pool.imap_unordered() - Get results in ANY order (FASTEST)
# ----------------------------
print("\n\n2D. pool.imap_unordered() - Get results in any order they finish")
print("-" * 70)

if __name__ == '__main__':
    with Pool(processes=3) as pool:
        numbers = [111, 222, 333, 444, 555]
        
        result_generator = pool.imap_unordered(square_number, numbers)
        
        print("\nGetting results in COMPLETION order (not input order):")
        for idx, result in enumerate(result_generator, 1):
            print(f"  {idx}. Got result: {result}")


# ============================================================================
# PART 3: QUICK COMPARISON TABLE
# ============================================================================

print("\n\n" + "="*70)
print("QUICK COMPARISON")
print("="*70)

comparison_table = """
╔════════════════════╦═════════════╦═════════════╦══════════════════════╗
║ Method             ║ Blocks?     ║ Returns     ║ Best For             ║
╠════════════════════╬═════════════╬═════════════╬══════════════════════╣
║ map()              ║ YES         ║ List (all)  ║ Simple parallel work ║
║ starmap()          ║ YES         ║ List (all)  ║ Multiple arguments   ║
║ apply()            ║ YES         ║ Single val  ║ Rarely used!         ║
╠════════════════════╬═════════════╬═════════════╬══════════════════════╣
║ apply_async()      ║ NO          ║ AsyncResult ║ Single background    ║
║                    ║             ║             ║ task                 ║
║ map_async()        ║ NO          ║ AsyncResult ║ Multiple background  ║
║                    ║             ║             ║ tasks                ║
║ imap()             ║ NO          ║ Generator   ║ Large datasets,      ║
║                    ║             ║             ║ ordered results      ║
║ imap_unordered()   ║ NO          ║ Generator   ║ Large datasets,      ║
║                    ║             ║             ║ speed is priority    ║
╚════════════════════╩═════════════╩═════════════╩══════════════════════╝
"""
print(comparison_table)


# ============================================================================
# PART 5: WHEN TO USE EACH METHOD
# ============================================================================

print("\n\n" + "="*70)
print("DECISION GUIDE: Which Method to Use?")
print("="*70)

decision_guide = """
START HERE: What do you need to do?

1. Do you have MULTIPLE tasks to run in parallel?
   → YES: Go to step 2
   → NO: You don't need multiprocessing

2. Can you wait for ALL results at the end?
   → YES: Use pool.map()  ✓ (Simplest, most common)
   → NO: Go to step 3

3. Do you want results as they finish?
   → YES: Use pool.imap() ✓ (Process 1 by 1)
   → NO: Use pool.map_async() and .get()

4. Does your function need multiple arguments?
   → YES: Use pool.starmap()
   → NO: Use pool.map()

5. Do you have MILLIONS of items and limited RAM?
   → YES: Use pool.imap_unordered()
   → NO: Use pool.map() or pool.imap()

AVOID:
❌ pool.apply() - Too slow, only use if you must run 1 task at a time
❌ pool.apply_async() - Complicated, use for special cases only
"""
print(decision_guide)

print("\n" + "="*70)
print("END OF GUIDE")
print("="*70)
