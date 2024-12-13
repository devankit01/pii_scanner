import os
import asyncio
from pii_scanner.scanners.ner_scanner import SpacyNERScanner
from pii_scanner.file_readers.csv_reader import csv_file_pii_detector
from pii_scanner.file_readers.json_reader import json_file_pii_detector
from pii_scanner.file_readers.xlsx_reader import xlsx_file_pii_detector
from pii_scanner.file_readers.doc_reader import doc_pii_detector

class PIIScanner:
    def __init__(self):
        self.spacy_ner_scanner = SpacyNERScanner()  # Initialize NER Scanner for column data scanning

    async def scan(self, file_path: str = None, data: list = None, sample_size = None, region: str = None):
        """
        Asynchronous method to scan data or file for PII.
        """
        if data is not None:
            print("Scanning provided data for PII asynchronously...")
            return await self.spacy_ner_scanner.scan(data, sample_size, region)
        elif file_path:
            print(f"Scanning file asynchronously: {file_path}")
            return await self.files_data_pii_scanner_async(file_path, sample_size, region)
        else:
            print("No data or file path provided for scanning.")
            return None



    # Placeholder for file processing methods
    async def files_data_pii_scanner_async(self, file_path: str, sample_size: float | None,  region: str):
        """
        Asynchronous method to process file data for PII.
        """
        print(f"Processing file: {file_path}")
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.csv':
            result = await csv_file_pii_detector(file_path, sample_size=sample_size, region=region )
            
        elif file_extension == '.json':
            result = await json_file_pii_detector(file_path=file_path, sample_size=sample_size, region=region)
            
        elif file_extension == '.xlsx':
            sheet_name = None
            result = await xlsx_file_pii_detector(file_path, sheet_name, sample_size=sample_size, region=region)
        
        elif file_extension in ['.txt', '.pdf', '.docx']:
            result = await doc_pii_detector(file_path, region=region)
            print("Text/PDF/Docx File PII Scanner Results:")
        return result

