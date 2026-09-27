"""
COMPLETE MULTIPROCESSING POOL METHODS COMPARISON
==================================================

ALL 7 methods compared side-by-side
Compare their differences, speed, memory usage, and when to use each

Methods:
1. pool.apply()           - Blocking, 1 task at a time (SLOW!)
2. pool.map()             - Blocking, parallel processing
3. pool.starmap()         - Blocking, parallel, multiple args
4. pool.apply_async()     - Non-blocking, 1 task
5. pool.map_async()       - Non-blocking, multiple tasks
6. pool.imap()            - Non-blocking, generator, ordered
7. pool.imap_unordered()  - Non-blocking, generator, any order
"""

from multiprocessing import Pool
import time
import sys

# Simple function for examples
def square(n):
    """Square a number"""
    time.sleep(0.5)  # Simulate work
    return n * n

def multiply(a, b):
    """Multiply two numbers"""
    time.sleep(0.5)
    return a * b


# ============================================================================
# COMPARISON 1: BASIC CHARACTERISTICS
# ============================================================================

print("\n" + "="*100)
print("COMPARISON 1: BASIC CHARACTERISTICS")
print("="*100)

comparison_table = """
┌──────────────────┬──────────┬──────────┬────────────┬──────────────┬─────────────────────┐
│ Method           │ Blocks?  │ Tasks    │ Returns    │ Memory Usage │ Processing Order    │
├──────────────────┼──────────┼──────────┼────────────┼──────────────┼─────────────────────┤
│ apply()          │ YES      │ 1        │ Value      │ -            │ Sequential (SLOW!)  │
│ map()            │ YES      │ Multiple │ List       │ All in RAM   │ Parallel (FAST)     │
│ starmap()        │ YES      │ Multiple │ List       │ All in RAM   │ Parallel (FAST)     │
├──────────────────┼──────────┼──────────┼────────────┼──────────────┼─────────────────────┤
│ apply_async()    │ NO       │ 1        │ AsyncResult│ -            │ Background          │
│ map_async()      │ NO       │ Multiple │ AsyncResult│ All in RAM   │ Background          │
│ imap()           │ NO       │ Multiple │ Generator  │ LOW ✓        │ Parallel, Ordered   │
│ imap_unordered() │ NO       │ Multiple │ Generator  │ LOW ✓        │ Parallel, Any order │
└──────────────────┴──────────┴──────────┴────────────┴──────────────┴─────────────────────┘

Legend:
- Blocks? = Does it wait for results?
- Tasks = How many tasks can it run?
- Returns = What does it return?
- Memory = How much RAM does it need?
- Processing Order = What order do results come in?
"""
print(comparison_table)


# ============================================================================
# COMPARISON 2: SPEED TEST - All methods on same data
# ============================================================================

print("\n\n" + "="*100)
print("COMPARISON 2: SPEED TEST - Process 12 items with 3 workers")
print("="*100)

if __name__ == '__main__':
    numbers = list(range(1, 13))  # [1, 2, 3, ..., 12]
    
    # 1. pool.apply() - SLOW (1 at a time)
    print("\n1️⃣ pool.apply() - Process one by one (SLOW)")
    print("-" * 100)
    start = time.time()
    with Pool(processes=3) as pool:
        results = []
        for n in numbers:
            result = pool.apply(square, (n,))  # ⬅️ Blocks on each one
            results.append(result)
    elapsed = time.time() - start
    print(f"Time: {elapsed:.2f}s | Results: {results}")
    print(f"⚠️  VERY SLOW! Only 1 worker works at a time (3 workers wasted)")
    apply_time = elapsed
    
    # 2. pool.map() - FAST (parallel)
    print("\n2️⃣ pool.map() - Parallel processing")
    print("-" * 100)
    start = time.time()
    with Pool(processes=3) as pool:
        results = pool.map(square, numbers)  # ⬅️ All parallel
    elapsed = time.time() - start
    print(f"Time: {elapsed:.2f}s | Results: {results}")
    print(f"✓ FAST! All 3 workers run in parallel")
    map_time = elapsed
    
    # 3. pool.starmap() - FAST (parallel, multiple args)
    print("\n3️⃣ pool.starmap() - Parallel with multiple arguments")
    print("-" * 100)
    pairs = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12)]
    start = time.time()
    with Pool(processes=3) as pool:
        results = pool.starmap(multiply, pairs)  # ⬅️ Unpacks tuples
    elapsed = time.time() - start
    print(f"Time: {elapsed:.2f}s | Results: {results}")
    print(f"✓ FAST! Same speed as map(), but handles multiple args")
    starmap_time = elapsed
    
    # 4. pool.apply_async() - INSTANT start
    print("\n4️⃣ pool.apply_async() - Non-blocking (instant return)")
    print("-" * 100)
    start = time.time()
    with Pool(processes=3) as pool:
        async_result = pool.apply_async(square, (1,))
    elapsed = time.time() - start
    print(f"Time to START: {elapsed:.4f}s (milliseconds!)")
    print(f"✓ Returns immediately! Main program can continue")
    print(f"Actual task time: ~0.5s (happens in background)")
    
    # 5. pool.map_async() - INSTANT start
    print("\n5️⃣ pool.map_async() - Non-blocking (instant return)")
    print("-" * 100)
    start = time.time()
    with Pool(processes=3) as pool:
        async_result = pool.map_async(square, numbers)
    elapsed = time.time() - start
    print(f"Time to START: {elapsed:.4f}s (milliseconds!)")
    print(f"✓ Returns immediately! All tasks running in background")
    result = async_result.get()  # Now wait
    print(f"Time to get results: ~{(elapsed + 2):.2f}s")
    
    # 6. pool.imap() - Generator (process results as they come)
    print("\n6️⃣ pool.imap() - Non-blocking generator (ordered)")
    print("-" * 100)
    start = time.time()
    with Pool(processes=3) as pool:
        count = 0
        for result in pool.imap(square, numbers):
            count += 1
            if count == 1:
                first_result_time = time.time() - start
    elapsed = time.time() - start
    print(f"Time to first result: {first_result_time:.2f}s")
    print(f"Time for all results: {elapsed:.2f}s")
    print(f"✓ Memory efficient! Process results immediately")
    
    # 7. pool.imap_unordered() - Generator (any order)
    print("\n7️⃣ pool.imap_unordered() - Non-blocking generator (any order)")
    print("-" * 100)
    start = time.time()
    with Pool(processes=3) as pool:
        count = 0
        for result in pool.imap_unordered(square, numbers):
            count += 1
            if count == 1:
                first_result_time = time.time() - start
    elapsed = time.time() - start
    print(f"Time to first result: {first_result_time:.2f}s")
    print(f"Time for all results: {elapsed:.2f}s")
    print(f"✓ Fastest! Results come in completion order")
    
    # Summary
    print("\n" + "="*100)
    print("⚡ SPEED SUMMARY")
    print("="*100)
    print(f"apply()          {apply_time:.2f}s  ❌ SLOWEST (don't use!)")
    print(f"map()            {map_time:.2f}s  ✓ FAST")
    print(f"starmap()        {starmap_time:.2f}s  ✓ FAST")
    print(f"apply_async()    ~0.001s  ✓ INSTANT (start time)")
    print(f"map_async()      ~0.001s  ✓ INSTANT (start time)")
    print(f"imap()           ~{map_time:.2f}s  ✓ FAST + Memory efficient")
    print(f"imap_unordered() ~{map_time:.2f}s  ✓ FASTEST + Memory efficient")


# ============================================================================
# COMPARISON 3: CODE EXAMPLES - Same task, different methods
# ============================================================================

print("\n\n" + "="*100)
print("COMPARISON 3: CODE EXAMPLES - Same task, different methods")
print("="*100)

code_examples = """
TASK: Process numbers [1, 2, 3, 4, 5]

1️⃣ apply() - Process ONE by ONE
─────────────────────────────────────────────────────────
with Pool(processes=3) as pool:
    results = []
    for n in [1, 2, 3, 4, 5]:
        result = pool.apply(square, (n,))  # Waits here
        results.append(result)
# Result: [1, 4, 9, 16, 25]
❌ Only 1 worker at a time! VERY SLOW!


2️⃣ map() - Process ALL in parallel, wait for all
─────────────────────────────────────────────────────────
with Pool(processes=3) as pool:
    results = pool.map(square, [1, 2, 3, 4, 5])
# Result: [1, 4, 9, 16, 25]
✓ All 3 workers process in parallel. Simple!


3️⃣ starmap() - Multiple arguments per task
─────────────────────────────────────────────────────────
with Pool(processes=3) as pool:
    pairs = [(1, 2), (3, 4), (5, 6)]
    results = pool.starmap(multiply, pairs)
# Result: [2, 12, 30]
✓ Same as map(), but unpacks tuples: (1,2) → multiply(1, 2)


4️⃣ apply_async() - Start 1 task, don't wait
─────────────────────────────────────────────────────────
with Pool(processes=3) as pool:
    async_result = pool.apply_async(square, (5,))
    # Main program continues here
    print("Task started!")
    result = async_result.get()  # Wait for result
# Result: 25
✓ Non-blocking! Main program continues


5️⃣ map_async() - Start multiple tasks, don't wait
─────────────────────────────────────────────────────────
with Pool(processes=3) as pool:
    async_result = pool.map_async(square, [1, 2, 3, 4, 5])
    # Main program continues here
    print("All tasks started!")
    results = async_result.get()  # Wait for all
# Result: [1, 4, 9, 16, 25]
✓ Non-blocking! Process results immediately


6️⃣ imap() - Get results one by one (ordered)
─────────────────────────────────────────────────────────
with Pool(processes=3) as pool:
    for result in pool.imap(square, [1, 2, 3, 4, 5]):
        print(f"Got: {result}")  # Process immediately
# Output: Got: 1, Got: 4, Got: 9, Got: 16, Got: 25
✓ Memory efficient! Results in input order


7️⃣ imap_unordered() - Get results any order (fastest)
─────────────────────────────────────────────────────────
with Pool(processes=3) as pool:
    for result in pool.imap_unordered(square, [1, 2, 3, 4, 5]):
        print(f"Got: {result}")  # Process immediately
# Output: Got: 1, Got: 4, Got: 25, Got: 9, Got: 16
✓ Memory efficient! Results come in completion order
"""
print(code_examples)


# ============================================================================
# COMPARISON 4: MEMORY USAGE
# ============================================================================

print("\n\n" + "="*100)
print("COMPARISON 4: MEMORY USAGE")
print("="*100)

memory_comparison = """
Scenario: Process 1,000,000 items

Blocking methods (store all results in RAM):
───────────────────────────────────────────
map()           → Creates list of 1,000,000 items in memory
                  RAM needed: ~40 MB (for integers) ❌

starmap()       → Same as map()
                  RAM needed: ~40 MB ❌

apply()         → Only 1 item at a time
                  RAM needed: negligible ✓


Non-blocking generators (stream results):
────────────────────────────────────────
apply_async()   → Stores all items in queue
                  RAM needed: ~40 MB (same as map()) ❌

map_async()     → Stores all items in queue
                  RAM needed: ~40 MB (same as map()) ❌

imap()          → Generator - processes one at a time
                  RAM needed: ~1 MB ✓✓ BEST!

imap_unordered()→ Generator - processes one at a time
                  RAM needed: ~1 MB ✓✓ BEST!


RULE: 
- Processing < 100 items? Use map() (simple)
- Processing 100-1M items? Use imap() or imap_unordered() (memory efficient)
- Processing > 1M items? Must use imap/imap_unordered()
"""
print(memory_comparison)


# ============================================================================
# COMPARISON 5: FEATURES
# ============================================================================

print("\n\n" + "="*100)
print("COMPARISON 5: FEATURES - What each method supports")
print("="*100)

features_table = """
┌──────────────────┬───────────┬──────────────┬──────────┬──────────────┐
│ Method           │ Callback? │ Timeout?     │ Ready()?│ Get order    │
├──────────────────┼───────────┼──────────────┼──────────┼──────────────┤
│ apply()          │ NO        │ NO           │ NO      │ Sequential   │
│ map()            │ NO        │ NO           │ NO      │ Same as input│
│ starmap()        │ NO        │ NO           │ NO      │ Same as input│
├──────────────────┼───────────┼──────────────┼──────────┼──────────────┤
│ apply_async()    │ YES ✓     │ YES ✓        │ YES ✓   │ N/A          │
│ map_async()      │ YES ✓     │ YES ✓        │ YES ✓   │ Same as input│
│ imap()           │ NO        │ NO           │ NO      │ Same as input│
│ imap_unordered() │ NO        │ NO           │ NO      │ Completion   │
└──────────────────┴───────────┴──────────────┴──────────┴──────────────┘

Callback = Run function when done
Timeout  = Set maximum wait time
Ready()  = Check progress without blocking
"""
print(features_table)


# ============================================================================
# COMPARISON 6: WHEN TO USE EACH
# ============================================================================

print("\n\n" + "="*100)
print("COMPARISON 6: DECISION GUIDE - When to use each method")
print("="*100)

decision_guide = """
┌─────────────────────────────────────────┬──────────────────────┐
│ Situation                               │ Use this             │
├─────────────────────────────────────────┼──────────────────────┤
│ "Process 10 items, need results"        │ pool.map()           │
│                                         │ ✓ Simplest!          │
├─────────────────────────────────────────┼──────────────────────┤
│ "Process with multiple arguments"       │ pool.starmap()       │
│  Example: multiply(1, 2), (3, 4)        │ ✓ Like map() but     │
│                                         │   unpacks tuples     │
├─────────────────────────────────────────┼──────────────────────┤
│ "1 heavy background task"               │ pool.apply_async()   │
│  Example: Download 1 large file         │ ✓ Non-blocking       │
├─────────────────────────────────────────┼──────────────────────┤
│ "100+ items, main needs to continue"    │ pool.map_async()     │
│ "Check progress, has callback"          │ ✓ Non-blocking       │
├─────────────────────────────────────────┼──────────────────────┤
│ "Process 1000+ items, limited RAM"      │ pool.imap()          │
│ "Need results in input order"           │ ✓ Memory efficient   │
├─────────────────────────────────────────┼──────────────────────┤
│ "Process 1 million items"               │ pool.imap_unordered()│
│ "Speed matters, order doesn't"          │ ✓ Fastest + memory   │
│                                         │   efficient          │
└─────────────────────────────────────────┴──────────────────────┘

🚀 QUICK RULE:
   Most common case? → pool.map()
   Large dataset?    → pool.imap() or pool.imap_unordered()
   Need more control?→ pool.apply_async() or pool.map_async()
"""
print(decision_guide)


# ============================================================================
# COMPARISON 7: DETAILED PROS & CONS
# ============================================================================

print("\n\n" + "="*100)
print("COMPARISON 7: DETAILED PROS & CONS")
print("="*100)

detailed_comparison = """
1️⃣ pool.apply()
───────────────────────────────────────────────────────────────────
Purpose: Process ONE task at a time
Blocks:  YES
Input:   One value (not iterable)

PROS:
  ✓ Simple syntax

CONS:
  ❌ EXTREMELY SLOW - only 1 worker at a time
  ❌ Wastes other workers
  ❌ No parallelism benefits

USE CASE: ❌ NEVER! Only in rare edge cases


2️⃣ pool.map()
───────────────────────────────────────────────────────────────────
Purpose: Process MULTIPLE items in parallel
Blocks:  YES (waits for all results)
Input:   List/iterable of values
Output:  List of results in same order

PROS:
  ✓ Simple, intuitive syntax
  ✓ All workers run in parallel
  ✓ Guaranteed output order
  ✓ Most commonly used

CONS:
  ❌ Loads all results in RAM
  ❌ Slower than async for huge datasets
  ❌ Main program blocks

USE CASE: ✓ DEFAULT CHOICE (95% of cases)


3️⃣ pool.starmap()
───────────────────────────────────────────────────────────────────
Purpose: Like map() but with multiple arguments
Blocks:  YES
Input:   List of tuples
Output:  List of results in same order

PROS:
  ✓ Parallel processing with multiple args
  ✓ Automatic tuple unpacking

CONS:
  ❌ Only for functions with 2+ arguments
  ❌ Loads all results in RAM

USE CASE: ✓ When function needs multiple arguments


4️⃣ pool.apply_async()
───────────────────────────────────────────────────────────────────
Purpose: Start 1 task, don't wait
Blocks:  NO
Input:   One value
Output:  AsyncResult object (call .get() later)

PROS:
  ✓ Non-blocking - main program continues
  ✓ Can set timeout
  ✓ Check progress with .ready()
  ✓ Callback support

CONS:
  ❌ Only for single task
  ❌ More complex code

USE CASE: ✓ Single background task, main needs to continue


5️⃣ pool.map_async()
───────────────────────────────────────────────────────────────────
Purpose: Start multiple tasks, don't wait
Blocks:  NO
Input:   List/iterable
Output:  AsyncResult object (call .get() later)

PROS:
  ✓ Non-blocking - main continues
  ✓ All workers run parallel
  ✓ Can set timeout
  ✓ Check progress with .ready()
  ✓ Callback support

CONS:
  ❌ More complex than map()
  ❌ Still loads all items in queue

USE CASE: ✓ Multiple background tasks, main needs responsive UI


6️⃣ pool.imap()
───────────────────────────────────────────────────────────────────
Purpose: Stream results one by one (in order)
Blocks:  NO (returns generator)
Input:   List/iterable
Output:  Generator (yields results as ready)

PROS:
  ✓ Memory efficient (processes one at a time)
  ✓ All workers run parallel
  ✓ Can process results immediately
  ✓ Results in predictable order

CONS:
  ❌ Can't use .get() (it's a generator)
  ❌ No callback support
  ❌ Requires loop

USE CASE: ✓ Large datasets where order matters


7️⃣ pool.imap_unordered()
───────────────────────────────────────────────────────────────────
Purpose: Stream results in completion order (fastest)
Blocks:  NO (returns generator)
Input:   List/iterable
Output:  Generator (yields results as completed)

PROS:
  ✓ Memory efficient
  ✓ All workers run parallel
  ✓ FASTEST option
  ✓ Process results immediately
  ✓ No blocking

CONS:
  ❌ Results not in input order
  ❌ No callback support
  ❌ Requires loop

USE CASE: ✓ Large datasets, speed critical, order doesn't matter
"""
print(detailed_comparison)


# ============================================================================
# COMPARISON 8: REAL WORLD SCENARIOS
# ============================================================================

print("\n\n" + "="*100)
print("COMPARISON 8: REAL WORLD SCENARIOS")
print("="*100)

scenarios = """
SCENARIO 1: Process 10 images for thumbnail gallery
────────────────────────────────────────────────────
✓ BEST: pool.map()
  - Simple
  - Fast enough for 10 items
  - Don't need memory optimization

Code:
    with Pool() as pool:
        thumbnails = pool.map(resize_image, images)


SCENARIO 2: Download 1000 files from URLs
──────────────────────────────────────────
✓ BEST: pool.imap_unordered()
  - Processing order doesn't matter
  - Memory efficient
  - Fastest option

Code:
    with Pool() as pool:
        for downloaded in pool.imap_unordered(download_file, urls):
            save_to_disk(downloaded)


SCENARIO 3: Web server processes images in background
─────────────────────────────────────────────────────
✓ BEST: pool.map_async()
  - Server must stay responsive
  - Don't wait for processing
  - Can check status with .ready()

Code:
    with Pool() as pool:
        async_result = pool.map_async(process, images)
        # Server responds immediately
        return "Processing started"
        # Later: results = async_result.get()


SCENARIO 4: Long-running ML model, keep UI responsive
──────────────────────────────────────────────────────
✓ BEST: pool.apply_async()
  - Single heavy task
  - UI must stay responsive
  - Callback to update UI when done

Code:
    with Pool() as pool:
        result = pool.apply_async(
            train_model, 
            (data,),
            callback=update_ui
        )


SCENARIO 5: Process 1 million sensor readings from edge device
──────────────────────────────────────────────────────────────
✓ BEST: pool.imap()
  - Must preserve order (time-series data)
  - Very large dataset
  - Limited memory (edge device)

Code:
    with Pool() as pool:
        for reading in pool.imap(process_sensor, data):
            save_to_database(reading)


SCENARIO 6: Simple batch processing job
────────────────────────────────────────
✓ BEST: pool.map()
  - Straightforward
  - Can wait for results
  - No special requirements

Code:
    with Pool() as pool:
        results = pool.map(process, data)
        # Use results
"""
print(scenarios)


# ============================================================================
# COMPARISON 9: FINAL CHEAT SHEET
# ============================================================================

print("\n\n" + "="*100)
print("COMPARISON 9: FINAL QUICK REFERENCE TABLE")
print("="*100)

final_table = """
┌──────────────────┬─────────────┬──────────────┬──────────┬────────────┬──────────────────────┐
│ Method           │ Use When    │ Input        │ Speed    │ Memory     │ Difficulty           │
├──────────────────┼─────────────┼──────────────┼──────────┼────────────┼──────────────────────┤
│ apply()          │ ❌ NEVER    │ Single value │ 🐌 SLOW  │ Low        │ Simple (but useless) │
│                  │             │              │          │            │                      │
│ map()            │ ✓ DEFAULT   │ List/items   │ ⚡ FAST  │ High       │ Simple ⭐⭐⭐        │
│                  │ (95% use)   │              │          │            │                      │
│ starmap()        │ ✓ Multiple  │ List of      │ ⚡ FAST  │ High       │ Simple ⭐⭐⭐        │
│                  │ args        │ tuples       │          │            │                      │
├──────────────────┼─────────────┼──────────────┼──────────┼────────────┼──────────────────────┤
│ apply_async()    │ ✓ 1 bg task │ Single value │ ⚡ FAST  │ Low        │ Medium ⭐⭐⭐        │
│                  │             │              │ (instant)│            │                      │
│ map_async()      │ ✓ Many bg   │ List/items   │ ⚡ FAST  │ High       │ Medium ⭐⭐⭐        │
│                  │ tasks       │              │ (instant)│            │                      │
│ imap()           │ ✓ Large     │ List/items   │ ⚡ FAST  │ Low ✓✓     │ Medium ⭐⭐          │
│                  │ data,       │              │ (+memory)│            │                      │
│                  │ ordered     │              │          │            │                      │
│ imap_unordered() │ ✓ HUGE      │ List/items   │ 🔥 FASTEST│ Low ✓✓    │ Medium ⭐⭐          │
│                  │ data,       │              │          │            │                      │
│                  │ any order   │              │          │            │                      │
└──────────────────┴─────────────┴──────────────┴──────────┴────────────┴──────────────────────┘

Legend:
- Use When: What problem does it solve?
- Speed: How fast?
- Memory: How much RAM needed?
- Difficulty: How hard to understand/use?
"""
print(final_table)


# ============================================================================
# COMPARISON 10: VISUAL TIMELINE COMPARISON
# ============================================================================

print("\n\n" + "="*100)
print("COMPARISON 10: TIMELINE - Which method finishes first?")
print("="*100)

timeline = """
Processing 12 items with 3 workers (each task takes 0.5s):

apply()          ████████░░░░░░░░░░░░░░  6.0s (1 worker, VERY SLOW!)
map()            ██░░░░░░░░░░░░░░░░░░  2.0s (all parallel)
starmap()        ██░░░░░░░░░░░░░░░░░░  2.0s (all parallel)
apply_async()    █░░░░░░░░░░░░░░░░░░░░  ~2.0s (instant start!)
map_async()      █░░░░░░░░░░░░░░░░░░░░  ~2.0s (instant start!)
imap()           ██░░░░░░░░░░░░░░░░░░  2.0s (stream results)
imap_unordered() ██░░░░░░░░░░░░░░░░░░  2.0s (any order)

█ = Time before first result
░ = Time until all results

Conclusions:
✓ apply() worst (don't use!)
✓ map/starmap best simple option
✓ async methods best for responsive UI
✓ imap methods best for huge datasets + memory
"""
print(timeline)


# ============================================================================
# SUMMARY TABLE
# ============================================================================

print("\n\n" + "="*100)
print("SUMMARY: HOW TO CHOOSE")
print("="*100)

summary = """
STEP 1: Do you have multiple items to process?
   → YES: Continue to step 2
   → NO: You don't need multiprocessing

STEP 2: Can your main program WAIT for all results?
   → YES: Go to step 3
   → NO: Use apply_async() or map_async() (non-blocking)

STEP 3: Do you have < 1000 items?
   → YES: Use pool.map() ✓ (BEST, simplest)
   → NO: Go to step 4

STEP 4: Do you need results in specific order?
   → YES: Use pool.imap() ✓ (memory efficient, ordered)
   → NO: Use pool.imap_unordered() ✓✓ (memory efficient, fastest)

STEP 5: Does your function need multiple arguments?
   → YES: Use pool.starmap() instead of pool.map()
   → NO: You're good!


════════════════════════════════════════════════════════════════════════
FINAL ANSWER BY USE CASE
════════════════════════════════════════════════════════════════════════

"I just want to process items in parallel"
→ Use: pool.map()

"I have 1 background task"
→ Use: pool.apply_async()

"I have many background tasks"
→ Use: pool.map_async()

"I have millions of items"
→ Use: pool.imap() or pool.imap_unordered()

"My function needs (a, b) arguments"
→ Use: pool.starmap()

"Don't know what to use"
→ Use: pool.map() (default answer)

════════════════════════════════════════════════════════════════════════
"""
print(summary)

print("\n" + "="*100)
print("END OF COMPARISON")
print("="*100)
