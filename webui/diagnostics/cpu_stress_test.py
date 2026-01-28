"""
CPU Stress Test - Load test for CPU stability
"""
import psutil
import time
import multiprocessing
from datetime import datetime


def stress_cpu_core(duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        _ = sum(i * i for i in range(10000))


def run() -> str:
    output = []
    output.append("=" * 60)
    output.append("CPU STRESS TEST")
    output.append("=" * 60)
    output.append("")
    
    output.append("--- Pre-Test CPU State ---")
    cpu_count = psutil.cpu_count(logical=True)
    output.append(f"Logical CPU cores: {cpu_count}")
    
    initial_cpu = psutil.cpu_percent(interval=1)
    output.append(f"Initial CPU usage: {initial_cpu}%")
    
    output.append("")
    output.append("--- Running 10-second Stress Test ---")
    output.append(f"Stressing {cpu_count} cores...")
    output.append("")
    
    start_time = time.time()
    processes = []
    samples = []
    
    try:
        for i in range(cpu_count):
            p = multiprocessing.Process(target=stress_cpu_core, args=(10,))
            p.start()
            processes.append(p)
        
        for _ in range(10):
            time.sleep(1)
            cpu_usage = psutil.cpu_percent(interval=0.1)
            samples.append(cpu_usage)
            elapsed = int(time.time() - start_time)
            output.append(f"  {elapsed}s: CPU usage {cpu_usage}%")
        
        for p in processes:
            p.join()
        
        output.append("")
        output.append("--- Test Results ---")
        if samples:
            output.append(f"Average CPU usage: {sum(samples)/len(samples):.1f}%")
            output.append(f"Peak CPU usage: {max(samples):.1f}%")
            output.append(f"Minimum CPU usage: {min(samples):.1f}%")
            
            avg_usage = sum(samples) / len(samples)
            if avg_usage > 80:
                output.append("STATUS: PASS - CPU stress test completed successfully")
            else:
                output.append("STATUS: WARNING - CPU did not reach expected load")
        
    except Exception as e:
        output.append(f"Error during stress test: {e}")
        for p in processes:
            if p.is_alive():
                p.terminate()
    
    output.append("")
    output.append("=" * 60)
    output.append(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 60)
    
    return "\n".join(output)
