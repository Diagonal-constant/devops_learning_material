"""
QUICK CHEAT SHEET - Python Multiprocessing Pool
================================================

GOLDEN RULE: Use pool.map() 95% of the time!
"""

import multiprocessing as mp
from multiprocessing import Pool

# ============================================================================
# YOUR FUNCTION TO RUN IN PARALLEL
# ============================================================================

def process_item(item):
    """Any function you want to run in parallel"""
    return item * 2


# ============================================================================
# BLOCKING METHODS (Wait for results)
# ============================================================================

if __name__ == '__main__':
    
    # ▶ USE THIS 95% OF THE TIME
    print("\n1. pool.map() - Simple, works great")
    print("-" * 50)
    with Pool(processes=4) as pool:
        items = [1, 2, 3, 4, 5]
        results = pool.map(process_item, items)  # BLOCKS until done
        print(f"Results: {results}")
    # When: You have multiple items, need all results, can wait


if __name__ == '__main__':
    # ▶ USE THIS when function has multiple arguments
    print("\n2. pool.starmap() - Multiple arguments")
    print("-" * 50)
    
    def multiply(a, b):
        return a * b
    
    with Pool(processes=2) as pool:
        pairs = [(2, 3), (4, 5)]
        results = pool.starmap(multiply, pairs)  # Unpacks tuples
        print(f"Results: {results}")
    # When: Function needs (a, b) or (x, y, z) instead of single value


# ============================================================================
# NON-BLOCKING METHODS (Don't wait, get results later)
# ============================================================================

if __name__ == '__main__':
    # ▶ USE THIS for memory-efficient processing
    print("\n3. pool.imap() - Get results one by one")
    print("-" * 50)
    with Pool(processes=3) as pool:
        items = [100, 200, 300, 400, 500]
        # Returns generator - doesn't load all results into memory
        for result in pool.imap(process_item, items):
            print(f"Got: {result}")  # Process as results come in
    # When: Processing millions of items, limited RAM, need results instantly


if __name__ == '__main__':
    # ▶ USE THIS when order doesn't matter (fastest)
    print("\n4. pool.imap_unordered() - Get results in any order")
    print("-" * 50)
    with Pool(processes=3) as pool:
        items = [10, 20, 30, 40, 50]
        for result in pool.imap_unordered(process_item, items):
            print(f"Got: {result}")  # Results come in completion order
    # When: Large datasets, speed matters, results order doesn't matter


# ============================================================================
# AVOID THESE
# ============================================================================

if __name__ == '__main__':
    # ✗ DON'T USE - Only 1 worker at a time!
    print("\n❌ AVOID: pool.apply()")
    print("-" * 50)
    with Pool(processes=3) as pool:
        # This uses only 1 worker. Very slow!
        result = pool.apply(process_item, (100,))
    # Never use this unless you have a weird edge case


if __name__ == '__main__':
    # ⚠️ Rarely needed - More complicated
    print("\n⚠️ SOMETIMES USE: pool.apply_async()")
    print("-" * 50)
    with Pool(processes=2) as pool:
        # Start task, don't wait
        async_result = pool.apply_async(process_item, (999,))
        print("Task started, doing other stuff...")
        # ... do other work ...
        result = async_result.get()  # Now wait for result
        print(f"Got: {result}")
    # Only use for special cases where you need more control


# ============================================================================
# QUICK DECISION TABLE
# ============================================================================

DECISION_TABLE = """
What do you need?              │ Use this          │ Example
───────────────────────────────┼──────────────────┼─────────────────────────────
Process list, need all results │ pool.map()        │ results = pool.map(f, items)
Process list, order doesn't    │ pool.imap_        │ for r in pool.imap_unordered():
matter, memory limited         │ unordered()       │   process(r)
Process list, get results as   │ pool.imap()       │ for r in pool.imap(f, items):
they come, keep order          │                   │   process(r)
Multiple arguments per call    │ pool.starmap()    │ pool.starmap(f, [(1,2),(3,4)])
Need more control              │ pool.apply_async()│ result = pool.apply_async(f)
───────────────────────────────┴──────────────────┴─────────────────────────────
"""

print(DECISION_TABLE)


# ============================================================================
# REAL WORLD: IMAGE PROCESSING
# ============================================================================

def resize_image(image_path):
    """Simulate resizing an image for computer vision"""
    # In real code: load image, resize, save
    import time
    time.sleep(1)  # Simulate processing
    return f"✓ {image_path}"


if __name__ == '__main__':
    print("\n\n" + "="*60)
    print("REAL WORLD: Process 10 images in parallel")
    print("="*60)
    
    images = [f"photo_{i}.jpg" for i in range(10)]
    
    print("\n❌ WITHOUT MULTIPROCESSING (10 seconds):")
    import time
    start = time.time()
    for img in images:
        result = resize_image(img)
    print(f"Took: {time.time() - start:.1f}s")
    
    print("\n✓ WITH pool.map() (3-4 seconds with 3 workers):")
    start = time.time()
    with Pool(processes=3) as pool:
        results = pool.map(resize_image, images)
    print(f"Took: {time.time() - start:.1f}s")
    print(f"Results: {results[:3]}...")  # Show first 3


# ============================================================================
# THINGS TO REMEMBER
# ============================================================================

TIPS = """
💡 THINGS TO REMEMBER:

1. Function must be at module level (not inside another function)
   ✓ Good:   def my_func(): ...
   ✗ Bad:    def outer():
                def my_func(): ...   # Won't work in multiprocessing!

2. Use 'with Pool()' - automatically closes workers

3. Number of processes = Your CPU cores
   Usually: processes = os.cpu_count() or 4 for testing

4. Results are ALWAYS a list or generator (never a single value)
   results = pool.map(func, [1, 2, 3])  # Returns [r1, r2, r3]

5. Pool is slow for very fast functions (overhead isn't worth it)
   Don't parallelize: func that runs in <0.01 seconds

6. Each worker has its own memory (no shared state)
   Workers can't modify a shared variable

7. Pickling: Function + arguments must be serializable (most are)
   Avoid: lambda, local functions, complex objects

8. Timeout: pool.map_async().get(timeout=30)  # Wait max 30s
"""

print(TIPS)
