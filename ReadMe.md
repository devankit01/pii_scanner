
# Pii Scanner Library - v0.1.7

[![Version](https://img.shields.io/github/v/release/yourusername/spacy-match-scanner)](https://github.com/yourusername/spacy-match-scanner/releases)
[![Python Version](https://img.shields.io/pypi/pyversions/spacy-match-scanner)](https://pypi.org/project/spacy-match-scanner/)
[![License](https://img.shields.io/github/license/yourusername/spacy-match-scanner)](https://github.com/yourusername/spacy-match-scanner/blob/main/LICENSE)

**SpacyMatchScanner** is a Python library designed for efficient text processing using SpaCy and custom regex pattern matching. This library is capable of processing a variety of text data formats, such as lists, plain text, PDFs, JSON, CSV, and XLSX files. It provides a streamlined API for extracting entities and patterns from large-scale text data asynchronously.

## Features

- **Text Processing**: Process large texts by chunking them and applying SpaCy-based Named Entity Recognition (NER) and custom regex pattern matching.
- **Supported Formats**: Handle multiple data formats, including:
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
- **Presidio**: `>=1.0` (Optional, if used for Presidio-based analysis)

### Installation

To install **SpacyMatchScanner**, use `pip`:

```bash
pip install spacy-match-scanner
```

### Install NLTK Datasets

The library automatically installs required NLTK datasets (`punkt` and `stopwords`) during initialization. If you face any issues with this, ensure you have an active internet connection to download the datasets.

### Usage

```python
from spacy_match_scanner import SpacyMatchScanner

# Initialize the scanner
scanner = SpacyMatchScanner()

# Example: Process a single large text
text = "Your large document or text content here."
region = "US"  # Specify region for pattern matching (optional)
results = await scanner.scan_async(text, region)

# Example: Process a batch of texts
texts = ["Text 1", "Text 2", "Text 3"]
batch_results = await scanner.scan_batch_async(texts, region)
```

### Supported Data Formats

1. **Plain Text**: You can pass raw text directly to the `scan_async` method for processing.
2. **PDF**: The library can extract text from PDF files and then process them.
3. **JSON**: Process JSON objects containing text data.
4. **CSV**: Process CSV files and extract text data for analysis.
5. **XLSX**: Process Excel files (XLSX format) containing text data.

For these formats, you can use the following functions:
```python
from spacy_match_scanner import SpacyMatchScanner
import pandas as pd
import json
from PyPDF2 import PdfReader

# Example: Process a JSON file
with open("data.json", "r") as file:
    json_data = json.load(file)
    scanner.scan_async(json_data["text"], region="US")

# Example: Process a CSV file
csv_data = pd.read_csv("data.csv")
for index, row in csv_data.iterrows():
    scanner.scan_async(row["text"], region="US")

# Example: Process a PDF file
reader = PdfReader("file.pdf")
pdf_text = ""
for page in reader.pages:
    pdf_text += page.extract_text()
scanner.scan_async(pdf_text, region="US")
```

### Key Methods

- **`scan_async(data: str, region: str)`**: Asynchronously processes a large text, applying SpaCy-based NER and custom regex pattern matching.
- **`scan_batch_async(data_batch: List[str], region: str)`**: Asynchronously processes a batch of texts (e.g., from a CSV, JSON, or XLSX file) in parallel.
- **`_chunk_text(text: str, chunk_size: int)`**: Splits large texts into smaller chunks for parallel processing.
- **`_initialize()`**: Initializes the SpaCy model and regex matcher.

### Example Use Cases

- **Entity Recognition**: Extract sensitive information such as names, emails, phone numbers, etc., from large documents, PDFs, or CSV files.
- **Pattern Matching**: Match custom patterns from various data sources using predefined regex patterns.
- **Batch Processing**: Efficiently handle large datasets (e.g., multiple documents, CSV, or JSON files) asynchronously.

### License

This library is open source and available under the MIT License. See the [LICENSE](LICENSE) file for more information.

### Version History

- **v0.1.7**: Initial release with support for text chunking, NER, and batch processing for text, PDFs, JSON, CSV, and XLSX files.
- **v0.1.6**: Added support for custom region-specific patterns and async processing.

