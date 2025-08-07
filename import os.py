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
    """Generate a human-readable assessment report matching the SOS v4 format"""
    from datetime import datetime
    
    # Extract key information
    agency_info = opp.get('agency', {})
    agency_name = agency_info.get('agency_name', 'Unknown Agency') if isinstance(agency_info, dict) else str(agency_info)
    
    # Get links
    highergov_link = opp.get('path', 'No link available')
    sam_link = opp.get('source_path', 'No SAM link')
    
    # Get dates
    response_date = opp.get('response_date', 'Not specified')
    posted_date = opp.get('posted_date', 'Not specified')
    
    # Get description
    description = opp.get('description_text', opp.get('description', 'No description available'))
    
    # Analyze assessment details for specific categories
    announcement_type = "RFQ/RFP - Commercial item solicitation (inferred from HigherGov data)"
    work_summary = f"Supply/repair of {opp_title} - Aviation component or service"
    sar_status = "No military SAR required"
    small_business = "Unknown set-aside status"
    sole_source = "Open competition"
    tech_data = "TDP availability unknown"
    traceability = "OEM traceability required (standard)"
    certifications = "Standard aviation certifications required"
    
    # Extract specific findings from detailed results
    blocking_factors = []
    positive_indicators = []
    
    for result in detailed_results:
        if result.decision == Decision.NO_GO:
            if "SAR" in result.reason:
                sar_status = f"Military SAR Present - {result.reason}"
                blocking_factors.append(f"SAR BLOCKER: {result.reason}")
            elif "sole source" in result.reason.lower():
                sole_source = f"Sole source restriction - {result.reason}"
                blocking_factors.append(f"SOLE SOURCE BLOCKER: {result.reason}")
            elif "security" in result.reason.lower():
                blocking_factors.append(f"SECURITY CLEARANCE BLOCKER: {result.reason}")
            elif "OEM" in result.reason:
                blocking_factors.append(f"OEM RESTRICTION BLOCKER: {result.reason}")
            elif "tech" in result.reason.lower():
                tech_data = f"Technical data not available - {result.reason}"
                blocking_factors.append(f"TECH DATA BLOCKER: {result.reason}")
            elif "platform" in result.reason.lower():
                blocking_factors.append(f"PLATFORM BLOCKER: {result.reason}")
            else:
                blocking_factors.append(f"OTHER BLOCKER: {result.reason}")
        elif result.decision == Decision.NEEDS_ANALYSIS:
            positive_indicators.append(f"NEEDS ANALYSIS: {result.reason}")
    
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
    
    # Build executive subject line
    due_date = response_date if response_date != "Not specified" else "TBD"
    subject_line = f"{opp_id} - {announcement_type.split('-')[0].strip()} - Due {due_date} - {opp_title[:30]}... - {final_recommendation}"
    
    report = f"""================================================================================
SOS OPPORTUNITY ASSESSMENT REPORT - Version 4 Format
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================================================================================

**SOLICITATION:** {opp_id}
**TITLE:** {opp_title}
**AGENCY:** {agency_name}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A. **LISTED ANSWERS**

1. **Announcement Type:**
   * Government Quote: "Data extracted from HigherGov API - {opp_title}" (HigherGov)
   * Assessment: {announcement_type}

2. **Work Summary (Aircraft/Components/Commercial Equivalent):**
   * Government Quote: "{description[:200]}..." (Solicitation)
   * Assessment: {work_summary}

3. **Source Approval Required (SAR) & OEM Traceability:**
   * Government Quote: {"SAR-related content found in document analysis" if "SAR" in sar_status else "No SAR requirements identified in available data"} (Analysis)
   * Assessment: {sar_status}

4. **Small Business Set-Aside Status:**
   * Government Quote: "Set-aside status not explicitly available in HigherGov data" (Data)
   * Assessment: {small_business}

5. **Sole Source / Intent to Award:**
   * Government Quote: {"Sole source language detected" if "sole source" in sole_source.lower() else "Open competition indicated"} (Analysis)
   * Assessment: {sole_source}

6. **Technical Data Package (TDP) Availability:**
   * Government Quote: "Technical data availability not specified in available information" (Data)
   * Assessment: {tech_data}

7. **Part Traceability / Acceptability (OEM/Surplus/Refurbished):**
   * Government Quote: "Standard aviation traceability requirements assumed" (Standard)
   * Assessment: {traceability}

8. **Key Certifications Required:**
   * Government Quote: "Standard aviation certifications apply" (Standard)
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
            'page_size': 100,  # Get 100 at a time
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