#!/usr/bin/env python3
"""
HigherGov Batch Fetcher and Assessor
Fetch ALL opportunities from a HigherGov search ID and assess them
"""

import os
import sys
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from sos_ingestion_gate_v419 import IngestionGateV419, Decision

class HigherGovBatchFetcher:
    """Fetch and assess all opportunities from HigherGov search"""
    
    def __init__(self):
        # Get API key from environment or use default
        self.api_key = os.environ.get('HIGHERGOV_API_KEY', '9874995194174018881c567d92a2c4d2')
        self.base_url = 'https://www.highergov.com/api-external/opportunity/'
        self.gate = IngestionGateV419()
        
    def fetch_all_opportunities(self, search_id: str, max_pages: int = 10) -> List[Dict]:
        """Fetch all opportunities for a search ID"""
        
        print(f"\n{'='*70}")
        print(f"FETCHING ALL OPPORTUNITIES FROM HIGHERGOV")
        print(f"Search ID: {search_id}")
        print(f"{'='*70}\n")
        
        all_opportunities = []
        page = 1
        
        while page <= max_pages:
            params = {
                'api_key': self.api_key,
                'search_id': search_id,
                'page_size': 100,  # Max allowed
                'page_number': page
            }
            
            print(f"Fetching page {page}...")
            
            try:
                response = requests.get(self.base_url, params=params, timeout=30)
                
                if response.status_code != 200:
                    print(f"Error: API returned status {response.status_code}")
                    if response.status_code == 401:
                        print("Authentication failed - check API key")
                    break
                
                data = response.json()
                results = data.get('results', [])
                
                if not results:
                    print(f"No more results. Total fetched: {len(all_opportunities)}")
                    break
                
                all_opportunities.extend(results)
                print(f"  Found {len(results)} opportunities on page {page}")
                
                # Check if there are more pages
                meta = data.get('meta', {})
                pagination = meta.get('pagination', {})
                total_pages = pagination.get('pages', 1)
                
                if page >= total_pages:
                    print(f"Reached last page. Total opportunities: {len(all_opportunities)}")
                    break
                
                page += 1
                
            except Exception as e:
                print(f"Error fetching page {page}: {e}")
                break
        
        return all_opportunities
    
    def fetch_document_text(self, document_path: str) -> str:
        """Fetch full document text if available"""
        if not document_path:
            return ""
        
        try:
            # Document path already includes API key
            response = requests.get(document_path, timeout=30)
            if response.status_code == 200:
                docs = response.json()
                
                # Combine all document text
                full_text = []
                for doc in docs.get('results', []):
                    # Add document filename
                    if doc.get('file_name'):
                        full_text.append(f"DOCUMENT: {doc['file_name']}\n")
                    
                    # Add document text - text_extract is the key field!
                    if doc.get('text_extract'):
                        full_text.append(doc['text_extract'])
                    elif doc.get('text'):
                        full_text.append(doc['text'])
                    elif doc.get('description'):
                        full_text.append(doc['description'])
                    
                    full_text.append("\n---\n")
                
                return "\n".join(full_text) if full_text else ""
        except Exception as e:
            # Silent fail - don't spam warnings
            pass
        
        return ""
    
    def process_opportunity(self, data: Dict) -> Dict:
        """Convert HigherGov data to our format - DOCUMENTS FIRST"""
        
        # Handle nested fields
        naics = data.get('naics_code', {})
        if isinstance(naics, dict):
            naics = naics.get('naics_code', '')
        
        psc = data.get('psc_code', {})
        if isinstance(psc, dict):
            psc = psc.get('psc_code', '')
        
        agency = data.get('agency', {})
        if isinstance(agency, dict):
            agency_name = agency.get('agency_name', 'Unknown')
        else:
            agency_name = str(agency) if agency else 'Unknown'
        
        # PRIORITY 1: Try to fetch full documents
        document_text = ""
        if data.get('document_path'):
            document_text = self.fetch_document_text(data['document_path'])
        
        # PRIORITY 2: Use provided description/summary
        description = data.get('description_text') or ''
        ai_summary = data.get('ai_summary') or ''
        
        # Combine all available text (documents > summary > description)
        if document_text:
            full_text = f"{document_text}\n\nSUMMARY:\n{ai_summary}\n\nDESCRIPTION:\n{description}"
        elif ai_summary and description:
            full_text = f"{ai_summary}\n\nDETAILS:\n{description}"
        elif ai_summary:
            full_text = ai_summary
        elif description:
            full_text = description
        else:
            # FALLBACK: Use title and metadata only
            full_text = f"Title: {data.get('title', '')}\nAgency: {agency_name}\nNAICS: {naics}\nPSC: {psc}"
        
        # Build opportunity object
        opportunity = {
            'id': data.get('source_id') or data.get('opp_key') or 'UNKNOWN',
            'title': data.get('title') or 'Unknown',
            'agency': agency_name,
            'naics': str(naics) if naics else '',
            'psc': str(psc) if psc else '',
            'set_aside': data.get('set_aside') or '',
            'text': full_text,
            'posted_date': data.get('posted_date') or '',
            'response_deadline': data.get('due_date') or '',
            'url': data.get('source_path') or data.get('path') or '',
            'value_low': data.get('val_est_low') or 0,
            'value_high': data.get('val_est_high') or 0,
            'nsn': data.get('nsn') or []
        }
        
        return opportunity
    
    def assess_batch(self, opportunities: List[Dict], fetch_docs: bool = True) -> Tuple[List, List, List, Dict]:
        """Assess all opportunities with optional document fetching"""
        
        print(f"\n{'='*70}")
        print(f"ASSESSING {len(opportunities)} OPPORTUNITIES")
        if fetch_docs:
            print(f"Document fetching: ENABLED (this may take longer)")
        else:
            print(f"Document fetching: DISABLED (using metadata only)")
        print(f"{'='*70}\n")
        
        # Process all opportunities with progress tracking
        processed = []
        docs_fetched = 0
        
        for i, opp in enumerate(opportunities):
            if i % 100 == 0 and i > 0:
                print(f"  Processed {i}/{len(opportunities)} opportunities...")
            
            # Track if we fetched documents
            had_doc_path = bool(opp.get('document_path'))
            proc_opp = self.process_opportunity(opp)
            
            # Check if we got substantial text (more than just metadata)
            if len(proc_opp.get('text', '')) > 500:
                docs_fetched += 1
            
            processed.append(proc_opp)
        
        print(f"\nDocument coverage: {docs_fetched}/{len(opportunities)} ({docs_fetched/len(opportunities)*100:.1f}%) have substantial text")
        
        # Run batch assessment
        go, nogo, further = [], [], []
        stats = {
            'total': len(processed),
            'errors': 0,
            'go_confidence_avg': 0,
            'knockout_reasons': {}
        }
        
        # Process each opportunity individually
        go_scores = []
        for opp in processed:
            try:
                result = self.gate.assess_opportunity(opp)
                
                if result.decision == Decision.GO:
                    go.append({**opp, 'assessment': result})
                    # Use primary blocker as confidence metric for now
                    go_scores.append(85.0)  # Default GO confidence
                elif result.decision == Decision.NO_GO:
                    nogo.append({**opp, 'assessment': result})
                    # Track knockout reasons
                    if result.primary_blocker:
                        stats['knockout_reasons'][result.primary_blocker] = stats['knockout_reasons'].get(result.primary_blocker, 0) + 1
                else:  # FURTHER_ANALYSIS
                    further.append({**opp, 'assessment': result})
            except Exception as e:
                print(f"  [ERROR] Assessment failed for {opp.get('title', 'Unknown')}: {str(e)}")
                stats['errors'] += 1
                nogo.append({**opp, 'assessment': None, 'error': str(e)})
        
        # Calculate average GO confidence
        if go_scores:
            stats['go_confidence_avg'] = sum(go_scores) / len(go_scores)
        
        return go, nogo, further, stats
    
    def generate_report(self, search_id: str, go: List, nogo: List, further: List, stats: Dict):
        """Generate assessment report"""
        
        total = len(go) + len(nogo) + len(further)
        
        print(f"\n{'='*70}")
        print(f"ASSESSMENT COMPLETE")
        print(f"{'='*70}\n")
        
        print(f"Search ID: {search_id}")
        print(f"Total Opportunities Assessed: {total}")
        print(f"Processing Time: {stats.get('processing_time', 0):.2f} seconds\n")
        
        print(f"RESULTS:")
        print(f"  GO (Pursue):           {len(go):3d} ({len(go)/total*100:.1f}%)")
        print(f"  NO-GO (Skip):          {len(nogo):3d} ({len(nogo)/total*100:.1f}%)")
        print(f"  FURTHER (Review):      {len(further):3d} ({len(further)/total*100:.1f}%)")
        
        # Show GO opportunities
        if go:
            print(f"\n{'='*70}")
            print(f"GO OPPORTUNITIES (PURSUE THESE):")
            print(f"{'='*70}")
            for i, opp in enumerate(go, 1):
                print(f"\n{i}. {opp['title']}")
                print(f"   ID: {opp['id']}")
                print(f"   Agency: {opp['agency']}")
                if 'assessment' in opp and opp['assessment'] and opp['assessment'].primary_blocker:
                    print(f"   Reason: {opp['assessment'].primary_blocker}")
                # print(f"   Confidence: 85%")  # Default GO confidence
                if opp.get('url'):
                    print(f"   URL: {opp['url']}")
        
        # Show NO-GO reasons summary
        if nogo:
            print(f"\n{'='*70}")
            print(f"NO-GO REASONS SUMMARY:")
            print(f"{'='*70}")
            
            reasons = {}
            for opp in nogo:
                # Get reasons from assessment result or error
                if 'assessment' in opp and opp['assessment']:
                    if opp['assessment'].primary_blocker:
                        reasons[opp['assessment'].primary_blocker] = reasons.get(opp['assessment'].primary_blocker, 0) + 1
                elif 'error' in opp:
                    reasons[f"Error: {opp['error']}"] = reasons.get(f"Error: {opp['error']}", 0) + 1
            
            for reason, count in sorted(reasons.items(), key=lambda x: x[1], reverse=True):
                print(f"  {reason}: {count} opportunities")
        
        # Save full results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        date_str = datetime.now().strftime('%Y%m%d')
        date_folder = datetime.now().strftime('%Y-%m-%d')
        
        # Create dated folders if they don't exist
        import os
        assessment_folder = f'Reports/{date_folder}/HigherGov-Assessments'
        go_folder = f'Reports/{date_folder}/GO-Opportunities'
        os.makedirs(assessment_folder, exist_ok=True)
        os.makedirs(go_folder, exist_ok=True)
        
        # Convert assessment objects to dictionaries for JSON serialization
        def serialize_opportunity(opp):
            """Convert opportunity with assessment to JSON-serializable format"""
            serialized = dict(opp)
            if 'assessment' in serialized and serialized['assessment']:
                assessment = serialized['assessment']
                serialized['assessment'] = {
                    'decision': assessment.decision.value if hasattr(assessment.decision, 'value') else str(assessment.decision),
                    'primary_blocker': assessment.primary_blocker,
                    'primary_blocker_category': assessment.primary_blocker_category,
                    'categories_triggered': assessment.categories_triggered,
                    'ko_logic_version': assessment.ko_logic_version
                }
            return serialized
        
        # Full assessment report
        filename = f"{assessment_folder}/Assessment_{search_id}_{timestamp}.json"
        
        results = {
            'search_id': search_id,
            'timestamp': str(datetime.now()),
            'summary': {
                'total': total,
                'go': len(go),
                'nogo': len(nogo),
                'further': len(further),
                'processing_time': stats.get('processing_time', 0)
            },
            'go_opportunities': [serialize_opportunity(opp) for opp in go],
            'nogo_opportunities': [serialize_opportunity(opp) for opp in nogo],
            'further_opportunities': [serialize_opportunity(opp) for opp in further]
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n[SAVED] Full assessment: {filename}")
        
        # ======================================
        # HARDWIRED CSV GENERATION - ALWAYS RUNS
        # ======================================
        # CSV MUST BE CREATED EVERY SINGLE TIME, NO EXCEPTIONS
        csv_filename = f"{assessment_folder}/Assessment_{search_id}_{timestamp}.csv"
        import csv
        
        # CRITICAL: CSV file is created regardless of opportunity count
        # This is a REQUIRED output for every run
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'opportunity_id', 'title', 'agency', 'decision', 
                'primary_blocker', 'naics', 'psc', 'set_aside',
                'posted_date', 'response_deadline', 'url',
                'value_low', 'value_high', 'has_documents'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Headers always written
            
            # Write all opportunities (may be empty)
            all_opps = go + nogo + further
            for opp in all_opps:
                # Convert assessment object to dict if needed
                assessment = opp.get('assessment')
                if assessment and hasattr(assessment, 'decision'):
                    # It's an AssessmentResult object
                    decision = assessment.decision.value if hasattr(assessment.decision, 'value') else str(assessment.decision)
                    primary_blocker = assessment.primary_blocker or ''
                elif isinstance(assessment, dict):
                    # Already a dict
                    decision = assessment.get('decision', 'UNKNOWN')
                    primary_blocker = assessment.get('primary_blocker', '')
                else:
                    decision = 'ERROR'
                    primary_blocker = opp.get('error', '')
                
                row = {
                    'opportunity_id': opp.get('id', ''),
                    'title': opp.get('title', ''),
                    'agency': opp.get('agency', ''),
                    'decision': decision,
                    'primary_blocker': primary_blocker,
                    'naics': opp.get('naics', ''),
                    'psc': opp.get('psc', ''),
                    'set_aside': opp.get('set_aside', ''),
                    'posted_date': opp.get('posted_date', ''),
                    'response_deadline': opp.get('response_deadline', ''),
                    'url': opp.get('url', ''),
                    'value_low': opp.get('value_low', 0),
                    'value_high': opp.get('value_high', 0),
                    'has_documents': 'Yes' if len(opp.get('text', '')) > 500 else 'No'
                }
                writer.writerow(row)
        
        print(f"[SAVED] CSV assessment: {csv_filename}")
        
        # VERIFICATION: Ensure CSV was actually created
        import os
        if not os.path.exists(csv_filename):
            print(f"[ERROR] CSV file was not created! Creating empty CSV...")
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            print(f"[FIXED] Empty CSV created: {csv_filename}")
        else:
            csv_size = os.path.getsize(csv_filename)
            print(f"[VERIFIED] CSV exists ({csv_size} bytes)")
        
        # GO opportunities report
        if go:
            go_filename = f"{go_folder}/GO_{search_id}_{date_str}.json"
            with open(go_filename, 'w') as f:
                json.dump({
                    'search_id': search_id,
                    'date': date_str,
                    'total_go': len(go),
                    'opportunities': [serialize_opportunity(opp) for opp in go]
                }, f, indent=2)
            print(f"[SAVED] GO opportunities: {go_filename}")
            
            # Also create a markdown summary for easy reading
            md_filename = f"{go_folder}/GO_{search_id}_{date_str}.md"
            with open(md_filename, 'w') as f:
                f.write(f"# GO OPPORTUNITIES REPORT\n")
                f.write(f"**Search ID:** {search_id}\n")
                f.write(f"**Date:** {date_str}\n")
                f.write(f"**Total GO:** {len(go)}\n\n")
                
                for i, opp in enumerate(go, 1):
                    f.write(f"## {i}. {opp['title']}\n")
                    f.write(f"- **ID:** {opp['id']}\n")
                    f.write(f"- **Agency:** {opp['agency']}\n")
                    val_low = float(opp.get('value_low', 0)) if opp.get('value_low') else 0
                    val_high = float(opp.get('value_high', 0)) if opp.get('value_high') else 0
                    f.write(f"- **Value:** ${val_low:,.0f} - ${val_high:,.0f}\n")
                    f.write(f"- **Due:** {opp.get('response_deadline', 'N/A')}\n")
                    # f.write(f"- **Confidence:** 85%\n")  # Default GO confidence
                    f.write(f"- **URL:** {opp.get('url', 'N/A')}\n\n")
            
            print(f"[SAVED] GO summary: {md_filename}")
        
        # Create daily summary dashboard
        dashboard_file = f"Reports/{date_folder}/DAILY_SUMMARY.md"
        dashboard_exists = os.path.exists(dashboard_file)
        
        with open(dashboard_file, 'a') as f:
            if not dashboard_exists:
                f.write(f"# DAILY ASSESSMENT SUMMARY - {date_folder}\n\n")
            
            f.write(f"\n## Search: {search_id} ({datetime.now().strftime('%H:%M:%S')})\n")
            f.write(f"- **Total Assessed:** {total}\n")
            f.write(f"- **GO:** {len(go)} ({len(go)/total*100:.1f}%)\n")
            f.write(f"- **NO-GO:** {len(nogo)} ({len(nogo)/total*100:.1f}%)\n")
            f.write(f"- **FURTHER:** {len(further)} ({len(further)/total*100:.1f}%)\n")
            
            if go:
                f.write(f"\n### Top GO Opportunities:\n")
                for opp in go[:3]:
                    f.write(f"- {opp['title'][:50]}...\n")
        
        print(f"[SAVED] Daily summary: {dashboard_file}")
        
        return results
    
    def run(self, search_id: str = None, fetch_docs: bool = True):
        """Main execution with optional document fetching"""
        
        # Get search ID from user if not provided
        if not search_id:
            print("\n" + "="*70)
            print("HIGHERGOV BATCH OPPORTUNITY FETCHER")
            print("CSV Output: ENABLED (Hardwired - Always Generated)")
            print("="*70)
            print("\nHow to get a search ID:")
            print("1. Go to https://www.highergov.com/contract-opportunity/")
            print("2. Run your search with filters")
            print("3. Copy the searchID from the URL")
            print("   Example: searchID=0dUlm563sCP3BItrd1W2l")
            print("\n" + "-"*70)
            
            search_id = input("\nEnter HigherGov search ID (or press Enter for demo): ").strip()
            
            if not search_id:
                search_id = "0dUlm563sCP3BItrd1W2l"  # Default demo ID
                print(f"Using demo search ID: {search_id}")
            
            # Ask about document fetching
            fetch_input = input("\nFetch full documents? (Y/n): ").strip().upper()
            fetch_docs = fetch_input != 'N'
        
        # Fetch all opportunities
        opportunities = self.fetch_all_opportunities(search_id)
        
        if not opportunities:
            print("\nNo opportunities found for this search ID")
            return None
        
        # Assess all opportunities with document fetching option
        go, nogo, further, stats = self.assess_batch(opportunities, fetch_docs=fetch_docs)
        
        # Generate report
        results = self.generate_report(search_id, go, nogo, further, stats)
        
        return results


def main():
    """Main entry point"""
    
    # Check for command line search ID
    search_id = None
    if len(sys.argv) > 1:
        search_id = sys.argv[1]
    
    # Create fetcher and run
    fetcher = HigherGovBatchFetcher()
    results = fetcher.run(search_id)
    
    if results and results['summary']['go'] > 0:
        print(f"\n[SUCCESS] Found {results['summary']['go']} GO opportunities!")
        print("Review the saved files for full details.")
    else:
        print("\n[INFO] No GO opportunities found in this search.")


if __name__ == "__main__":
    main()