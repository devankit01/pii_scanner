
# Pii Scanner


**PIIScanner** is a Python library designed for text processing using SpaCy and custom regex pattern matching. This library is capable of processing a variety of text data formats, such as lists, plain text, PDFs, JSON, CSV, and XLSX files.

## Features

- **Text Processing**: Process large texts by chunking them and applying SpaCy-based Named Entity Recognition (NER) and custom regex pattern matching.
- **Supported Formats**: Handle multiple data formats, including:
  - List of data
  - Plain text
  - PDFs
  - JSON
  - CSV
  - XLSX
- **Asynchronous**: Process multiple texts in parallel for faster analysis.
- **Region-Specific Matching**: Ability to apply region-specific regex patterns to enhance entity detection.
- **Pre-installed NLTK Datasets**: Automatically downloads and uses required NLTK datasets like `punkt` and `stopwords` to improve text processing.

## Requirements

- **Python**: >= 3.10
- **SpaCy**: `>=3.0`
- **NLTK**: `>=3.6`
- **Presidio**: `>=1.0` 

### Installation

To install **SpacyMatchScanner**, use `pip`:

```bash
pip install pii-scanner
```

### Install NLTK Datasets

The library automatically installs required NLTK datasets (`punkt` and `stopwords`) during initialization. If you face any issues with this, ensure you have an active internet connection to download the datasets.

### Usage

```python
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
```

### Supported Data Formats

1. **Plain Text**: You can pass raw text directly to the `scan_async` method for processing.
2. **PDF**: The library can extract text from PDF files and then process them.
3. **JSON**: Process JSON objects containing text data.
4. **CSV**: Process CSV files and extract text data for analysis.
5. **XLSX**: Process Excel files (XLSX format) containing text data.



### License

This library is open source and available under the MIT License. See the [LICENSE](LICENSE) file for more information.

### Version History

- **v0.1.7**: Initial release with support for text chunking, NER, and batch processing for text, PDFs, JSON, CSV, and XLSX files.
- **v0.1.6**: Added support for custom region-specific patterns and async processing.

