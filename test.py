import asyncio
import time
from pii_scanner.scanner import PIIScanner
from pii_scanner.constants.patterns_countries import Regions

async def run_scan():
    # Start the timer
    start_time = time.time()

    pii_scanner = PIIScanner()
    # file_path = 'dummy-pii/test.json' 
    # file_path = 'dummy-pii/test.xlsx' 
    file_path = 'dummy-pii/test.pdf' 
    results_async = await pii_scanner.scan(file_path=file_path, sample_size=0.005, region=Regions.IN)
    
    # End the timer
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time taken for asynchronous scan: {total_time:.4f} seconds")
    print("Asynchronous Results:", results_async)

# Run the asynchronous scan
asyncio.run(run_scan())
