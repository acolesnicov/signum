from signum import sign

import os
import psutil
import time

def benchmark_and_leak_check():
    process = psutil.Process(os.getpid())

    # Test data
    test_cases = [
        ("Base (int)", lambda: sign(-5)),
        ("Base (float)", lambda: sign(-5.5)),
        ("Preprocess (str)", lambda: sign("15 men", preprocess=lambda s: (float(s.split()[0]),))),
        ("If_exc (error)", lambda: sign("error", if_exc=(0,)))
    ]

    print(f"{'Test Case':<20} | {'Time (s)':<10} | {'Memory (MB)':<12}")
    print("-" * 50)

    for name, func in test_cases:
        # Before
        start_mem = process.memory_info().rss / 1024 / 1024
        start_time = time.perf_counter()

        # Main loop (1 mln calls)
        for _ in range(1_000_000):
            func()

        # After
        end_time = time.perf_counter()
        end_mem = process.memory_info().rss / 1024 / 1024

        duration = end_time - start_time
        mem_diff = end_mem - start_mem

        print(f"{name:<20} | {duration:>9.4f} | {end_mem:>10.2f} ({mem_diff:+.2f})")

if __name__ == "__main__":
    for _ in range(1_000_000): # Warm up (get libraries)
        sign(1)
    benchmark_and_leak_check()
