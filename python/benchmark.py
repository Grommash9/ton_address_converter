# pip install pytoniq-core tonsdk ton_address_converter
# python python/benchmark.py

import time
import random
from typing import List, Callable
import ton_address_converter
from pytoniq_core import Address  # pip install pytoniq-core
from tonsdk.utils import Address as TonSdkAddress 

def generate_test_addresses(n: int) -> List[str]:
    # Example raw address template
    template = "0:73f17af370bd9d1f754be87a8a2d46f178aa72a9fc26f8ed9305977313f5dd29"
    addresses = []
    for _ in range(n):
        # Modify last few characters to create variation
        mod_addr = template[:-8] + ''.join(random.choices('0123456789abcdef', k=8))
        addresses.append(mod_addr)
    return addresses

def benchmark_ton_address_converter(addresses: List[str]) -> float:
    start_time = time.time()
    ton_address_converter.batch_convert_to_friendly(addresses, chunk_size=1000)
    return time.time() - start_time

def benchmark_pytoniq(addresses: List[str]) -> float:
    start_time = time.time()
    for addr in addresses:
        Address(addr).to_str(is_user_friendly=True)
    return time.time() - start_time

def benchmark_tonsdk(addresses: List[str]) -> float:
    start_time = time.time()
    for addr in addresses:
        TonSdkAddress(addr).to_string()
    return time.time() - start_time

def run_benchmarks(sizes: List[int] = [100, 1000, 10000, 100000]):
    results = []
    
    for size in sizes:
        print(f"\nBenchmarking with {size} addresses:")
        addresses = generate_test_addresses(size)
        
        # Run each benchmark
        ton_time = benchmark_ton_address_converter(addresses)
        pytoniq_time = benchmark_pytoniq(addresses)
        tonsdk_time = benchmark_tonsdk(addresses)
        
        results.append({
            'size': size,
            'ton_address_converter': ton_time,
            'pytoniq': pytoniq_time,
            'tonsdk': tonsdk_time,
            'speedup_vs_pytoniq': pytoniq_time / ton_time,
            'speedup_vs_tonsdk': tonsdk_time / ton_time
        })
        
        print(f"ton_address_converter: {ton_time:.4f}s")
        print(f"pytoniq: {pytoniq_time:.4f}s")
        print(f"tonsdk: {tonsdk_time:.4f}s")
        print(f"Speedup vs pytoniq: {pytoniq_time/ton_time:.2f}x")
        print(f"Speedup vs tonsdk: {tonsdk_time/ton_time:.2f}x")
    
    return results

if __name__ == "__main__":
    run_benchmarks()