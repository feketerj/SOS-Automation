#!/usr/bin/env python3
"""
Master Analytics Database Tracker
Maintains rolling database of all assessments for analytics
"""

import os
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict, Counter
from datetime import timedelta

class MasterAnalyticsTracker:
    """Maintains master database of all assessment runs"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.master_dir = self.base_dir / "Master_Analytics"
        self.master_dir.mkdir(exist_ok=True)
        
        # Master databases
        self.master_csv = self.master_dir / "master_assessments.csv"
        self.daily_summary = self.master_dir / "daily_summaries.csv"
        self.monthly_stats = self.master_dir / "monthly_statistics.json"
        
    def update_master_database(self, assessment_csv: Path) -> Dict:
        """Add new assessment results to master database"""
        
        # Read new assessment data
        with open(assessment_csv, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            new_data = list(reader)
        
        # Add run metadata
        run_id = assessment_csv.parent.name
        run_date = datetime.now().strftime('%Y-%m-%d')
        for row in new_data:
            row['run_id'] = run_id
            row['run_date'] = run_date
        
        # Load existing master database
        master_data = []
        existing_keys = set()
        
        if self.master_csv.exists():
            with open(self.master_csv, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                master_data = list(reader)
                existing_keys = {(row['announcement_number'], row['run_id']) 
                               for row in master_data}
        
        # Add new records (avoid duplicates)
        new_records = 0
        for row in new_data:
            key = (row['announcement_number'], row['run_id'])
            if key not in existing_keys:
                master_data.append(row)
                new_records += 1
        
        # Save updated master
        if master_data:
            fieldnames = list(master_data[0].keys())
            with open(self.master_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(master_data)
        
        # Update daily summary
        self._update_daily_summary(new_data)
        
        # Calculate statistics
        stats = self._calculate_statistics(master_data)
        
        return {
            'total_records': len(master_data),
            'new_records_added': new_records,
            'statistics': stats
        }
    
    def _update_daily_summary(self, data: List[Dict]):
        """Update daily summary statistics"""
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Calculate daily stats
        go_count = sum(1 for row in data if row.get('final_decision') == 'GO')
        no_go_count = sum(1 for row in data if row.get('final_decision') == 'NO-GO')
        indeterminate_count = sum(1 for row in data if row.get('final_decision') == 'INDETERMINATE')
        
        confidences = [float(row.get('confidence', 0)) for row in data if row.get('confidence')]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        values = [float(row.get('value_high', 0)) for row in data if row.get('value_high')]
        total_value = sum(values)
        
        daily_stats = {
            'date': today,
            'total_assessed': len(data),
            'go_count': go_count,
            'no_go_count': no_go_count,
            'indeterminate_count': indeterminate_count,
            'avg_confidence': avg_confidence,
            'total_value_high': total_value
        }
        
        # Load existing summary
        summary_data = []
        if self.daily_summary.exists():
            with open(self.daily_summary, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                summary_data = list(reader)
        
        # Update or append today's data
        updated = False
        for row in summary_data:
            if row['date'] == today:
                # Update existing entry
                for key in ['total_assessed', 'go_count', 'no_go_count', 'indeterminate_count']:
                    row[key] = str(int(row.get(key, 0)) + daily_stats[key])
                row['avg_confidence'] = str((float(row.get('avg_confidence', 0)) + avg_confidence) / 2)
                row['total_value_high'] = str(float(row.get('total_value_high', 0)) + total_value)
                updated = True
                break
        
        if not updated:
            summary_data.append({k: str(v) for k, v in daily_stats.items()})
        
        # Save summary
        if summary_data:
            fieldnames = ['date', 'total_assessed', 'go_count', 'no_go_count', 
                         'indeterminate_count', 'avg_confidence', 'total_value_high']
            with open(self.daily_summary, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(summary_data)
        
    def _calculate_statistics(self, data: List[Dict]) -> Dict:
        """Calculate comprehensive statistics"""
        
        # Count unique announcements
        unique_announcements = len(set(row['announcement_number'] for row in data))
        
        # Decision breakdown
        decision_counts = Counter(row.get('final_decision', 'UNKNOWN') for row in data)
        
        # Knockout categories
        ko_counts = Counter(row.get('knockout_category', 'UNKNOWN') 
                          for row in data if row.get('knockout_category'))
        
        # Top agencies
        agency_counts = Counter(row.get('agency', 'UNKNOWN') for row in data)
        top_agencies = dict(agency_counts.most_common(10))
        
        # Calculate averages
        confidences = [float(row.get('confidence', 0)) for row in data if row.get('confidence')]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        values = [float(row.get('value_high', 0)) for row in data if row.get('value_high')]
        total_value = sum(values)
        
        # Date range
        dates = [row.get('posted_date') for row in data if row.get('posted_date')]
        earliest_date = min(dates) if dates else None
        latest_date = max(dates) if dates else None
        
        stats = {
            'total_opportunities': len(data),
            'unique_opportunities': unique_announcements,
            'decision_breakdown': {
                'GO': decision_counts.get('GO', 0),
                'NO-GO': decision_counts.get('NO-GO', 0),
                'INDETERMINATE': decision_counts.get('INDETERMINATE', 0)
            },
            'knockout_categories': dict(ko_counts),
            'top_agencies': top_agencies,
            'avg_confidence': avg_confidence,
            'total_potential_value': total_value,
            'date_range': {
                'earliest': earliest_date,
                'latest': latest_date
            }
        }
        
        # Save monthly statistics
        month_key = datetime.now().strftime('%Y-%m')
        
        if self.monthly_stats.exists():
            with open(self.monthly_stats, 'r') as f:
                monthly_data = json.load(f)
        else:
            monthly_data = {}
            
        monthly_data[month_key] = stats
        
        with open(self.monthly_stats, 'w') as f:
            json.dump(monthly_data, f, indent=2)
            
        return stats
    
    def generate_analytics_report(self) -> str:
        """Generate comprehensive analytics report"""
        
        if not self.master_csv.exists():
            return "No data available for analytics"
            
        with open(self.master_csv, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        report = ["# MASTER ANALYTICS REPORT", 
                 f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
        
        # Overall statistics
        unique_announcements = len(set(row['announcement_number'] for row in data))
        report.append("## OVERALL STATISTICS")
        report.append(f"- Total Assessments: {len(data)}")
        report.append(f"- Unique Opportunities: {unique_announcements}")
        report.append("")
        
        # Decision breakdown
        report.append("## DECISION BREAKDOWN")
        for decision in ['GO', 'NO-GO', 'INDETERMINATE']:
            count = sum(1 for row in data if row.get('final_decision') == decision)
            pct = (count / len(data)) * 100 if data else 0
            report.append(f"- {decision}: {count} ({pct:.1f}%)")
        report.append("")
        
        # Knockout patterns
        report.append("## TOP KNOCKOUT PATTERNS")
        ko_counts = Counter(row.get('knockout_category') 
                          for row in data 
                          if row.get('final_decision') == 'NO-GO' and row.get('knockout_category'))
        for category, count in ko_counts.most_common(10):
            report.append(f"- {category}: {count} occurrences")
        report.append("")
        
        # Agency breakdown
        report.append("## TOP AGENCIES")
        agency_counts = Counter(row.get('agency', 'UNKNOWN') for row in data)
        for agency, count in agency_counts.most_common(10):
            report.append(f"- {agency}: {count} opportunities")
        report.append("")
        
        # Value analysis
        values = [float(row.get('value_high', 0)) for row in data if row.get('value_high')]
        if values:
            report.append("## VALUE ANALYSIS")
            go_value = sum(float(row.get('value_high', 0)) 
                          for row in data 
                          if row.get('final_decision') == 'GO' and row.get('value_high'))
            total_value = sum(values)
            avg_value = total_value / len(values) if values else 0
            report.append(f"- Total Opportunity Value: ${total_value:,.0f}")
            report.append(f"- GO Opportunity Value: ${go_value:,.0f}")
            report.append(f"- Average Opportunity Value: ${avg_value:,.0f}")
        
        # Save report
        report_path = self.master_dir / f"analytics_report_{datetime.now().strftime('%Y%m%d')}.md"
        with open(report_path, 'w') as f:
            f.write('\n'.join(report))
            
        return '\n'.join(report)
    
    def get_trend_analysis(self, days: int = 30) -> Dict:
        """Analyze trends over specified period"""
        
        if not self.daily_summary.exists():
            return {}
            
        with open(self.daily_summary, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            daily_data = list(reader)
        
        # Filter to last N days
        cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        recent_data = [row for row in daily_data if row['date'] >= cutoff]
        
        if not recent_data:
            return {}
            
        total_assessed = sum(int(row.get('total_assessed', 0)) for row in recent_data)
        total_go = sum(int(row.get('go_count', 0)) for row in recent_data)
        daily_average = total_assessed / len(recent_data) if recent_data else 0
        go_rate = (total_go / total_assessed) * 100 if total_assessed > 0 else 0
        
        # Find peak day
        peak_day = max(recent_data, key=lambda x: int(x.get('total_assessed', 0)))
        
        trends = {
            'period_days': days,
            'total_assessed': total_assessed,
            'daily_average': daily_average,
            'go_rate': go_rate,
            'peak_day': {
                'date': peak_day['date'],
                'count': int(peak_day['total_assessed'])
            }
        }
        
        return trends


def update_from_latest_run():
    """Update master database from latest assessment run"""
    
    tracker = MasterAnalyticsTracker()
    
    # Find latest assessment
    sos_output = Path(__file__).parent / "SOS_Output"
    
    # Get most recent run
    latest_csv = None
    latest_time = None
    
    for month_dir in sorted(sos_output.glob("*"), reverse=True):
        if month_dir.is_dir():
            for run_dir in sorted(month_dir.glob("Run_*"), reverse=True):
                assessment_csv = run_dir / "assessment.csv"
                if assessment_csv.exists():
                    if latest_time is None or assessment_csv.stat().st_mtime > latest_time:
                        latest_csv = assessment_csv
                        latest_time = assessment_csv.stat().st_mtime
                        
    if latest_csv:
        print(f"Updating from: {latest_csv}")
        result = tracker.update_master_database(latest_csv)
        print(f"Master database updated: {result['total_records']} total records")
        print(f"New records added: {result['new_records_added']}")
        
        # Generate report
        report = tracker.generate_analytics_report()
        print("\n" + "="*50)
        print(report)
        
        # Show trends
        trends = tracker.get_trend_analysis(30)
        if trends:
            print("\n## 30-DAY TRENDS")
            print(f"- Total Assessed: {trends['total_assessed']}")
            print(f"- Daily Average: {trends['daily_average']:.1f}")
            print(f"- GO Rate: {trends['go_rate']:.1f}%")
    else:
        print("No assessment files found")


if __name__ == "__main__":
    update_from_latest_run()