#!/usr/bin/env python3
"""
SOS Pipeline Results Summary Generator
Creates human-readable reports from JSON output files
"""

import json
import glob
import os
from datetime import datetime
from collections import defaultdict

def load_results():
    """Load all JSON results from output directory"""
    results = []
    json_files = glob.glob("output/*.json")
    
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                results.append(data)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return results

def generate_summary_report(results):
    """Generate executive summary"""
    total = len(results)
    go_count = sum(1 for r in results if r['final_decision'] == 'GO')
    no_go_count = sum(1 for r in results if r['final_decision'] == 'NO-GO')
    needs_analysis_count = sum(1 for r in results if r['final_decision'] == 'NEEDS ANALYSIS')
    
    # Analyze rejection reasons
    rejection_reasons = defaultdict(int)
    for result in results:
        if result['final_decision'] == 'NO-GO' and result.get('assessment_details'):
            for check in result['assessment_details']:
                if 'NO-GO' in str(check['decision']):
                    rejection_reasons[check['check_name']] += 1
                    break  # Only count the first blocking reason
    
    report = f"""
================================================================================
SOS OPPORTUNITY ASSESSMENT PIPELINE - EXECUTIVE SUMMARY
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================================================================================

OVERALL RESULTS:
• Total Opportunities Processed: {total}
• GO (Viable): {go_count} ({go_count/total*100:.1f}%)
• NO-GO (Rejected): {no_go_count} ({no_go_count/total*100:.1f}%)
• NEEDS ANALYSIS (Manual Review): {needs_analysis_count} ({needs_analysis_count/total*100:.1f}%)

TOP REJECTION REASONS:
"""
    
    for reason, count in sorted(rejection_reasons.items(), key=lambda x: x[1], reverse=True):
        percentage = count/no_go_count*100 if no_go_count > 0 else 0
        report += f"• {reason}: {count} rejections ({percentage:.1f}% of all rejections)\n"
    
    return report

def generate_go_opportunities_report(results):
    """Generate detailed report of GO opportunities"""
    go_results = [r for r in results if r['final_decision'] == 'GO']
    
    report = f"""
================================================================================
VIABLE OPPORTUNITIES (GO DECISIONS) - DETAILED REVIEW
================================================================================
Found {len(go_results)} viable opportunities for SourceOne Spares:

"""
    
    for i, result in enumerate(go_results, 1):
        opp = result['original_opportunity']
        report += f"""
{i}. SOLICITATION: {opp.get('solicitation_number', 'N/A')}
   Title: {result.get('opportunity_title', 'N/A')[:100]}{'...' if len(result.get('opportunity_title', '')) > 100 else ''}
   Agency: {opp.get('agency', 'N/A')}
   Due Date: {opp.get('response_date', 'N/A')}
   Posted: {opp.get('posted_date', 'N/A')}
   
   WHY IT PASSED: All critical filters passed
   - ✓ Aviation-related opportunity
   - ✓ No SAR requirements detected
   - ✓ No security clearance required  
   - ✓ Not sole source to another company
   - ✓ No prohibited certifications required
   - ✓ Platform assessment favorable
   
   DESCRIPTION EXCERPT:
   {opp.get('description', 'No description')[:300]}{'...' if len(opp.get('description', '')) > 300 else ''}
   
   ----------------------------------------
"""
    
    return report

def generate_rejection_analysis(results):
    """Generate detailed analysis of rejections"""
    no_go_results = [r for r in results if r['final_decision'] == 'NO-GO']
    
    # Group by rejection reason
    by_reason = defaultdict(list)
    for result in no_go_results:
        if result.get('assessment_details'):
            for check in result['assessment_details']:
                if 'NO-GO' in str(check['decision']):
                    by_reason[check['check_name']].append(result)
                    break
    
    report = f"""
================================================================================
REJECTION ANALYSIS - WHY OPPORTUNITIES WERE FILTERED OUT
================================================================================
Analyzed {len(no_go_results)} rejected opportunities:

"""
    
    for reason, rejected_opps in sorted(by_reason.items(), key=lambda x: len(x[1]), reverse=True):
        report += f"""
{reason.upper()} REJECTIONS: {len(rejected_opps)} opportunities
{'-' * 60}
"""
        
        # Show top 5 examples for each rejection reason
        for i, result in enumerate(rejected_opps[:5], 1):
            opp = result['original_opportunity']
            blocking_check = None
            for check in result.get('assessment_details', []):
                if 'NO-GO' in str(check['decision']):
                    blocking_check = check
                    break
            
            report += f"""
Example {i}: {opp.get('solicitation_number', 'N/A')}
Title: {result.get('opportunity_title', 'N/A')[:80]}{'...' if len(result.get('opportunity_title', '')) > 80 else ''}
Reason: {blocking_check['reason'] if blocking_check else 'Unknown'}
Quote: "{blocking_check['quote'][:150] if blocking_check and blocking_check['quote'] else 'No quote available'}{'...' if blocking_check and len(blocking_check['quote']) > 150 else ''}"

"""
        
        if len(rejected_opps) > 5:
            report += f"... and {len(rejected_opps) - 5} more similar rejections\n"
        
        report += "\n"
    
    return report

def generate_needs_analysis_report(results):
    """Generate report for opportunities needing manual analysis"""
    needs_analysis = [r for r in results if r['final_decision'] == 'NEEDS ANALYSIS']
    
    if not needs_analysis:
        return "\n================================================================================\nNEEDS ANALYSIS OPPORTUNITIES: None found\n================================================================================\n"
    
    report = f"""
================================================================================
OPPORTUNITIES REQUIRING MANUAL ANALYSIS
================================================================================
Found {len(needs_analysis)} opportunities requiring expert review:

"""
    
    for i, result in enumerate(needs_analysis, 1):
        opp = result['original_opportunity']
        analysis_check = None
        for check in result.get('assessment_details', []):
            if 'NEEDS ANALYSIS' in str(check['decision']):
                analysis_check = check
                break
        
        report += f"""
{i}. SOLICITATION: {opp.get('solicitation_number', 'N/A')}
   Title: {result.get('opportunity_title', 'N/A')}
   Agency: {opp.get('agency', 'N/A')}
   Due Date: {opp.get('response_date', 'N/A')}
   
   ANALYSIS REQUIRED: {analysis_check['reason'] if analysis_check else 'Unknown reason'}
   Context: "{analysis_check['quote'][:200] if analysis_check and analysis_check['quote'] else 'No context available'}{'...' if analysis_check and len(analysis_check['quote']) > 200 else ''}"
   
   DESCRIPTION:
   {opp.get('description', 'No description')[:400]}{'...' if len(opp.get('description', '')) > 400 else ''}
   
   ----------------------------------------
"""
    
    return report

def main():
    print("Loading results from JSON files...")
    results = load_results()
    
    if not results:
        print("No JSON files found in output directory!")
        return
    
    print(f"Loaded {len(results)} opportunities. Generating reports...")
    
    # Generate all reports
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Executive Summary
    summary = generate_summary_report(results)
    with open(f"SOS_Executive_Summary_{timestamp}.txt", 'w', encoding='utf-8') as f:
        f.write(summary)
    
    # GO Opportunities Report
    go_report = generate_go_opportunities_report(results)
    with open(f"SOS_Viable_Opportunities_{timestamp}.txt", 'w', encoding='utf-8') as f:
        f.write(go_report)
    
    # Rejection Analysis
    rejection_report = generate_rejection_analysis(results)
    with open(f"SOS_Rejection_Analysis_{timestamp}.txt", 'w', encoding='utf-8') as f:
        f.write(rejection_report)
    
    # Needs Analysis Report
    needs_report = generate_needs_analysis_report(results)
    with open(f"SOS_Manual_Review_Required_{timestamp}.txt", 'w', encoding='utf-8') as f:
        f.write(needs_report)
    
    # Combined comprehensive report
    comprehensive = summary + go_report + rejection_report + needs_report
    with open(f"SOS_Complete_Assessment_Report_{timestamp}.txt", 'w', encoding='utf-8') as f:
        f.write(comprehensive)
    
    print(f"\n✅ Reports generated successfully!")
    print(f"📊 Executive Summary: SOS_Executive_Summary_{timestamp}.txt")
    print(f"🎯 Viable Opportunities: SOS_Viable_Opportunities_{timestamp}.txt") 
    print(f"❌ Rejection Analysis: SOS_Rejection_Analysis_{timestamp}.txt")
    print(f"🔍 Manual Review Required: SOS_Manual_Review_Required_{timestamp}.txt")
    print(f"📋 Complete Report: SOS_Complete_Assessment_Report_{timestamp}.txt")
    
    # Also print executive summary to console
    print(summary)

if __name__ == "__main__":
    main()
