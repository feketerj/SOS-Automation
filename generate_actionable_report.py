#!/usr/bin/env python3
"""
SOS Pipeline Results Summary Generator - Enhanced Version
Creates actionable reports with all critical business information
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

def format_checklist_results(assessment_details):
    """Format the checklist results in a readable way"""
    checklist = []
    for check in assessment_details:
        status = "✅ PASS" if "PASS" in str(check['decision']) else "❌ FAIL" if "NO-GO" in str(check['decision']) else "⚠️ REVIEW"
        checklist.append(f"   {status} {check['check_name']}: {check['reason']}")
        if check.get('quote') and check['quote'].strip():
            quote_short = check['quote'][:100] + "..." if len(check['quote']) > 100 else check['quote']
            checklist.append(f"        Quote: \"{quote_short}\"")
    return "\n".join(checklist)

def generate_actionable_summary(results):
    """Generate executive summary with actionable intelligence"""
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
SOS OPPORTUNITY ASSESSMENT PIPELINE - ACTIONABLE SUMMARY
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================================================================================

📊 PIPELINE PERFORMANCE:
• Total Opportunities Analyzed: {total}
• 🎯 VIABLE OPPORTUNITIES: {go_count} ({go_count/total*100:.1f}%)
• ❌ REJECTED OPPORTUNITIES: {no_go_count} ({no_go_count/total*100:.1f}%)
• 🔍 NEEDS MANUAL REVIEW: {needs_analysis_count} ({needs_analysis_count/total*100:.1f}%)

🚫 TOP REJECTION REASONS:
"""
    
    for reason, count in sorted(rejection_reasons.items(), key=lambda x: x[1], reverse=True)[:5]:
        percentage = count/no_go_count*100 if no_go_count > 0 else 0
        report += f"   • {reason}: {count} rejections ({percentage:.1f}% of rejections)\n"
    
    report += f"""

📈 BUSINESS IMPACT:
• You can focus on {go_count} qualified opportunities instead of reviewing {total}
• Time savings: ~{total * 5} minutes saved (5 min per manual review)
• Success rate: {go_count/total*100:.1f}% identification rate

⏰ NEXT ACTIONS:
1. Review the {go_count} viable opportunities below
2. Follow up on the {needs_analysis_count} opportunities needing analysis
3. Consider scaling to process all 900+ opportunities in your saved search
"""
    
    return report

def generate_viable_opportunities_actionable(results):
    """Generate actionable report of viable opportunities"""
    go_results = [r for r in results if r['final_decision'] == 'GO']
    
    report = f"""
================================================================================
🎯 VIABLE OPPORTUNITIES - READY FOR PURSUIT ({len(go_results)} Total)
================================================================================

"""
    
    for i, result in enumerate(go_results, 1):
        opp = result['original_opportunity']
        
        # Extract key information
        solicitation_id = opp.get('source_id', result.get('opportunity_id', 'Unknown'))
        title = result.get('opportunity_title', opp.get('title', 'No title'))
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
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPPORTUNITY #{i}: {solicitation_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 BASIC INFORMATION:
   • Solicitation ID: {solicitation_id}
   • Title: {title}
   • Agency: {agency_name}
   • Response Due: {response_date}
   • Posted Date: {posted_date}

🔗 LINKS FOR REVIEW:
   • HigherGov: {highergov_link}
   • SAM.gov: {sam_link}

✅ SOS CHECKLIST RESULTS:
{format_checklist_results(result.get('assessment_details', []))}

📄 OPPORTUNITY DESCRIPTION:
{description[:500]}{'...' if len(description) > 500 else ''}

⚡ ACTION REQUIRED:
   1. Review full solicitation at links above
   2. Assess technical requirements and specifications
   3. Determine bid/no-bid decision based on SOS capabilities
   4. Note response deadline: {response_date}

"""
    
    return report

def generate_rejection_details(results):
    """Generate detailed rejection analysis for learning"""
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
❌ REJECTION ANALYSIS - UNDERSTANDING THE FILTERS
================================================================================

This section helps you understand why {len(no_go_results)} opportunities were filtered out.
Review these to validate the pipeline logic and identify potential improvements.

"""
    
    for reason, rejected_opps in sorted(by_reason.items(), key=lambda x: len(x[1]), reverse=True):
        report += f"""
🚫 {reason.upper()}: {len(rejected_opps)} Rejections
{'-' * 80}
"""
        
        # Show top 3 examples for each rejection reason
        for i, result in enumerate(rejected_opps[:3], 1):
            opp = result['original_opportunity']
            solicitation_id = opp.get('source_id', result.get('opportunity_id', 'Unknown'))
            title = result.get('opportunity_title', opp.get('title', 'No title'))
            
            blocking_check = None
            for check in result.get('assessment_details', []):
                if 'NO-GO' in str(check['decision']):
                    blocking_check = check
                    break
            
            sam_link = opp.get('source_path', 'No link')
            
            report += f"""
Example {i}: {solicitation_id}
   Title: {title[:80]}{'...' if len(title) > 80 else ''}
   Reason: {blocking_check['reason'] if blocking_check else 'Unknown'}
   Evidence: "{blocking_check['quote'][:150] if blocking_check and blocking_check['quote'] else 'No evidence'}{'...' if blocking_check and len(blocking_check.get('quote', '')) > 150 else ''}"
   Link: {sam_link}

"""
        
        if len(rejected_opps) > 3:
            report += f"   ... and {len(rejected_opps) - 3} more similar rejections\n"
        
        report += "\n"
    
    return report

def generate_manual_review_actionable(results):
    """Generate actionable manual review list"""
    needs_analysis = [r for r in results if r['final_decision'] == 'NEEDS ANALYSIS']
    
    if not needs_analysis:
        return """
================================================================================
🔍 MANUAL REVIEW REQUIRED: None
================================================================================
All opportunities received clear GO/NO-GO decisions. No manual analysis needed.
"""
    
    report = f"""
================================================================================
🔍 MANUAL REVIEW REQUIRED - EXPERT ANALYSIS NEEDED ({len(needs_analysis)} Total)
================================================================================

These opportunities require your expertise to make the final determination:

"""
    
    for i, result in enumerate(needs_analysis, 1):
        opp = result['original_opportunity']
        solicitation_id = opp.get('source_id', result.get('opportunity_id', 'Unknown'))
        title = result.get('opportunity_title', opp.get('title', 'No title'))
        agency_info = opp.get('agency', {})
        agency_name = agency_info.get('agency_name', 'Unknown Agency') if isinstance(agency_info, dict) else str(agency_info)
        
        analysis_check = None
        for check in result.get('assessment_details', []):
            if 'NEEDS ANALYSIS' in str(check['decision']):
                analysis_check = check
                break
        
        highergov_link = opp.get('path', 'No link available')
        sam_link = opp.get('source_path', 'No SAM link')
        description = opp.get('description_text', opp.get('description', 'No description available'))
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MANUAL REVIEW #{i}: {solicitation_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 BASIC INFORMATION:
   • Solicitation ID: {solicitation_id}
   • Title: {title}
   • Agency: {agency_name}
   • Response Due: {opp.get('response_date', 'Not specified')}

🔗 REVIEW LINKS:
   • HigherGov: {highergov_link}
   • SAM.gov: {sam_link}

⚠️ ANALYSIS REQUIRED:
   Reason: {analysis_check['reason'] if analysis_check else 'Manual review flagged'}
   Context: "{analysis_check['quote'][:200] if analysis_check and analysis_check['quote'] else 'Review full solicitation for details'}{'...' if analysis_check and len(analysis_check.get('quote', '')) > 200 else ''}"

📄 OPPORTUNITY DETAILS:
{description[:400]}{'...' if len(description) > 400 else ''}

🎯 EXPERT DECISION NEEDED:
   □ Review technical requirements and platform compatibility
   □ Assess SOS capability match
   □ Make final GO/NO-GO determination
   □ Document decision rationale

"""
    
    return report

def main():
    print("Loading pipeline results...")
    results = load_results()
    
    if not results:
        print("No JSON files found in output directory!")
        return
    
    print(f"Loaded {len(results)} opportunities. Generating actionable reports...")
    
    # Generate timestamp for files
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Generate actionable reports
    summary = generate_actionable_summary(results)
    with open(f"SOS_ACTIONABLE_Summary_{timestamp}.txt", 'w', encoding='utf-8') as f:
        f.write(summary)
    
    viable_report = generate_viable_opportunities_actionable(results)
    with open(f"SOS_VIABLE_Opportunities_{timestamp}.txt", 'w', encoding='utf-8') as f:
        f.write(viable_report)
    
    rejection_report = generate_rejection_details(results)
    with open(f"SOS_REJECTION_Analysis_{timestamp}.txt", 'w', encoding='utf-8') as f:
        f.write(rejection_report)
    
    manual_report = generate_manual_review_actionable(results)
    with open(f"SOS_MANUAL_Review_{timestamp}.txt", 'w', encoding='utf-8') as f:
        f.write(manual_report)
    
    # Combined actionable report
    combined = summary + viable_report + manual_report + rejection_report
    with open(f"SOS_COMPLETE_Actionable_Report_{timestamp}.txt", 'w', encoding='utf-8') as f:
        f.write(combined)
    
    print(f"\n🎯 ACTIONABLE REPORTS GENERATED!")
    print(f"📊 Executive Summary: SOS_ACTIONABLE_Summary_{timestamp}.txt")
    print(f"✅ Viable Opportunities: SOS_VIABLE_Opportunities_{timestamp}.txt") 
    print(f"🔍 Manual Review: SOS_MANUAL_Review_{timestamp}.txt")
    print(f"❌ Rejection Analysis: SOS_REJECTION_Analysis_{timestamp}.txt")
    print(f"📋 Complete Report: SOS_COMPLETE_Actionable_Report_{timestamp}.txt")
    
    # Print summary to console
    print(summary)

if __name__ == "__main__":
    main()
