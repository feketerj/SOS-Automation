"""
Document Fetcher for Multi-Stage Pipeline
Fetches and aggregates documents from HigherGov API with proper timeouts and retries
"""

import requests
import json
import logging
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import hardcoded configuration
from pipeline_config import get_api_key, get_endpoint, RATE_LIMITS

logger = logging.getLogger(__name__)


class DocumentFetcher:
    """Fetches documents and metadata from HigherGov API"""

    def __init__(self):
        """Initialize with hardcoded HigherGov API key"""
        self.api_key = get_api_key("highergov")
        self.base_url = get_endpoint("highergov", "base_url")
        self.last_api_call = 0

        # NO TIMEOUTS - Document fetching takes a LONG time
        self.DOCUMENT_TIMEOUT = None  # No timeout, let it run as long as needed
        self.MAX_RETRIES = 10  # Many more retries for reliability
        self.RETRY_DELAYS = [2, 3, 5, 8, 10, 15, 20, 30, 45, 60]  # Progressive backoff up to 1 minute

        # MUCH LARGER document size limits to match production
        self.MAX_DOCUMENT_LENGTH = 2000000  # 2M characters total (was 500K)
        self.MAX_SINGLE_DOC = 500000  # 500K per document (was 200K)

    def fetch_opportunity_with_documents(self, search_id: str) -> Dict[str, Any]:
        """
        Fetch opportunity metadata and all associated documents
        ALWAYS attempts to fetch documents if they exist
        """
        logger.info(f"Fetching opportunity and documents for: {search_id}")

        result = {
            "search_id": search_id,
            "metadata": {},
            "documents": [],
            "combined_text": "",
            "fetch_status": "pending",
            "errors": []
        }

        try:
            # Step 1: Fetch opportunity metadata
            metadata = self._fetch_opportunity_metadata(search_id)
            if metadata:
                result["metadata"] = metadata
                logger.info(f"Fetched metadata for {search_id}: {metadata.get('title', 'No title')[:100]}")
            else:
                result["errors"].append("Failed to fetch opportunity metadata")
                result["fetch_status"] = "metadata_failed"
                return result

            # Step 2: ALWAYS try to fetch documents if available
            documents = self._fetch_all_documents(metadata)
            if documents:
                result["documents"] = documents
                logger.info(f"Fetched {len(documents)} documents totaling {sum(len(d.get('text', '')) for d in documents)} characters")
            else:
                logger.warning(f"No documents fetched for {search_id}")

            # Step 3: Combine all text for processing
            result["combined_text"] = self._combine_texts(metadata, documents)
            result["fetch_status"] = "complete"

        except Exception as e:
            logger.error(f"Error fetching opportunity {search_id}: {e}")
            result["errors"].append(str(e))
            result["fetch_status"] = "error"

        return result

    def _fetch_opportunity_metadata(self, search_id: str) -> Optional[Dict]:
        """Fetch opportunity metadata from HigherGov API with retries"""
        url = f"{self.base_url}/api-external/opportunity/"
        params = {"search": search_id}
        headers = {"Authorization": f"Api-Key {self.api_key}"}

        for attempt in range(self.MAX_RETRIES):
            try:
                # Rate limiting
                self._apply_rate_limit()

                logger.info(f"Fetching metadata attempt {attempt + 1}/{self.MAX_RETRIES} (no timeout)")
                response = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=self.DOCUMENT_TIMEOUT  # None = no timeout
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("results"):
                        return data["results"][0]
                    else:
                        logger.warning(f"No results found for search_id: {search_id}")
                        return None

                elif response.status_code == 429:  # Rate limited
                    wait_time = self.RETRY_DELAYS[min(attempt, len(self.RETRY_DELAYS)-1)]
                    logger.warning(f"Rate limited, waiting {wait_time} seconds")
                    time.sleep(wait_time)
                    continue

                else:
                    logger.error(f"API error {response.status_code}: {response.text}")

            except requests.Timeout:
                wait_time = self.RETRY_DELAYS[min(attempt, len(self.RETRY_DELAYS)-1)]
                logger.warning(f"Timeout on attempt {attempt + 1}, waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            except Exception as e:
                logger.error(f"Error fetching metadata: {e}")
                if attempt < self.MAX_RETRIES - 1:
                    wait_time = self.RETRY_DELAYS[min(attempt, len(self.RETRY_DELAYS)-1)]
                    time.sleep(wait_time)

        logger.error(f"Failed to fetch metadata after {self.MAX_RETRIES} attempts")
        return None

    def _fetch_all_documents(self, metadata: Dict) -> List[Dict]:
        """
        Fetch ALL documents associated with an opportunity
        Uses multiple methods to ensure documents are retrieved
        """
        documents = []

        # Method 1: Use source_id_version as related_key (most reliable)
        if metadata.get("source_id_version"):
            docs = self._fetch_documents_by_related_key(metadata["source_id_version"])
            if docs:
                documents.extend(docs)
                logger.info(f"Fetched {len(docs)} documents using source_id_version")

        # Method 2: Try document_path if available
        if metadata.get("document_path") and not documents:
            docs = self._fetch_documents_by_related_key(metadata["document_path"])
            if docs:
                documents.extend(docs)
                logger.info(f"Fetched {len(docs)} documents using document_path")

        # Method 3: Try using ID directly if no documents yet
        if metadata.get("id") and not documents:
            docs = self._fetch_documents_by_related_key(str(metadata["id"]))
            if docs:
                documents.extend(docs)
                logger.info(f"Fetched {len(docs)} documents using opportunity ID")

        # Method 4: Include inline text from metadata if substantial
        if not documents:
            # Use description_text and ai_summary as fallback
            inline_doc = {}

            if metadata.get("description_text"):
                inline_doc["description_text"] = metadata["description_text"]

            if metadata.get("ai_summary"):
                inline_doc["ai_summary"] = metadata["ai_summary"]

            if metadata.get("naics_description"):
                inline_doc["naics_description"] = metadata["naics_description"]

            if inline_doc:
                inline_doc["source"] = "metadata_inline"
                inline_doc["text"] = " ".join(inline_doc.values())
                documents.append(inline_doc)
                logger.info(f"Using inline metadata text ({len(inline_doc['text'])} chars)")

        return documents

    def _fetch_documents_by_related_key(self, related_key: str) -> List[Dict]:
        """Fetch documents using related_key parameter"""
        url = f"{self.base_url}/api-external/document/"
        params = {"related_key": related_key}
        headers = {"Authorization": f"Api-Key {self.api_key}"}

        for attempt in range(self.MAX_RETRIES):
            try:
                # Rate limiting
                self._apply_rate_limit()

                logger.info(f"Fetching documents with related_key={related_key}, attempt {attempt + 1} (no timeout)")
                response = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=self.DOCUMENT_TIMEOUT  # None = no timeout
                )

                if response.status_code == 200:
                    data = response.json()
                    documents = []

                    if data.get("results"):
                        for doc in data["results"]:
                            # Extract text from various fields
                            doc_text = ""

                            # Primary text source
                            if doc.get("text_extract"):
                                doc_text = doc["text_extract"]

                            # Fallback to other text fields
                            elif doc.get("content"):
                                doc_text = doc["content"]
                            elif doc.get("text"):
                                doc_text = doc["text"]

                            if doc_text:
                                # Truncate if too long
                                if len(doc_text) > self.MAX_SINGLE_DOC:
                                    doc_text = doc_text[:self.MAX_SINGLE_DOC]
                                    logger.warning(f"Truncated document from {len(doc_text)} to {self.MAX_SINGLE_DOC} chars")

                                documents.append({
                                    "file_name": doc.get("file_name", "unknown"),
                                    "file_type": doc.get("file_type", "unknown"),
                                    "file_size": doc.get("file_size", 0),
                                    "text": doc_text,
                                    "download_url": doc.get("download_url", ""),
                                    "source": "document_api"
                                })

                    return documents

                elif response.status_code == 429:
                    wait_time = self.RETRY_DELAYS[min(attempt, len(self.RETRY_DELAYS)-1)]
                    logger.warning(f"Rate limited, waiting {wait_time} seconds")
                    time.sleep(wait_time)
                    continue

                elif response.status_code == 404:
                    logger.info(f"No documents found for related_key: {related_key}")
                    return []

                else:
                    logger.warning(f"Document API error {response.status_code}")

            except requests.Timeout:
                wait_time = self.RETRY_DELAYS[min(attempt, len(self.RETRY_DELAYS)-1)]
                logger.warning(f"Document fetch timeout on attempt {attempt + 1}, waiting {wait_time}s")
                time.sleep(wait_time)
            except Exception as e:
                logger.error(f"Error fetching documents: {e}")
                if attempt < self.MAX_RETRIES - 1:
                    wait_time = self.RETRY_DELAYS[min(attempt, len(self.RETRY_DELAYS)-1)]
                    time.sleep(wait_time)

        return []

    def _combine_texts(self, metadata: Dict, documents: List[Dict]) -> str:
        """
        Combine metadata and document texts into a single string
        Preserves all available information for pipeline processing
        """
        combined_parts = []

        # Add metadata header
        combined_parts.append("=== OPPORTUNITY METADATA ===")
        combined_parts.append(f"Title: {metadata.get('title', 'N/A')}")
        combined_parts.append(f"Agency: {metadata.get('agency', 'N/A')}")
        combined_parts.append(f"Office: {metadata.get('office', 'N/A')}")
        combined_parts.append(f"Type: {metadata.get('type', 'N/A')}")
        combined_parts.append(f"Set-Aside: {metadata.get('type_of_set_aside', 'N/A')}")
        combined_parts.append(f"NAICS: {metadata.get('naics', 'N/A')}")
        combined_parts.append(f"Response Date: {metadata.get('response_date_time', 'N/A')}")
        combined_parts.append(f"Posted Date: {metadata.get('posted_date', 'N/A')}")

        # Add description
        if metadata.get("description_text"):
            combined_parts.append("\n=== DESCRIPTION ===")
            combined_parts.append(metadata["description_text"])

        # Add AI summary if available
        if metadata.get("ai_summary"):
            combined_parts.append("\n=== AI SUMMARY ===")
            combined_parts.append(metadata["ai_summary"])

        # Add all document texts
        if documents:
            combined_parts.append("\n=== DOCUMENTS ===")
            for i, doc in enumerate(documents, 1):
                if doc.get("text"):
                    combined_parts.append(f"\n--- Document {i}: {doc.get('file_name', 'Unknown')} ---")
                    combined_parts.append(doc["text"])

        combined_text = "\n".join(combined_parts)

        # Enforce total size limit
        if len(combined_text) > self.MAX_DOCUMENT_LENGTH:
            logger.warning(f"Combined text exceeds limit ({len(combined_text)} > {self.MAX_DOCUMENT_LENGTH}), truncating")
            combined_text = combined_text[:self.MAX_DOCUMENT_LENGTH]

        return combined_text

    def _apply_rate_limit(self):
        """Apply rate limiting between API calls"""
        time_since_last = time.time() - self.last_api_call
        min_delay = 1.0 / RATE_LIMITS.get("highergov_calls_per_second", 2)

        if time_since_last < min_delay:
            sleep_time = min_delay - time_since_last
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)

        self.last_api_call = time.time()

    def prefetch_batch(self, search_ids: List[str], max_workers: int = 2) -> Dict[str, Dict]:
        """
        Prefetch documents for multiple opportunities
        Returns dict mapping search_id to fetched data
        """
        logger.info(f"Prefetching documents for {len(search_ids)} opportunities")
        results = {}

        for search_id in search_ids:
            try:
                results[search_id] = self.fetch_opportunity_with_documents(search_id)
                logger.info(f"Prefetched {search_id}: {results[search_id]['fetch_status']}")
            except Exception as e:
                logger.error(f"Failed to prefetch {search_id}: {e}")
                results[search_id] = {
                    "search_id": search_id,
                    "fetch_status": "error",
                    "errors": [str(e)]
                }

        return results


if __name__ == "__main__":
    # Test document fetcher
    fetcher = DocumentFetcher()

    # Test with a known search ID
    test_ids = ["fa860624r0076"]  # Example ID

    for test_id in test_ids:
        print(f"\nFetching documents for: {test_id}")
        result = fetcher.fetch_opportunity_with_documents(test_id)

        print(f"Status: {result['fetch_status']}")
        print(f"Metadata title: {result['metadata'].get('title', 'N/A')[:100] if result['metadata'] else 'No metadata'}")
        print(f"Documents fetched: {len(result['documents'])}")
        print(f"Combined text length: {len(result['combined_text'])} characters")

        if result['errors']:
            print(f"Errors: {result['errors']}")

        # Show document summary
        for doc in result['documents'][:3]:  # First 3 docs
            print(f"  - {doc.get('file_name', 'unknown')}: {len(doc.get('text', ''))} chars")