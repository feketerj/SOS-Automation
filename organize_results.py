#!/usr/bin/env python3
"""
SOS Pipeline Results Organizer
Creates organized folder structure with opportunities sorted by decision type
"""

import json
import glob
import os
import shutil
from datetime import datetime
from pathlib import Path

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

def create_folder_structure():
    """Create organized folder structure"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_folder = f"SOS_Assessment_Results_{timestamp}"
    
    # Create main folder and subfolders
    folders = {
        'base': base_folder,
        'go': os.path.join(base_folder, "1_GO_Opportunities"),
        'needs_analysis': os.path.join(base_folder, "2_NEEDS_ANALYSIS"),
        'no_go': os.path.join(base_folder, "3_NO_GO_Rejected"),
        'summary': os.path.join(base_folder, "0_SUMMARY_REPORTS")
    }
    
    for folder in folders.values():
        os.makedirs(folder, exist_ok=True)
    
    return folders

def create_opportunity_file(result, folder_path):
    """Create individual opportunity file with all relevant info"""
    opp = result['original_opportunity']
    solicitation_id = opp.get('source_id', result.get('opportunity_id', 'Unknown'))
    title = result.get('opportunity_title', opp.get('title', 'No title'))
    decision = result['final_decision']
    
    # Clean filename
    safe_id = "".join(c for c in solicitation_id if c.isalnum() or c in ('-', '_')).rstrip()
    filename = f"{safe_id}_{decision}.txt"
    filepath = os.path.join(folder_path, filename)
    
    # Get key information
    agency_info = opp.get('agency', {})
    agency_name = agency_info.get('agency_name', 'Unknown Agency') if isinstance(agency_info, dict) else str(agency_info)
    
    highergov_link = opp.get('path', 'No link available')
    sam_link = opp.get('source_path', 'No SAM link')
    response_date = opp.get('response_date', 'Not specified')
    posted_date = opp.get('posted_date', 'Not specified')
    description = opp.get('description_text', opp.get('description', 'No description available'))
    
    # Format checklist results
    checklist_results = []
    for check in result.get('assessment_details', []):
        status = "✅ PASS" if "PASS" in str(check['decision']) else "❌ FAIL" if "NO-GO" in str(check['decision']) else "⚠️ REVIEW"
        checklist_results.append(f"   {status} {check['check_name']}: {check['reason']}")
        if check.get('quote') and check['quote'].strip():
            quote_short = check['quote'][:150] + "..." if len(check['quote']) > 150 else check['quote']
            checklist_results.append(f"        Evidence: \"{quote_short}\"")
    
    checklist_text = "\n".join(checklist_results)
    
    # Create file content based on decision type
    if decision == 'GO':
        content = f"""
================================================================================
🎯 VIABLE OPPORTUNITY - READY FOR PURSUIT
================================================================================

📋 OPPORTUNITY DETAILS:
   • Solicitation ID: {solicitation_id}
   • Title: {title}
   • Agency: {agency_name}
   • Response Due: {response_date}
   • Posted Date: {posted_date}
   • Decision: {decision}

🔗 DIRECT LINKS:
   • SAM.gov (Primary): {sam_link}
   • HigherGov: {highergov_link}

✅ SOS ASSESSMENT RESULTS:
{checklist_text}

📄 OPPORTUNITY DESCRIPTION:
{description}

⚡ NEXT ACTIONS:
   1. Click SAM.gov link above to review full solicitation
   2. Assess technical requirements against SOS capabilities
   3. Check response deadline: {response_date}
   4. Make bid/no-bid decision
   5. Prepare proposal if pursuing

💡 WHY THIS PASSED:
This opportunity met all SOS criteria - it's aviation-related, doesn't require 
military source approval (SAR), no security clearances needed, and matches 
your business capabilities.
"""
    
    elif decision == 'NEEDS ANALYSIS':
        analysis_reason = "Manual review required"
        analysis_context = "Review full solicitation for details"
        
        for check in result.get('assessment_details', []):
            if 'NEEDS ANALYSIS' in str(check['decision']):
                analysis_reason = check.get('reason', analysis_reason)
                analysis_context = check.get('quote', analysis_context)
                break
        
        content = f"""
================================================================================
⚠️ MANUAL ANALYSIS REQUIRED - EXPERT REVIEW NEEDED
================================================================================

📋 OPPORTUNITY DETAILS:
   • Solicitation ID: {solicitation_id}
   • Title: {title}
   • Agency: {agency_name}
   • Response Due: {response_date}
   • Posted Date: {posted_date}
   • Decision: {decision}

🔗 REVIEW LINKS:
   • SAM.gov (Primary): {sam_link}
   • HigherGov: {highergov_link}

⚠️ WHY MANUAL REVIEW IS NEEDED:
   Reason: {analysis_reason}
   Context: {analysis_context[:300]}{'...' if len(analysis_context) > 300 else ''}

🔍 ASSESSMENT RESULTS:
{checklist_text}

📄 OPPORTUNITY DESCRIPTION:
{description}

🎯 EXPERT ANALYSIS REQUIRED:
   □ Review full solicitation at SAM.gov link above
   □ Assess platform compatibility and technical requirements
   □ Determine if opportunity matches SOS capabilities
   □ Make final GO/NO-GO decision
   □ Document decision rationale for future reference

⏰ RESPONSE DEADLINE: {response_date}
"""
    
    else:  # NO-GO
        rejection_reason = "Unknown"
        rejection_quote = "No details available"
        
        for check in result.get('assessment_details', []):
            if 'NO-GO' in str(check['decision']):
                rejection_reason = check.get('reason', rejection_reason)
                rejection_quote = check.get('quote', rejection_quote)
                break
        
        content = f"""
================================================================================
❌ REJECTED OPPORTUNITY - FILTERED OUT
================================================================================

📋 OPPORTUNITY DETAILS:
   • Solicitation ID: {solicitation_id}
   • Title: {title}
   • Agency: {agency_name}
   • Response Due: {response_date}
   • Posted Date: {posted_date}
   • Decision: {decision}

🔗 REFERENCE LINKS:
   • SAM.gov: {sam_link}
   • HigherGov: {highergov_link}

❌ REJECTION REASON:
   Primary Issue: {rejection_reason}
   Evidence: "{rejection_quote[:300]}{'...' if len(rejection_quote) > 300 else ''}"

🔍 FULL ASSESSMENT RESULTS:
{checklist_text}

📄 OPPORTUNITY DESCRIPTION:
{description[:500]}{'...' if len(description) > 500 else ''}

💡 WHY THIS WAS REJECTED:
This opportunity was filtered out because it doesn't meet SOS business criteria.
Common rejection reasons include:
• Military Source Approval Required (SAR)
• Security clearance requirements
• Not aviation-related
• Sole source to another company
• Platform restrictions

This filtering saves you time by eliminating opportunities that wouldn't be 
a good fit for SourceOne Spares.
"""
    
    # Write the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

def create_summary_files(results, summary_folder):
    """Create summary files in the summary folder"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    go_count = sum(1 for r in results if r['final_decision'] == 'GO')
    no_go_count = sum(1 for r in results if r['final_decision'] == 'NO-GO')
    needs_analysis_count = sum(1 for r in results if r['final_decision'] == 'NEEDS ANALYSIS')
    total = len(results)
    
    # Executive Summary
    summary_content = f"""
================================================================================
SOS OPPORTUNITY ASSESSMENT PIPELINE - EXECUTIVE SUMMARY
Generated: {timestamp}
================================================================================

📊 RESULTS OVERVIEW:
• Total Opportunities Processed: {total}
• 🎯 Viable Opportunities (GO): {go_count} ({go_count/total*100:.1f}%)
• ⚠️ Need Manual Review: {needs_analysis_count} ({needs_analysis_count/total*100:.1f}%)
• ❌ Rejected (NO-GO): {no_go_count} ({no_go_count/total*100:.1f}%)

📁 FOLDER ORGANIZATION:
• 1_GO_Opportunities: {go_count} files - Ready to pursue
• 2_NEEDS_ANALYSIS: {needs_analysis_count} files - Require expert review
• 3_NO_GO_Rejected: {no_go_count} files - Filtered out (reference only)

⚡ IMMEDIATE ACTIONS:
1. Start with folder "1_GO_Opportunities" - these are your best prospects
2. Review folder "2_NEEDS_ANALYSIS" - make expert decisions on these
3. Use folder "3_NO_GO_Rejected" to understand what was filtered out

💡 HOW TO USE THESE RESULTS:
• Each file contains complete opportunity details and direct SAM.gov links
• GO opportunities are ready for immediate pursuit
• Files are named with solicitation ID for easy reference
• All assessment reasoning is documented for transparency

📈 BUSINESS IMPACT:
• Time Saved: ~{total * 5} minutes (vs manual review of all opportunities)
• Focus: You can concentrate on {go_count} high-quality prospects
• Efficiency: {go_count/total*100:.1f}% identification rate

🚀 NEXT STEPS:
1. Open "1_GO_Opportunities" folder
2. Review each opportunity file
3. Click SAM.gov links for full solicitation details
4. Make bid/no-bid decisions based on your capabilities
"""
    
    with open(os.path.join(summary_folder, "README_START_HERE.txt"), 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    # Quick Reference Guide
    quick_ref = f"""
================================================================================
QUICK REFERENCE GUIDE - SOS ASSESSMENT RESULTS
================================================================================

📁 FOLDER GUIDE:

🎯 1_GO_Opportunities ({go_count} files)
   • These passed all SOS filters
   • Ready for immediate pursuit
   • Each file has SAM.gov links and full details
   • Priority: HIGH - Review these first

⚠️ 2_NEEDS_ANALYSIS ({needs_analysis_count} files)
   • Require expert judgment
   • Platform or capability questions
   • Review and make manual GO/NO-GO decision
   • Priority: MEDIUM - Expert review needed

❌ 3_NO_GO_Rejected ({no_go_count} files)
   • Filtered out for good reasons
   • Reference only - understand why rejected
   • Priority: LOW - Review only if curious

📋 FILE NAMING:
Files are named: [SolicitationID]_[Decision].txt
Example: FA8118RFIMAC1_GO.txt

🔗 WHAT'S IN EACH FILE:
• Complete opportunity details
• Direct SAM.gov and HigherGov links
• Full SOS assessment checklist results
• Specific action items
• Response deadlines

⚡ WORKFLOW:
1. Open "1_GO_Opportunities" folder
2. Open each file and click SAM.gov link
3. Review full solicitation
4. Make bid/no-bid decision
5. Note response deadlines
"""
    
    with open(os.path.join(summary_folder, "Quick_Reference_Guide.txt"), 'w', encoding='utf-8') as f:
        f.write(quick_ref)

def main():
    print("Loading assessment results...")
    results = load_results()
    
    if not results:
        print("No JSON files found in output directory!")
        return
    
    print(f"Loaded {len(results)} opportunities. Creating organized folder structure...")
    
    # Create folder structure
    folders = create_folder_structure()
    
    # Sort results by decision type
    go_count = 0
    needs_analysis_count = 0
    no_go_count = 0
    
    for result in results:
        decision = result['final_decision']
        
        if decision == 'GO':
            filename = create_opportunity_file(result, folders['go'])
            go_count += 1
            print(f"Created GO opportunity: {filename}")
            
        elif decision == 'NEEDS ANALYSIS':
            filename = create_opportunity_file(result, folders['needs_analysis'])
            needs_analysis_count += 1
            print(f"Created NEEDS ANALYSIS: {filename}")
            
        else:  # NO-GO
            filename = create_opportunity_file(result, folders['no_go'])
            no_go_count += 1
    
    # Create summary files
    create_summary_files(results, folders['summary'])
    
    print(f"\n🎯 ORGANIZED RESULTS CREATED!")
    print(f"📁 Main Folder: {folders['base']}")
    print(f"✅ GO Opportunities: {go_count} files in '1_GO_Opportunities'")
    print(f"⚠️ Needs Analysis: {needs_analysis_count} files in '2_NEEDS_ANALYSIS'")
    print(f"❌ Rejected: {no_go_count} files in '3_NO_GO_Rejected'")
    print(f"📋 Summary: Guide files in '0_SUMMARY_REPORTS'")
    print(f"\n🚀 START HERE: Open {folders['base']} folder and read 'README_START_HERE.txt'")

if __name__ == "__main__":
    main()
