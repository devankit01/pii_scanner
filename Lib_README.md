# PII Scanner

A Python library designed for text processing using SpaCy and custom regex pattern matching. This library is capable of processing a variety of text data formats, such as lists, plain text, PDFs, JSON, CSV, and XLSX files

## Installation

```bash
pip install pii_scanner
```

## Usage 

```bash
import asyncio
from pii_scanner.scanner import PIIScanner
from pii_scanner.constants.patterns_countries import Regions

async def run_scan():
    # Start the timer
    start_time = time.time()

    pii_scanner = PIIScanner()
    # file_path = 'dummy-pii/test.json' 
    file_path = 'dummy-pii/test.xlsx' 

    data = ['Ankit Gupta', '+919140562125', 'Indian']
    results_list_data = await pii_scanner.scan(data=, sample_size=0.005, region=Regions.IN)
    # results_file_data = await pii_scanner.scan(file_path=file_path, sample_size=0.005, region=Regions.IN)

    print("Results:", results_list_data, results_list_data)

# Run the asynchronous scan
asyncio.run(run_scan())


```


## Output 

```bash
[
    {
        "text": "Ankit Gupta",
        "entity_detected": [
            {"type": "PERSON", "start": 0, "end": 11, "score": 0.85}
        ]
    },
    {
        "text": "+919140562195",
        "entity_detected": [
            {"type": "PHONE_NUMBER", "start": 0, "end": 13, "score": 0.85}
        ]
    },
    {
        "text": "Indian",
        "entity_detected": [
            {"type": "NATIONALITY", "start": 0, "end": 6, "score": 0.9}
        ]
    }
]


```


