import os
import requests
import logging
from typing import Dict, List, Optional
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class EnhancedHigherGovClient:
    """
    Enhanced HigherGov API client for SOS opportunity assessment pipeline.
    Supports configurable daily endpoint URLs.
    """

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://www.highergov.com/api-external"):
        """
        Initialize the HigherGov API client.
        
        Args:
            api_key: HigherGov API key. If not provided, will look for HIGHERGOV_API_KEY env var.
            base_url: Base URL for the HigherGov API.
        """
        self.api_key = api_key or os.getenv('HIGHERGOV_API_KEY')
        self.saved_search_id = os.getenv('SAVED_SEARCH_ID')
        self.use_mock_data = not self.api_key  # Use mock data if no API key
        
        if self.api_key:
            self.base_url = base_url
            self.session = requests.Session()
            # HigherGov uses API key as a query parameter, not in headers
            self.session.headers.update({
                'Content-Type': 'application/json',
                'User-Agent': 'SOS-Automation-Pipeline/1.0'
            })
            print(f"Using real HigherGov API with saved search: {self.saved_search_id}")
        else:
            print("No API key found - using mock data for testing")

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make a GET request to the HigherGov API or return mock data.
        
        Args:
            endpoint: API endpoint 
            params: Query parameters
            
        Returns:
            JSON response as dictionary
        """
        # If using mock data, return mock data immediately
        if self.use_mock_data:
            print(f"Using mock data for endpoint: {endpoint}")
            return self._get_mock_data()
        
        # Construct the proper API URL
        # Remove leading slash from endpoint to avoid double slash
        endpoint = endpoint.lstrip('/')
        url = f"{self.base_url}/{endpoint}"
        
        # Set up parameters
        if not params:
            params = {}
        params['api_key'] = self.api_key
        
        try:
            logger.info(f"Making API request to: {url}")
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            # Handle both 'opportunities' and 'results' response formats
            opp_count = len(data.get('opportunities', [])) or len(data.get('results', []))
            logger.info(f"API request successful. Received {opp_count} opportunities.")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            # For testing purposes, return mock data if API fails
            return self._get_mock_data()
        except Exception as e:
            logger.error(f"Unexpected error in API request: {e}")
            return self._get_mock_data()

    def _get_mock_data(self) -> Dict:
        """
        Return mock data for testing when API is unavailable.
        """
        logger.warning("Using mock data for testing - API call failed or not configured")
        
        return {
            "results": [
                {
                    "source_id": "MOCK-001-SAR-TEST",
                    "title": "F-16 Engine Components - Source Approval Required",
                    "description_text": "This procurement requires engineering source approval by the design control activity. Military specification parts only. Approved sources must submit SAR package with proposal.",
                    "due_date": "2025-12-01",
                    "set_aside": "Small Business",
                    "documents": []
                },
                {
                    "source_id": "MOCK-002-COMMERCIAL-TEST", 
                    "title": "Boeing 737 Hydraulic System Overhaul",
                    "description_text": "Commercial item acquisition under FAR Part 12. Seeking overhaul services for Boeing 737-800 hydraulic pumps. Refurbished parts acceptable. P/N: 12345-67890, Qty: 5 each.",
                    "due_date": "2025-12-15",
                    "set_aside": "Unrestricted",
                    "documents": []
                },
                {
                    "source_id": "MOCK-003-OEM-RESTRICTION-TEST",
                    "title": "KC-46 Landing Gear Components - OEM Only",
                    "description_text": "Procurement for KC-46 Pegasus landing gear components. OEM direct traceability only. Authorized distributor required. Boeing factory authorized dealer preference.",
                    "due_date": "2025-11-30",
                    "set_aside": "Small Business",
                    "documents": []
                },
                {
                    "source_id": "MOCK-004-INTENT-SOLE-SOURCE-TEST",
                    "title": "UH-60 Black Hawk Spare Parts - Intent to Sole Source",
                    "description_text": "Intent to sole source to Sikorsky for UH-60 Black Hawk spare parts. Brand name or equal may be acceptable. ITAR compliance required for international delivery.",
                    "due_date": "2025-12-20",
                    "set_aside": "Small Business Set-Aside",
                    "documents": []
                },
                {
                    "source_id": "MOCK-005-PURE-CIVILIAN-TEST",
                    "title": "Cessna 208 Caravan Engine Overhaul",
                    "description_text": "State of Alaska Department of Transportation seeking engine overhaul services for Cessna 208 Caravan fleet. PT6A-114A engines. Refurbished and surplus parts acceptable.",
                    "due_date": "2025-12-10",
                    "set_aside": "Unrestricted",
                    "documents": []
                }
            ],
            "total_count": 5,
            "page": 1,
            "per_page": 50
        }

    def get_saved_search_opportunities(self, search_id: str, limit: int = 50) -> Dict:
        """
        Fetch opportunities from a saved search.
        
        Args:
            search_id: The HigherGov saved search ID
            limit: Maximum number of opportunities to fetch
            
        Returns:
            Dictionary containing opportunities and metadata
        """
        params = {
            'search_id': search_id,
            'limit': limit,
            'include_documents': True
        }
        
        return self._get('opportunity', params=params)

    def get_opportunity_details(self, opportunity_id: str) -> Dict:
        """
        Fetch detailed information for a specific opportunity.
        
        Args:
            opportunity_id: The opportunity source_id or HigherGov ID
            
        Returns:
            Dictionary containing detailed opportunity information
        """
        return self._get(f'opportunity/{opportunity_id}')

    def search_opportunities(self, query: str, filters: Optional[Dict] = None) -> Dict:
        """
        Search for opportunities using text query and filters.
        
        Args:
            query: Text search query
            filters: Additional search filters
            
        Returns:
            Dictionary containing search results
        """
        params = {
            'q': query,
            'include_documents': True
        }
        
        if filters:
            params.update(filters)
            
        return self._get('opportunity/search', params=params)

    def get_opportunity_documents(self, document_path: str, max_docs: int = 10, max_text_per_doc: Optional[int] = 50000) -> Dict:
        """
        Enhanced method to fetch opportunity documents with support for raw PDF content.
        Now handles massive PDFs by returning raw bytes for RAG processing.
        
        Args:
            document_path: Full URL to the documents API endpoint
            max_docs: Maximum number of documents to fetch
            max_text_per_doc: Maximum text size per document (None = no limit for RAG processing)
            
        Returns:
            Dictionary containing document results with both text and raw PDF content
        """
        if self.use_mock_data:
            return {"results": []}
        
        try:
            # The document_path already contains the full URL with API key
            logger.info(f"Fetching documents with RAG support: max_docs={max_docs}, max_text_per_doc={max_text_per_doc}")
            response = requests.get(document_path, timeout=60)  # Increased timeout for RAG processing
            response.raise_for_status()
            
            raw_data = response.json()
            
            # Process documents with RAG support
            if 'results' in raw_data and raw_data['results']:
                processed_docs = []
                
                for i, doc in enumerate(raw_data['results'][:max_docs]):
                    doc_name = doc.get('file_name', f'Document_{i+1}')
                    doc_url = doc.get('document_url') or doc.get('file_url')
                    
                    processed_doc = doc.copy()
                    
                    # If we have a document URL, fetch the raw content for RAG processing
                    if doc_url:
                        try:
                            # Fetch the actual document content
                            doc_response = requests.get(doc_url, timeout=45)
                            doc_response.raise_for_status()
                            
                            raw_content = doc_response.content
                            content_type = doc_response.headers.get('content-type', '').lower()
                            
                            processed_doc['size_bytes'] = len(raw_content)
                            processed_doc['content_type'] = content_type
                            
                            # Handle PDF files - provide raw content for RAG processing
                            if 'pdf' in content_type or doc_name.lower().endswith('.pdf'):
                                processed_doc['pdf_content'] = raw_content
                                processed_doc['is_pdf'] = True
                                
                                # Quick text extraction for immediate analysis (limited)
                                if 'text_extract' not in processed_doc or not processed_doc.get('text_extract'):
                                    try:
                                        import PyPDF2
                                        import io
                                        
                                        pdf_reader = PyPDF2.PdfReader(io.BytesIO(raw_content))
                                        text_content = ""
                                        
                                        # Extract from first few pages for quick preview
                                        for page_num, page in enumerate(pdf_reader.pages[:5]):
                                            try:
                                                text_content += page.extract_text() + "\n"
                                            except:
                                                continue
                                        
                                        processed_doc['text_extract'] = text_content[:2000] + f"\n\n[PDF PREVIEW - Full {len(raw_content)} byte PDF available for RAG processing]"
                                        
                                    except Exception as e:
                                        logger.warning(f"Could not extract preview from PDF {doc_name}: {e}")
                                        processed_doc['text_extract'] = f"[PDF Content - {len(raw_content)} bytes - Use RAG processor for full text]"
                                
                                logger.info(f"Prepared PDF {doc_name} ({len(raw_content)} bytes) for RAG processing")
                            
                            # Handle other file types
                            else:
                                try:
                                    # Try to decode as text
                                    text_content = raw_content.decode('utf-8', errors='ignore')
                                    
                                    # Apply size limits for non-PDF files
                                    if max_text_per_doc and len(text_content) > max_text_per_doc:
                                        first_part = text_content[:int(max_text_per_doc * 0.7)]
                                        last_part = text_content[-int(max_text_per_doc * 0.3):]
                                        processed_doc['text_extract'] = first_part + f"\n\n[... TRUNCATED {len(text_content) - max_text_per_doc} CHARACTERS ...]\n\n" + last_part
                                        logger.warning(f"Truncated text document {doc_name} from {len(text_content)} to ~{max_text_per_doc} chars")
                                    else:
                                        processed_doc['text_extract'] = text_content
                                        
                                except UnicodeDecodeError:
                                    processed_doc['text_extract'] = f"[Binary content - {len(raw_content)} bytes]"
                                    processed_doc['raw_content'] = raw_content
                        
                        except requests.RequestException as e:
                            logger.error(f"Failed to fetch document content for {doc_name}: {e}")
                            # Keep the original document metadata even if content fetch failed
                        except Exception as e:
                            logger.error(f"Error processing document {doc_name}: {e}")
                    
                    # Handle existing text_extract with size limits (for non-PDF docs)
                    elif 'text_extract' in processed_doc and processed_doc['text_extract']:
                        original_length = len(processed_doc['text_extract'])
                        if max_text_per_doc and original_length > max_text_per_doc:
                            first_part = processed_doc['text_extract'][:int(max_text_per_doc * 0.7)]
                            last_part = processed_doc['text_extract'][-int(max_text_per_doc * 0.3):]
                            processed_doc['text_extract'] = first_part + f"\n\n[... TRUNCATED {original_length - max_text_per_doc} CHARACTERS ...]\n\n" + last_part
                            logger.warning(f"Truncated existing text for {doc_name} from {original_length} to ~{max_text_per_doc} chars")
                    
                    processed_docs.append(processed_doc)
                
                raw_data['results'] = processed_docs
                raw_data['rag_ready'] = True
                logger.info(f"Successfully processed {len(processed_docs)} documents with RAG support")
            
            return raw_data
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching documents from {document_path} - documents may be too large")
            return {"results": [], "error": "timeout"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch documents from {document_path}: {e}")
            return {"results": [], "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error processing documents with RAG support: {e}")
            return {"results": [], "error": str(e)}
