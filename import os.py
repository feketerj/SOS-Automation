import os
import json
import logging
import hashlib
import time
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Import our custom modules
# Make sure these files are in the correct subdirectories (api_clients/ and filters/)
from api_clients.highergov_client_enhanced import EnhancedHigherGovClient
from filters.initial_checklist_v2 import InitialChecklistFilterV2, Decision
from document_processors.pdf_rag_processor import PDFRAGProcessor

# --- Configuration ---
# Set up basic logging to see the script's progress
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file (for the API key)
load_dotenv()

# Your specific HigherGov Saved Search ID
SAVED_SEARCH_ID = 'tFDSNa5qi9S92K-bXbReY'
OUTPUT_DIR = 'output'
CACHE_DIR = 'document_cache'  # Cache for large documents


def get_document_cache_key(opportunity_id: str, document_path: str) -> str:
    """Generate a unique cache key for document content."""
    return hashlib.md5(f"{opportunity_id}_{document_path}".encode()).hexdigest()


def load_cached_documents(cache_key: str) -> Optional[Dict]:
    """Load cached document content if available and recent."""
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    if os.path.exists(cache_file):
        try:
            # Check if cache is less than 24 hours old
            if time.time() - os.path.getmtime(cache_file) < 86400:  # 24 hours
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.warning(f"Failed to load cache {cache_key}: {e}")
    
    return None


def save_cached_documents(cache_key: str, documents: Dict) -> None:
    """Save document content to cache."""
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(documents, f, indent=2)
    except Exception as e:
        logging.warning(f"Failed to save cache {cache_key}: {e}")


def extract_critical_text_segments(full_text: str, opp_title: str, max_length: int = 100000) -> str:
    """
    Intelligently extract the most critical segments for SOS analysis.
    Focus on sections likely to contain deal-breakers and key requirements.
    """
    if len(full_text) <= max_length:
        return full_text
    
    # Keywords that indicate critical sections for SOS analysis
    critical_keywords = [
        # SAR/Approval related
        'source approval', 'sar', 'design control', 'engineering approval', 'approved source',
        # OEM/Traceability
        'oem', 'original equipment', 'authorized dealer', 'traceability', 'pedigree',
        # Security/Clearance
        'security clearance', 'classified', 'secret', 'confidential', 'itar',
        # Sole source
        'sole source', 'single source', 'proprietary', 'only source',
        # Technical data
        'technical data', 'tdp', 'technical package', 'drawings', 'specifications',
        # Set-aside
        'small business', 'set aside', 'hubzone', 'sdvosb', 'wosb',
        # Platform specifics
        'f-15', 'f-16', 'f-22', 'f-35', 'b-1', 'b-2', 'b-52', 'c-130', 'kc-135',
        # Commercial indicators
        'commercial', 'cots', 'far part 12', 'commercial item',
        # Requirements/Restrictions
        'shall', 'must', 'required', 'mandatory', 'restriction', 'limitation'
    ]
    
    # Split text into paragraphs
    paragraphs = full_text.split('\n\n')
    
    # Score paragraphs by relevance
    scored_paragraphs = []
    for i, para in enumerate(paragraphs):
        score = 0
        para_lower = para.lower()
        
        # Score based on critical keywords
        for keyword in critical_keywords:
            if keyword in para_lower:
                score += 10
        
        # Boost score for paragraphs with opportunity title keywords
        title_words = opp_title.lower().split()
        for word in title_words:
            if len(word) > 3 and word in para_lower:
                score += 5
        
        # Boost score for paragraphs with numbers (often requirements)
        if any(char.isdigit() for char in para):
            score += 2
        
        # Boost score for shorter paragraphs (often key statements)
        if len(para) < 500:
            score += 1
        
        scored_paragraphs.append((score, i, para))
    
    # Sort by score (descending) and take the best ones
    scored_paragraphs.sort(reverse=True)
    
    # Build optimized text
    selected_text = ""
    used_length = 0
    
    # Always include the first few paragraphs (introduction)
    for i in range(min(3, len(paragraphs))):
        if used_length + len(paragraphs[i]) < max_length * 0.3:  # Reserve 30% for intro
            selected_text += paragraphs[i] + "\n\n"
            used_length += len(paragraphs[i])
    
    # Add high-scoring paragraphs
    for score, idx, para in scored_paragraphs:
        if score > 0 and used_length + len(para) < max_length:
            if para not in selected_text:  # Avoid duplicates
                selected_text += f"[SCORE: {score}] {para}\n\n"
                used_length += len(para)
    
    # Add the last paragraph (often contains contact/submission info)
    if len(paragraphs) > 0 and paragraphs[-1] not in selected_text:
        last_para = paragraphs[-1]
        if used_length + len(last_para) < max_length:
            selected_text += f"[FINAL SECTION] {last_para}"
    
    logging.info(f"Optimized text from {len(full_text)} to {len(selected_text)} chars ({len(selected_text)/len(full_text)*100:.1f}%)")
    return selected_text


def process_opportunity_documents_with_rag(api_client, opp: Dict, rag_processor: PDFRAGProcessor) -> str:
    """
    Process opportunity documents using advanced PDF RAG processing.
    Handles massive PDFs by converting them into intelligent, searchable chunks.
    """
    opp_id = opp.get('source_id', 'unknown')
    opp_title = opp.get('title', '')
    document_path = opp.get('document_path')
    
    if not document_path:
        return opp.get('description_text', '')
    
    logging.info(f"Processing documents with RAG for {opp_id}...")
    
    try:
        # Get raw documents from API (no size limits now - RAG will handle it)
        start_time = time.time()
        documents = api_client.get_opportunity_documents(
            document_path, 
            max_docs=10,  # Allow more documents
            max_text_per_doc=None  # Remove size limits - RAG will handle
        )
        
        if not documents.get('results'):
            logging.info(f"No documents found for {opp_id}")
            return opp.get('description_text', '')
        
        # Process documents with intelligent analysis - RAG for PDFs, smart extraction for text
        all_analysis_text = opp.get('description_text', '')
        total_chunks_processed = 0
        
        for doc in documents['results']:
            doc_name = doc.get('file_name', 'Unknown Document')
            
            # Strategy: Use RAG for PDFs, intelligent extraction for large text documents
            if doc.get('pdf_content'):
                # We have raw PDF - use full RAG processing
                pdf_content = doc['pdf_content']
                logging.info(f"RAG processing PDF: {doc_name} ({len(pdf_content)} bytes)")
                
                chunks = rag_processor.process_pdf_to_rag(pdf_content, doc_name)
                if chunks:
                    top_chunks = rag_processor.get_top_relevant_chunks(
                        chunks, 
                        max_chunks=25,
                        min_relevance=0.3
                    )
                    chunk_text = rag_processor.chunks_to_analysis_text(top_chunks, include_metadata=True)
                    all_analysis_text += f"\n\n{chunk_text}\n"
                    total_chunks_processed += len(chunks)
                    logging.info(f"Processed {len(chunks)} chunks from {doc_name}, using top {len(top_chunks)} for analysis")
                else:
                    logging.warning(f"No chunks extracted from {doc_name}")
                    
            elif doc.get('text_extract'):
                # We have pre-extracted text - apply intelligent processing for large documents
                extracted_text = doc['text_extract']
                
                if len(extracted_text) > 50000:  # For large documents, apply intelligent extraction
                    logging.info(f"Applying intelligent processing to large document: {doc_name} ({len(extracted_text)} chars)")
                    processed_text = extract_critical_text_segments(extracted_text, opp_title, max_length=100000)
                    all_analysis_text += f"\n\n--- Document: {doc_name} (Intelligently Processed) ---\n"
                    all_analysis_text += processed_text
                else:
                    # Small documents - use as-is
                    all_analysis_text += f"\n\n--- Document: {doc_name} ---\n"
                    all_analysis_text += extracted_text
        
        processing_time = time.time() - start_time
        
        logging.info(f"RAG Processing Summary for {opp_id}:")
        logging.info(f"  - Documents processed: {len(documents['results'])}")
        logging.info(f"  - Total chunks created: {total_chunks_processed}")
        logging.info(f"  - Final text length: {len(all_analysis_text):,} characters")
        logging.info(f"  - Processing time: {processing_time:.2f}s")
        
        return all_analysis_text
        
    except Exception as e:
        logging.error(f"RAG processing failed for {opp_id}: {e}")
        # Fallback to original description
        return opp.get('description_text', '')


def process_opportunity_documents_robust(api_client, opp: Dict) -> str:
    """
    Legacy robust processing function - kept for compatibility.
    """
    return process_opportunity_documents_with_rag(api_client, opp, PDFRAGProcessor())


def generate_human_readable_report(opp, opp_id, opp_title, final_decision, detailed_results):
    """Generate a human-readable assessment report matching the SOS v4 format with pipeline title"""
    from datetime import datetime
    import re
    
    # Extract key information
    agency_info = opp.get('agency', {})
    agency_name = agency_info.get('agency_name', 'Unknown Agency') if isinstance(agency_info, dict) else str(agency_info)
    
    # Get links
    highergov_link = opp.get('path', 'No link available')
    sam_link = opp.get('source_path', 'No SAM link')
    
    # Get dates
    response_date = opp.get('response_date', 'Not specified')
    posted_date = opp.get('posted_date', 'Not specified')
    
    # Get full text for quote extraction
    full_text = opp.get('full_analysis_text', opp.get('description_text', ''))
    description = opp.get('description_text', opp.get('description', 'No description available'))
    
    # Extract pipeline title components
    def extract_part_numbers(text):
        """Extract part numbers from text with improved patterns"""
        pn_patterns = [
            r'[Pp](?:art\s*)?[Nn](?:umber)?[:\s]*([A-Z0-9\-]{4,20})',  # P/N: or Part Number:
            r'NSN[:\s]*(\d{4}-\d{2}-[A-Z0-9\-]{3,15})',  # NSN format
            r'\b([A-Z0-9]{2,4}-[A-Z0-9\-]{4,15})\b',  # Standard format like 145-2134
            r'[Mm]odel[:\s]*([A-Z0-9\-]{3,15})',  # Model number
            r'\b([A-Z]{2,4}\d{2,8}[A-Z]?)\b'  # Format like KC46, F16A
        ]
        found_parts = []
        text_lines = text.split('\n')
        
        for line in text_lines[:50]:  # Check first 50 lines for part numbers
            line_clean = line.strip()
            if len(line_clean) > 10:
                for pattern in pn_patterns:
                    matches = re.findall(pattern, line_clean, re.IGNORECASE)
                    for match in matches:
                        # Filter out obvious non-part numbers
                        if (len(match) >= 4 and len(match) <= 20 and 
                            not match.lower().startswith(('http', 'www', 'email')) and
                            match not in found_parts):
                            found_parts.append(match)
                            if len(found_parts) >= 3:  # Limit to 3 part numbers
                                return found_parts
        
        # If no specific part numbers found, look for the title itself
        if not found_parts:
            title_parts = re.findall(r'\b([A-Z0-9\-]{3,15})\b', opp_title)
            if title_parts:
                return title_parts[:2]
        
        return ["Various"] if not found_parts else found_parts
    
    def extract_quantity(text):
        """Extract quantity from text"""
        qty_patterns = [
            r'quantity[:\s]+(\d+)',
            r'qty[:\s]+(\d+)',
            r'(\d+)\s+each',
            r'(\d+)\s+ea\b'
        ]
        for pattern in qty_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return "NA"
    
    def extract_aircraft_platform(text):
        """Extract aircraft platform from text"""
        platforms = [
            # Primary military platforms with civilian equivalents
            'KC-46', 'P-8', 'C-40', 'C-32', 'VC-25', 'E-3', 'E-6', 'E-8', 'KC-135',
            # Also check for common abbreviations without hyphens
            'KC46', 'P8', 'C40', 'C32',
            # Other common platforms
            'C-130', 'F-16', 'F-15', 'F-22', 'F-35', 'B-1', 'B-2', 'B-52',
            'C-17', 'UH-60', 'AH-64', 'CH-47', 
            # Civilian platforms
            'Boeing 737', 'Boeing 767', 'Boeing 747', 'Boeing 757', 'Airbus'
        ]
        
        text_lower = text.lower()
        
        # Check for specific platform matches
        for platform in platforms:
            if platform.lower() in text_lower:
                # Map some abbreviations to full names
                if platform.lower() in ['p8', 'p-8']:
                    return 'P-8 Poseidon'
                elif platform.lower() in ['kc46', 'kc-46']:
                    return 'KC-46 Pegasus'
                elif platform.lower() in ['c40', 'c-40']:
                    return 'C-40 Clipper'
                else:
                    return platform
        
        return "Support Equipment"
    
    def extract_description_action(title):
        """Create action description from title"""
        title_lower = title.lower()
        if any(word in title_lower for word in ['repair', 'overhaul', 'refurbish']):
            return "repair parts"
        elif any(word in title_lower for word in ['purchase', 'buy', 'procure']):
            return "purchase parts" 
        elif any(word in title_lower for word in ['support', 'maintenance']):
            return "support items"
        else:
            return "supply parts"
    
    # Build pipeline title
    part_numbers = extract_part_numbers(full_text)
    quantity = extract_quantity(full_text)
    aircraft = extract_aircraft_platform(full_text)
    action_desc = extract_description_action(opp_title)
    
    pipeline_title = f"PN: {', '.join(part_numbers)} | Qty: {quantity} | {opp_id} | {aircraft} | {action_desc}"
    
    # Extract quotes for each section with better search
    def find_quote(search_terms, default_msg="No specific language found", section_name=""):
        """Find relevant quotes from full text with better logic"""
        best_quote = None
        best_score = 0
        
        # Split text into meaningful sentences
        sentences = []
        for line in full_text.split('\n'):
            line = line.strip()
            if len(line) > 20 and not line.startswith('|'):  # Skip table formatting
                # Split long lines into sentences
                for sent in line.split('.'):
                    sent = sent.strip()
                    if len(sent) > 15:
                        sentences.append(sent)
        
        # Score sentences by relevance
        for sentence in sentences:
            sentence_lower = sentence.lower()
            score = 0
            
            # Score based on search terms
            for term in search_terms:
                if term.lower() in sentence_lower:
                    score += 10
            
            # Additional scoring for meaningful content
            if any(word in sentence_lower for word in ['shall', 'must', 'required', 'provided']):
                score += 5
            if any(word in sentence_lower for word in ['contractor', 'offeror', 'vendor']):
                score += 3
            if len(sentence) > 30 and len(sentence) < 150:  # Prefer medium-length sentences
                score += 2
                
            if score > best_score and score > 5:  # Minimum relevance threshold
                best_score = score
                best_quote = sentence
        
        if best_quote and len(best_quote) > 20:  # Ensure meaningful quotes
            # Trim excessively long quotes
            if len(best_quote) > 120:
                best_quote = best_quote[:120].strip()
            return f'"{best_quote}..." (Document analysis)'
        else:
            return f'"{default_msg}"'
    
    # Extract quotes for each section with better search - but these will be overridden by filter findings
    # Get actual announcement type from document metadata or content
    def determine_announcement_type(opp_data, full_text):
        """Determine the actual announcement type from opportunity data and document content"""
        # Check opportunity metadata first
        notice_type = opp_data.get('notice_type', '').lower()
        solicitation_type = opp_data.get('solicitation_type', '').lower() 
        description = opp_data.get('description_text', '').lower()
        title = opp_data.get('title', '').lower()
        
        # Look for explicit notice type indicators
        if any(term in notice_type for term in ['sources sought', 'source sought']):
            return "Sources Sought Notice"
        elif any(term in notice_type for term in ['pre-solicitation', 'presolicitation']):
            return "Pre-Solicitation Notice"
        elif any(term in notice_type for term in ['award', 'contract award']):
            return "Award Notice"
        elif any(term in notice_type for term in ['rfp', 'request for proposal']):
            return "Request for Proposal (RFP)"
        elif any(term in notice_type for term in ['rfq', 'request for quotation']):
            return "Request for Quotation (RFQ)"
        elif any(term in notice_type for term in ['ifi', 'invitation for bid']):
            return "Invitation for Bid (IFB)"
        elif any(term in notice_type for term in ['modification', 'amendment']):
            return "Solicitation Modification/Amendment"
        
        # Check solicitation type field
        if 'rfp' in solicitation_type or 'proposal' in solicitation_type:
            return "Request for Proposal (RFP)"
        elif 'rfq' in solicitation_type or 'quotation' in solicitation_type:
            return "Request for Quotation (RFQ)"
        elif 'ifb' in solicitation_type or 'bid' in solicitation_type:
            return "Invitation for Bid (IFB)"
        
        # Check document content for announcement type indicators
        content_check = (description + ' ' + title + ' ' + full_text[:1000]).lower()
        
        # Check for specific notice types in content
        if 'commercial product procurement notice' in content_check:
            return "Request for Quotation (RFQ) - Commercial"
        elif any(term in content_check for term in ['sources sought', 'market research', 'capability statement']):
            return "Sources Sought Notice"
        elif any(term in content_check for term in ['request for proposal', 'rfp']):
            return "Request for Proposal (RFP)"
        elif any(term in content_check for term in ['request for quotation', 'rfq']):
            return "Request for Quotation (RFQ)"
        elif any(term in content_check for term in ['invitation for bid', 'ifb', 'sealed bid']):
            return "Invitation for Bid (IFB)"
        elif any(term in content_check for term in ['pre-solicitation', 'advance notice']):
            return "Pre-Solicitation Notice"
        elif any(term in content_check for term in ['contract award', 'award notice', 'awarded to']):
            return "Award Notice"
        elif any(term in content_check for term in ['modification', 'amendment', 'change order']):
            return "Solicitation Modification/Amendment"
        elif any(term in content_check for term in ['combined synopsis', 'synopsis/solicitation']):
            return "Combined Synopsis/Solicitation"
        
        # Default fallback
        return "Solicitation Notice (Type TBD)"
    
    actual_announcement_type = determine_announcement_type(opp, full_text)
    announcement_quote = find_quote(['solicitation', 'synopsis', 'notice', 'rfq', 'rfp', 'request for'], 
                                   f"Document indicates: {actual_announcement_type}", "announcement")
    
    # Set work summary and quote based on title analysis
    if 'repair' in opp_title.lower() or 'modification' in opp_title.lower():
        default_work_summary = f"Repair/modification of {opp_title} - Aviation component service"
        work_quote = find_quote(['repair', 'modification', 'overhaul', 'rfi', 'ready for issue'], 
                               "Contractor shall provide repair services", "work")
    else:
        default_work_summary = f"Supply/procurement of {opp_title} - Aviation component or service"
        work_quote = find_quote(['supply', 'purchase', 'provide', 'deliver', 'furnish'], 
                               description[:100] + "...", "work")
    
    # Check if TDP seems available
    if any(term in full_text.lower() for term in ['repair manuals', 'drawings', 'specifications', 'tech publications']):
        default_tech_data = "TDP appears available - repair manuals/drawings referenced"
    else:
        default_tech_data = "TDP availability unknown"
    
    # Default quotes - will be replaced by filter findings if blockers detected
    sar_quote = find_quote(['source approval required', 'sar', 'approved source list', 'mil-std', 'military specification'], 
                          "No source approval requirements found", "sar")
    
    setaside_quote = find_quote(['small business set-aside', 'set aside for small business', 'hubzone', 'sdvosb', 'not applicable'], 
                               "Set-aside determination not specified", "setaside")
    
    solesource_quote = find_quote(['sole source', 'single source', 'intent to award', 'all responsible sources may submit'], 
                                 "Open competition - all responsible sources", "solesource")
    
    tdp_quote = find_quote(['technical data', 'drawings', 'specifications', 'repair manuals', 'tech publications'], 
                          "Technical data availability not clearly specified", "tdp")
    
    trace_quote = find_quote(['traceability', 'certificate of conformance', 'coc', 'pedigree', 'airworthy'], 
                            "Standard traceability requirements apply", "traceability")
    
    cert_quote = find_quote(['certificate of conformance', 'airworthy', 'far 52.246', 'quality requirements'], 
                           "Standard certifications required", "certifications")
    
    # Extract specific findings from detailed results and build assessments based on what filters actually found
    blocking_factors = []
    positive_indicators = []
    
    # Start with defaults, but override based on actual filter findings
    announcement_type = actual_announcement_type  # Use the actual announcement type we determined
    work_summary = default_work_summary
    sar_status = "No military SAR required"
    small_business = "Unknown set-aside status"
    sole_source = "Open competition"
    tech_data = default_tech_data
    traceability = "OEM traceability required (standard)"
    certifications = "Standard aviation certifications required"
    
    # Process each filter result and update assessments with actual findings
    for result in detailed_results:
        # Extract the actual quote that caused the decision
        filter_quote = result.quote if hasattr(result, 'quote') and result.quote else "Filter analysis"
        
        if result.decision == Decision.NO_GO:
            if "SAR" in result.reason or "source approval" in result.reason.lower():
                sar_status = f"Yes - Military SAR required. {result.reason}"
                sar_quote = f'"{filter_quote[:120]}..." (Filter detected SAR requirement)'
                blocking_factors.append(f"SAR BLOCKER: {result.reason}")
                
            elif "sole source" in result.reason.lower() or "single source" in result.reason.lower():
                sole_source = f"Sole source restriction - {result.reason}"
                solesource_quote = f'"{filter_quote[:120]}..." (Filter detected sole source)'
                blocking_factors.append(f"SOLE SOURCE BLOCKER: {result.reason}")
                
            elif "security" in result.reason.lower() or "clearance" in result.reason.lower():
                blocking_factors.append(f"SECURITY CLEARANCE BLOCKER: {result.reason}")
                
            elif "OEM" in result.reason or "original equipment" in result.reason.lower():
                traceability = f"OEM restriction detected - {result.reason}"
                trace_quote = f'"{filter_quote[:120]}..." (Filter detected OEM restriction)'
                blocking_factors.append(f"OEM RESTRICTION BLOCKER: {result.reason}")
                
            elif "tech" in result.reason.lower() or "technical data" in result.reason.lower():
                tech_data = f"Technical data not available - {result.reason}"
                tdp_quote = f'"{filter_quote[:120]}..." (Filter detected TDP issue)'
                blocking_factors.append(f"TECH DATA BLOCKER: {result.reason}")
                
            elif "platform" in result.reason.lower():
                blocking_factors.append(f"PLATFORM BLOCKER: {result.reason}")
                
            elif "set-aside" in result.reason.lower() or "small business" in result.reason.lower():
                small_business = f"Set-aside restriction - {result.reason}"
                setaside_quote = f'"{filter_quote[:120]}..." (Filter detected set-aside)'
                blocking_factors.append(f"SET-ASIDE BLOCKER: {result.reason}")
                
            else:
                blocking_factors.append(f"OTHER BLOCKER: {result.reason}")
                
        elif result.decision == Decision.NEEDS_ANALYSIS:
            positive_indicators.append(f"NEEDS ANALYSIS: {result.reason}")
            
        elif result.decision == Decision.PASS:
            # For passed checks, we can note positive findings but don't override announcement type
            if "aviation" in result.reason.lower() or "aircraft" in result.reason.lower():
                positive_indicators.append(f"Aviation-related: {result.reason}")
            # Don't override announcement_type for commercial findings - we already determined the actual type
    
    # Determine status
    if final_decision == Decision.GO:
        final_recommendation = "GO"
        justification = "This opportunity passed all SOS filters with no blocking restrictions identified. Aviation-related component with acceptable business terms."
    elif final_decision == Decision.NEEDS_ANALYSIS:
        final_recommendation = "Further Analysis Required"
        justification = "This opportunity requires manual review due to conditional platforms or mixed indicators. Human judgment needed for final determination."
    else:
        final_recommendation = "NO-GO"
        justification = f"This opportunity has blocking restrictions: {', '.join([bf.split(':')[0] for bf in blocking_factors[:2]])}"
    
    # Build executive subject line (using pipeline format for GO decisions)
    due_date = response_date if response_date != "Not specified" else "TBD"
    if final_decision == Decision.GO:
        subject_line = pipeline_title  # Use pipeline title for GO decisions
    else:
        subject_line = f"{opp_id} - RFQ/RFP - Due {due_date} - {opp_title[:30]}... - {final_recommendation}"
    
    report = f"""================================================================================
SOS OPPORTUNITY ASSESSMENT REPORT - Version 4 Format
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================================================================================

{f"**PIPELINE TITLE:** {pipeline_title}" if final_decision == Decision.GO else ""}

**SOLICITATION:** {opp_id}
**TITLE:** {opp_title}
**AGENCY:** {agency_name}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A. **LISTED ANSWERS**

1. **Announcement Type:**
   * Government Quote: {announcement_quote}
   * Assessment: {announcement_type}

2. **Work Summary (Aircraft/Components/Commercial Equivalent):**
   * Government Quote: {work_quote}
   * Assessment: {work_summary}

3. **Source Approval Required (SAR) & OEM Traceability:**
   * Government Quote: {sar_quote}
   * Assessment: {sar_status}

4. **Small Business Set-Aside Status:**
   * Government Quote: {setaside_quote}
   * Assessment: {small_business}

5. **Sole Source / Intent to Award:**
   * Government Quote: {solesource_quote}
   * Assessment: {sole_source}

6. **Technical Data Package (TDP) Availability:**
   * Government Quote: {tdp_quote}
   * Assessment: {tech_data}

7. **Part Traceability / Acceptability (OEM/Surplus/Refurbished):**
   * Government Quote: {trace_quote}
   * Assessment: {traceability}

8. **Key Certifications Required:**
   * Government Quote: {cert_quote}
   * Assessment: {certifications}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

B. **KEY DEAL-BREAKERS SUMMARY**

**Blockers:**
{chr(10).join([f"- {bf}" for bf in blocking_factors]) if blocking_factors else "- No blocking factors identified"}

**Positives:**
{chr(10).join([f"- {pi}" for pi in positive_indicators]) if positive_indicators else "- Aviation-related opportunity identified"}
- Open to competitive bidding
- Commercial aviation component/service

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

C. **FINAL RECOMMENDATION:**
**{final_recommendation}**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

D. **JUSTIFICATION:**
{justification}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

E. **EXECUTIVE SUBJECT LINE:**
{subject_line}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**DETAILED CHECKLIST RESULTS:**
{chr(10).join([f"- {result.check_name}: {result.decision.value} - {result.reason}" for result in detailed_results if result.decision != Decision.PASS]) if any(result.decision != Decision.PASS for result in detailed_results) else "- All checks passed - No blocking issues found"}

**LINKS FOR REVIEW:**
- HigherGov: {highergov_link}
- SAM.gov: {sam_link}

**RESPONSE DUE:** {response_date}
**POSTED DATE:** {posted_date}

================================================================================
End of Assessment - {opp_id}
================================================================================
"""
    
    return report


def main():
    """
    Main function to run the SOS opportunity assessment pipeline with RAG processing.
    """
    logging.info("--- Starting SourceOne Spares Automation Pipeline with PDF RAG Processing ---")

    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logging.info(f"Output will be saved to the '{OUTPUT_DIR}' directory.")

    try:
        # --- Step 1: Initialize Clients ---
        api_client = EnhancedHigherGovClient()
        filter_logic = InitialChecklistFilterV2()
        
        # Initialize the PDF RAG processor
        rag_processor = PDFRAGProcessor(cache_dir="pdf_rag_cache")
        logging.info("API Client, V2 Filter Logic, and PDF RAG Processor initialized successfully.")

        # Create cache directory
        os.makedirs(CACHE_DIR, exist_ok=True)

        # --- Step 2: Fetch Opportunities ---
        logging.info(f"Fetching opportunities from saved search ID: {SAVED_SEARCH_ID}")
        # Use the correct HigherGov API endpoint structure with document inclusion
        search_params = {
            'api_key': api_client.api_key,
            'search_id': SAVED_SEARCH_ID,
            'page_size': 5,  # Get up to 5 opportunities to see what's available
            'source_type': 'sam',  # Federal opportunities
            'include_documents': True,  # IMPORTANT: Include document attachments
            'include_ai_summary': True  # Also include AI summaries if available
        }
        # Use the correct endpoint path
        response_data = api_client._get('opportunity/', params=search_params)
        
        opportunities = response_data.get('results', [])
        if not opportunities:
            logging.warning("No opportunities found for the given saved search. Exiting.")
            return

        logging.info(f"Found {len(opportunities)} opportunities to process.")
        
        # Track processing statistics
        processed_count = 0
        error_count = 0

        # --- Step 3: Process Each Opportunity with PDF RAG Processing ---
        for i, opp in enumerate(opportunities, 1):
            opp_id = opp.get('source_id', 'UnknownID')
            opp_title = opp.get('title', 'Unknown Title')
            
            print("\n" + "="*80)
            logging.info(f"Processing Opportunity {i}/{len(opportunities)}: {opp_title[:50]}... ({opp_id})")
            
            try:
                # --- Step 3.5: Advanced PDF RAG Processing ---
                start_time = time.time()
                enhanced_text = process_opportunity_documents_with_rag(api_client, opp, rag_processor)
                processing_time = time.time() - start_time
                
                # Update the opportunity object with enhanced text
                opp['full_analysis_text'] = enhanced_text
                
                logging.info(f"RAG processing completed in {processing_time:.2f}s for {opp_id}")
                
                # --- Step 4: Assess with V2 Filter ---
                final_decision, detailed_results = filter_logic.assess_opportunity(opp)
                
                # --- Step 5: Report Results ---
                print(f"\nFINAL DECISION: [{final_decision.value}]")
                print("-"*20)
                print("Detailed Assessment Breakdown:")
                for result in detailed_results:
                    # Only print checks that were not a simple PASS
                    if result.decision != Decision.PASS:
                        print(f"  - Check: {result.check_name}")
                        print(f"    - Decision: {result.decision.value}")
                        print(f"    - Reason: {result.reason}")
                        if result.quote:
                            print(f"    - Quote: '{result.quote[:150]}...'") # Truncate long quotes

                # --- Step 6: Save Human-Readable Report ---
                report = generate_human_readable_report(opp, opp_id, opp_title, final_decision, detailed_results)
                
                file_path = os.path.join(OUTPUT_DIR, f"{opp_id}.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                logging.info(f"Assessment report saved to {file_path}")
                
                # Also save JSON for summary generation (optional backup)
                json_data = {
                    'opportunity_id': opp_id,
                    'opportunity_title': opp_title,
                    'final_decision': final_decision.value,
                    'assessment_details': [res.__dict__ for res in detailed_results],
                    'processing_time': processing_time,
                    'text_length': len(enhanced_text),
                    'rag_processed': True,
                    'original_opportunity': opp
                }
                json_path = os.path.join(OUTPUT_DIR, f"{opp_id}.json")
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=4, default=str)
                
                processed_count += 1
                
            except Exception as e:
                logging.error(f"Failed to process opportunity {opp_id}: {e}")
                error_count += 1
                
                # Create error report
                error_report = f"""ERROR PROCESSING {opp_id}
Title: {opp_title}
Error: {str(e)}
Time: {time.strftime('%Y-%m-%d %H:%M:%S')}

This opportunity could not be processed due to technical issues.
Please review manually or retry later.
"""
                error_path = os.path.join(OUTPUT_DIR, f"{opp_id}_ERROR.txt")
                with open(error_path, 'w', encoding='utf-8') as f:
                    f.write(error_report)
        
        # Final processing summary
        logging.info(f"""
        === PDF RAG PROCESSING SUMMARY ===
        Total Opportunities: {len(opportunities)}
        Successfully Processed: {processed_count}
        Errors: {error_count}
        Success Rate: {processed_count/len(opportunities)*100:.1f}%
        RAG Cache Directory: pdf_rag_cache/
        """)

    except Exception as e:
        logging.error(f"An unexpected error occurred in the main pipeline: {e}", exc_info=True)

    finally:
        logging.info("--- Pipeline execution finished. ---")


if __name__ == "__main__":
    main()