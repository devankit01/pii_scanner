import time
import logging
import random
import asyncio
import spacy
from spacy.matcher import Matcher
from typing import Dict, List, Union
from pii_scanner.regex_patterns.matcher_patterns import patterns
from pii_scanner.check_digit_warehouse.validate_entity_type import validate_entity_check_digit


logger = logging.getLogger(__name__)

class SpacyMatchScanner:
    """
    SpacyMatch Scanner using Presidio's AnalyzerEngine with SpaCy
    """

    SPACY_EN_MODEL = "en_core_web_lg"

    def __init__(self):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize variables for lazy loading
        self.matcher = None
        self.nlp_engine = None
        self.initialized = False
        self.region = None

    def _initialize(self):
        """Lazy initialization of the SpaCy model and Matcher."""
        if not self.initialized:
            try:
                self.nlp_engine = spacy.load(self.SPACY_EN_MODEL)
            except OSError:
                self.logger.warning("Downloading en_core_web_lg language model for SpaCy")
                from spacy.cli import download
                download(self.SPACY_EN_MODEL)
                self.nlp_engine = spacy.load(self.SPACY_EN_MODEL)

            # Create matcher and add patterns once
            self.matcher = Matcher(self.nlp_engine.vocab)

            global_patterns = patterns.get("GLOBAL", {})
            region_patterns = patterns.get(self.region, {})

            # Combine pattern dictionaries
            combined_patterns = {**global_patterns, **region_patterns}
            for label, pattern in combined_patterns.items():
                self.matcher.add(label, [[{"TEXT": {"regex": pattern}}]])

            self.initialized = True

    def _chunk_text(self, text: str, chunk_size: int = 512) -> List[str]:
        """
        Split the text into chunks for processing.
        Each chunk will be a substring with a max size of chunk_size.
        """
        words = text.split()
        chunks = []
        chunk = []

        for word in words:
            if len(" ".join(chunk) + " " + word) <= chunk_size:
                chunk.append(word)
            else:
                chunks.append(" ".join(chunk))
                chunk = [word]

        if chunk:
            chunks.append(" ".join(chunk))
        return chunks

    async def _scan_text_async(self, data: str) -> List[Dict[str, Union[str, List[Dict[str, str]]]]]:
        """Asynchronously process a single text chunk using SpaCy and Matcher."""
        self._initialize()
        doc = self.nlp_engine(data)

        matched_patterns = []

        # Apply SpaCy NER detection asynchronously
        for ent in doc.ents:
            matched_patterns.append({
                'text': ent.text,
                'entity_detected': [{
                    'type': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char,
                    'score': 0.95  # Using a fixed score for demo
                }]
            })

        # Apply custom regex patterns using the pre-configured matcher asynchronously
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            pattern_id = self.nlp_engine.vocab.strings[match_id]
            entity = doc[start:end].text

            # For demo purposes, using a random score
            score = random.uniform(0.8, 1.0)

            matched_patterns.append({
                'text': entity,
                'entity_detected': [{
                    'type': pattern_id,
                    'start': start,
                    'end': end,
                    'score': score
                }]
            })

        return matched_patterns

    async def scan_async(self, data: str, region: str) -> List[Dict[str, Union[str, List[Dict[str, str]]]]]:
        """
        Asynchronously process a large text by splitting it into chunks and processing each chunk in parallel.
        """
        self.region = region
        start_time = time.time()

        # Chunk the large text into smaller chunks
        text_chunks = self._chunk_text(data)

        # Process each text chunk asynchronously in parallel
        tasks = [self._scan_text_async(chunk) for chunk in text_chunks]
        chunk_results = await asyncio.gather(*tasks)

        # Combine the results from all chunks
        final_results = [item for sublist in chunk_results for item in sublist]
        
        for entity in final_results:
            
            analyzer_result = entity.get("entity_detected", [])
            text = entity.get("text", [])
            
            if analyzer_result and len(analyzer_result):
                analyzer_result = analyzer_result[0]
                entity_type = analyzer_result.get("type")
                entity_text = text
                
                # Call validate_entity_check_digit function and get result
                validation_result = await validate_entity_check_digit(text, entity_type, self.region.value)
                
                # Create the updated 'entity_detected' dictionary
                updated_entity_detected = {
                    "type": entity_type,  # This will be 'PERSON' or another type, based on the entity_type
                    "text": entity_text
                }
                
                # Update the dictionary with validation result
                if validation_result.get("check_digit"):
                    entity["validated"] = {
                        "entity_detected": [updated_entity_detected],
                        "check_digit": True
                    }
                else:
                    entity["validated"] = {
                        "entity_detected": [updated_entity_detected],
                        "check_digit": False
                    }

        end_time = time.time()
        processing_time = end_time - start_time
        self.logger.info(f"Processing completed in {processing_time:.2f} seconds.")

        return final_results
