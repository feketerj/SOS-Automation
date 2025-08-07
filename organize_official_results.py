"""
Organize SOS Assessment Results into Folder Structure
Based on official SOS filter decisions
"""

import json
import os
from datetime import datetime
from pathlib import Path

def organize_results():
    """Create organized folder structure from SOS assessment results"""
    
    # Create timestamp for folder name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_folder = f"SOS_Assessment_Results_{timestamp}"
    
    # Create main folders
    folders = {
        'GO': os.path.join(base_folder, '01_GO_Opportunities'),
        'NO-GO': os.path.join(base_folder, '02_NO-GO_Opportunities'),
        'NEEDS ANALYSIS': os.path.join(base_folder, '03_NEEDS_ANALYSIS')
    }
    
    for folder in folders.values():
        Path(folder).mkdir(parents=True, exist_ok=True)
    
    # Process results
    results_summary = {
        'GO': [],
        'NO-GO': [],
        'NEEDS ANALYSIS': []
    }
    
    # Read all assessment files
    for filename in os.listdir('output'):
        if filename.endswith('.json'):
            try:
                with open(os.path.join('output', filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                decision = data.get('final_decision', 'UNKNOWN')
                if decision not in folders:
                    decision = 'NO-GO'  # Default unknown to NO-GO
                
                # Extract opportunity info
                opp = data.get('original_opportunity', {})
                opp_id = data.get('opportunity_id', 'UNKNOWN')
                title = data.get('opportunity_title', 'No Title')
                
                # Create individual opportunity file
                safe_filename = "".join(c for c in f"{opp_id}_{title}" if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_filename = safe_filename[:100]  # Limit length
                
                opportunity_file = {
                    'id': opp_id,
                    'title': title,
                    'decision': decision,
                    'sam_url': f"https://sam.gov/opp/{opp.get('source_id', '')}/view" if opp.get('source_id') else 'No URL',
                    'posted_date': opp.get('posted_date', 'Unknown'),
                    'description': opp.get('description_text', 'No description')[:1000],
                    'assessment_summary': {
                        'phase_0': data.get('phase_0', {}),
                        'phase_1': data.get('phase_1', {}),
                        'reasoning': data.get('reasoning', [])
                    },
                    'next_steps': get_next_steps(decision, data)
                }
                
                # Save individual file
                output_path = os.path.join(folders[decision], f"{safe_filename}.json")
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(opportunity_file, f, indent=2, ensure_ascii=False)
                
                # Add to summary
                results_summary[decision].append({
                    'id': opp_id,
                    'title': title,
                    'file': f"{safe_filename}.json"
                })
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue
    
    # Create summary report
    create_summary_report(base_folder, results_summary)
    
    # Create action items
    create_action_items(base_folder, results_summary)
    
    print(f"✅ Results organized in folder: {base_folder}")
    print(f"📊 Summary: {len(results_summary['GO'])} GO, {len(results_summary['NO-GO'])} NO-GO, {len(results_summary['NEEDS ANALYSIS'])} NEEDS ANALYSIS")
    
    return base_folder

def get_next_steps(decision, data):
    """Generate next steps based on decision"""
    if decision == 'GO':
        return [
            "1. Review opportunity details and requirements",
            "2. Prepare capability statement",
            "3. Register in SAM.gov if not already registered", 
            "4. Submit proposal by deadline",
            "5. Follow up on submission status"
        ]
    elif decision == 'NEEDS ANALYSIS':
        reasons = data.get('reasoning', [])
        return [
            "1. Analyze specific concerns identified",
            "2. Determine if restrictions can be overcome",
            "3. Evaluate cost-benefit of pursuing",
            "4. Make GO/NO-GO decision after analysis"
        ] + [f"   - Address: {reason}" for reason in reasons]
    else:
        return [
            "1. Do not pursue - does not meet SOS criteria",
            "2. File for future reference if criteria change"
        ]

def create_summary_report(base_folder, results_summary):
    """Create executive summary report"""
    report = f"""
SOS OPPORTUNITY ASSESSMENT SUMMARY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
================
Total Opportunities Assessed: {sum(len(v) for v in results_summary.values())}
- GO Opportunities: {len(results_summary['GO'])}
- NO-GO Opportunities: {len(results_summary['NO-GO'])}
- NEEDS ANALYSIS: {len(results_summary['NEEDS ANALYSIS'])}

SUCCESS RATE: {(len(results_summary['GO']) / sum(len(v) for v in results_summary.values()) * 100):.1f}%

GO OPPORTUNITIES (IMMEDIATE ACTION REQUIRED)
==========================================
"""
    
    for i, opp in enumerate(results_summary['GO'], 1):
        report += f"{i:2d}. {opp['title'][:60]}\n"
        report += f"    ID: {opp['id']}\n"
        report += f"    File: {opp['file']}\n\n"
    
    if results_summary['NEEDS ANALYSIS']:
        report += "\nNEEDS ANALYSIS OPPORTUNITIES\n"
        report += "============================\n"
        for i, opp in enumerate(results_summary['NEEDS ANALYSIS'], 1):
            report += f"{i:2d}. {opp['title'][:60]}\n"
            report += f"    ID: {opp['id']}\n\n"
    
    report += f"\nRECOMMENDATIONS\n"
    report += f"===============\n"
    report += f"1. Immediately review and pursue all {len(results_summary['GO'])} GO opportunities\n"
    report += f"2. Prioritize opportunities with shortest deadlines\n"
    report += f"3. Ensure SAM.gov registration is current\n"
    report += f"4. Prepare standardized capability statements\n"
    
    if results_summary['NEEDS ANALYSIS']:
        report += f"5. Conduct detailed analysis on {len(results_summary['NEEDS ANALYSIS'])} flagged opportunities\n"
    
    with open(os.path.join(base_folder, 'EXECUTIVE_SUMMARY.txt'), 'w', encoding='utf-8') as f:
        f.write(report)

def create_action_items(base_folder, results_summary):
    """Create actionable task list"""
    actions = f"""
SOS OPPORTUNITY ACTION ITEMS
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

IMMEDIATE ACTIONS (GO OPPORTUNITIES)
===================================
"""
    
    for i, opp in enumerate(results_summary['GO'], 1):
        actions += f"\n□ OPPORTUNITY {i}: {opp['title'][:50]}\n"
        actions += f"  ├─ ID: {opp['id']}\n"
        actions += f"  ├─ Review details in: {opp['file']}\n"
        actions += f"  ├─ Check deadline and requirements\n"
        actions += f"  ├─ Prepare capability statement\n"
        actions += f"  └─ Submit proposal\n"
    
    if results_summary['NEEDS ANALYSIS']:
        actions += f"\n\nANALYSIS REQUIRED\n"
        actions += f"=================\n"
        for i, opp in enumerate(results_summary['NEEDS ANALYSIS'], 1):
            actions += f"\n□ ANALYZE {i}: {opp['title'][:50]}\n"
            actions += f"  ├─ ID: {opp['id']}\n"
            actions += f"  └─ Review concerns in: {opp['file']}\n"
    
    actions += f"\n\nOVERALL TASKS\n"
    actions += f"=============\n"
    actions += f"□ Verify SAM.gov registration status\n"
    actions += f"□ Update capability statements\n"
    actions += f"□ Set up tracking system for submissions\n"
    actions += f"□ Schedule follow-up reviews\n"
    
    with open(os.path.join(base_folder, 'ACTION_ITEMS.txt'), 'w', encoding='utf-8') as f:
        f.write(actions)

if __name__ == "__main__":
    organize_results()
