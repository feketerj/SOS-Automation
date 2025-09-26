#!/usr/bin/env python3
"""Parse batch results and show decision summary"""

import json
import sys

def parse_results(filename):
    """Parse JSONL batch results"""
    
    results = []
    decisions = {'GO': 0, 'NO-GO': 0, 'INDETERMINATE': 0, 'ERROR': 0}
    
    with open(filename, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
                
            try:
                data = json.loads(line)
                custom_id = data.get('custom_id', '')
                
                # Extract opportunity info from custom_id
                parts = custom_id.split('-')
                if len(parts) >= 4:
                    search_id = parts[1]
                    opp_id = parts[2]
                else:
                    search_id = 'unknown'
                    opp_id = custom_id
                
                # Parse response
                response = data.get('response', {})
                if response.get('status_code') == 200:
                    body = response.get('body', {})
                    choices = body.get('choices', [])
                    if choices:
                        content = choices[0]['message']['content']
                        
                        # Extract JSON from content
                        if '```json' in content:
                            json_str = content.split('```json')[1].split('```')[0]
                            result = json.loads(json_str)
                            
                            recommendation = result.get('recommendation', 'UNKNOWN')
                            title = result.get('solicitation_title', 'Unknown')[:50]
                            rationale = result.get('rationale', '')[:100]
                            
                            # Convert NO-GO to INDETERMINATE (batch AI shouldn't return NO-GO)
                            if recommendation == 'NO-GO':
                                recommendation = 'INDETERMINATE'
                                rationale = f"[CONVERTED FROM NO-GO] {rationale}"
                            
                            decisions[recommendation] = decisions.get(recommendation, 0) + 1
                            
                            results.append({
                                'search_id': search_id,
                                'opp_id': opp_id,
                                'title': title,
                                'decision': recommendation,
                                'rationale': rationale
                            })
                else:
                    decisions['ERROR'] += 1
                    print(f"  Line {line_num}: API error")
                    
            except Exception as e:
                decisions['ERROR'] += 1
                print(f"  Line {line_num}: Parse error - {e}")
    
    # Display summary
    print(f"\nBATCH RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total processed: {len(results)}")
    print(f"\nDecision breakdown:")
    for decision, count in sorted(decisions.items()):
        if count > 0:
            print(f"  {decision}: {count}")
    
    # Show GO opportunities
    go_opps = [r for r in results if r['decision'] == 'GO']
    if go_opps:
        print(f"\nGO Opportunities ({len(go_opps)}):")
        for opp in go_opps[:10]:  # Show first 10
            print(f"  - {opp['title']}")
            print(f"    {opp['rationale']}")
    
    # Show INDETERMINATE opportunities
    ind_opps = [r for r in results if r['decision'] == 'INDETERMINATE']
    if ind_opps:
        print(f"\nINDETERMINATE Opportunities ({len(ind_opps)}):")
        for opp in ind_opps[:10]:  # Show first 10
            print(f"  - {opp['title']}")
            print(f"    {opp['rationale']}")
    
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        parse_results(sys.argv[1])
    else:
        # Default to most recent
        parse_results("batch_output_20250912_181945.jsonl")