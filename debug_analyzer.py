"""
SOS Pipeline Debugging and Monitoring Tools
Provides utilities for analyzing logs, tracking performance, and debugging filter decisions
"""

import json
import pandas as pd
from pathlib import Path
import re
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from collections import defaultdict
import logging

class SOSDebugAnalyzer:
    """
    Analyzes SOS pipeline logs and results to identify issues and opportunities
    """
    
    def __init__(self, logs_dir: str = "logs", output_dir: str = "output"):
        self.logs_dir = Path(logs_dir)
        self.output_dir = Path(output_dir)
        
    def analyze_filter_decisions(self, days_back: int = 7):
        """Analyze filter decisions to identify patterns and potential improvements"""
        
        print("ANALYZING FILTER DECISIONS")
        print("=" * 50)
        
        # Read debug decisions
        debug_file = self.logs_dir / "debug_decisions.jsonl"
        if not debug_file.exists():
            print(f"ERROR: Debug file not found: {debug_file}")
            return
        
        decisions = []
        with open(debug_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    decisions.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        
        if not decisions:
            print("ERROR: No debug decisions found")
            return
        
        print(f"INFO: Analyzed {len(decisions)} filter decisions")
        
        # Analyze patterns
        step_counts = defaultdict(int)
        match_rates = defaultdict(list)
        
        for decision in decisions:
            step = decision.get('step', 'unknown')
            matched = decision.get('matched', False)
            
            step_counts[step] += 1
            match_rates[step].append(matched)
        
        # Summary statistics
        print("\nDECISION STATISTICS:")
        for step, count in sorted(step_counts.items()):
            matches = sum(match_rates[step])
            match_rate = (matches / count) * 100 if count > 0 else 0
            print(f"  {step}: {count} decisions, {match_rate:.1f}% matched")
        
        # Look for pattern misses
        pattern_misses = [d for d in decisions if d.get('type') == 'pattern_miss']
        if pattern_misses:
            print(f"\nWARNING: PATTERN ENHANCEMENT OPPORTUNITIES: {len(pattern_misses)}")
            for miss in pattern_misses[-5:]:  # Show last 5
                print(f"  - {miss.get('opportunity_id')}: {miss.get('expected_pattern')}")
                print(f"    Reason: {miss.get('reason')}")
        
        return decisions
    
    def analyze_performance_logs(self):
        """Analyze performance logs to identify bottlenecks"""
        
        print("\nANALYZING PERFORMANCE")
        print("=" * 50)
        
        perf_file = self.logs_dir / "performance.log"
        if not perf_file.exists():
            print(f"ERROR: Performance log not found: {perf_file}")
            return
        
        # Parse performance data
        performance_data = []
        with open(perf_file, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.search(r'(\w+) executed in ([\d.]+) seconds', line)
                if match:
                    function_name, execution_time = match.groups()
                    performance_data.append({
                        'function': function_name,
                        'time': float(execution_time),
                        'timestamp': line.split(' - ')[0]
                    })
        
        if not performance_data:
            print("ERROR: No performance data found")
            return
        
        # Analyze timing data
        df = pd.DataFrame(performance_data)
        
        print(f"INFO: Analyzed {len(performance_data)} function executions")
        
        # Function timing summary
        timing_summary = df.groupby('function')['time'].agg(['count', 'mean', 'std', 'max']).round(4)
        print("\n⏱️  FUNCTION TIMING SUMMARY:")
        print(timing_summary.to_string())
        
        # Identify slow functions
        slow_functions = timing_summary[timing_summary['mean'] > 1.0]  # > 1 second
        if not slow_functions.empty:
            print(f"\n🐌 SLOW FUNCTIONS (>1s average):")
            print(slow_functions.to_string())
        
        return performance_data
    
    def analyze_error_patterns(self):
        """Analyze error logs to identify common failure patterns"""
        
        print("\nANALYZING ERROR PATTERNS")
        print("=" * 50)
        
        error_file = self.logs_dir / "errors.log"
        if not error_file.exists():
            print(f"ERROR: Error log not found: {error_file}")
            return
        
        errors = []
        with open(error_file, 'r', encoding='utf-8') as f:
            for line in f:
                if 'ERROR' in line or 'WARNING' in line:
                    errors.append(line.strip())
        
        if not errors:
            print("SUCCESS: No errors found")
            return
        
        print(f"INFO: Found {len(errors)} error/warning entries")
        
        # Categorize errors
        error_categories = defaultdict(int)
        for error in errors:
            if 'API' in error:
                error_categories['API Issues'] += 1
            elif 'Filter' in error or 'FILTER' in error:
                error_categories['Filter Issues'] += 1
            elif 'regex' in error.lower():
                error_categories['Regex Issues'] += 1
            elif 'json' in error.lower() or 'JSON' in error:
                error_categories['JSON Issues'] += 1
            else:
                error_categories['Other'] += 1
        
        print("\nERROR CATEGORIES:")
        for category, count in sorted(error_categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count}")
        
        # Show recent errors
        print(f"\nRECENT ERRORS (last 5):")
        for error in errors[-5:]:
            print(f"  {error[:100]}...")
        
        return errors
    
    def analyze_results_distribution(self):
        """Analyze the distribution of GO vs NO-GO decisions"""
        
        print("\nANALYZING RESULTS DISTRIBUTION")
        print("=" * 50)
        
        if not self.output_dir.exists():
            print(f"ERROR: Output directory not found: {self.output_dir}")
            return
        
        result_files = list(self.output_dir.glob("*.json"))
        if not result_files:
            print("ERROR: No result files found")
            return
        
        results = []
        for file_path in result_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    results.append({
                        'decision': data.get('final_decision', 'UNKNOWN'),
                        'opportunity_id': data.get('opportunity_id'),
                        'reasoning': data.get('reasoning', [])
                    })
            except (json.JSONDecodeError, Exception):
                continue
        
        print(f"INFO: Analyzed {len(results)} assessment results")
        
        # Decision distribution
        decisions = [r['decision'] for r in results]
        decision_counts = pd.Series(decisions).value_counts()
        
        print("\nDECISION DISTRIBUTION:")
        for decision, count in decision_counts.items():
            percentage = (count / len(results)) * 100
            print(f"  {decision}: {count} ({percentage:.1f}%)")
        
        # Analyze NO-GO reasons
        no_go_results = [r for r in results if r['decision'] == 'NO-GO']
        if no_go_results:
            print(f"\n🚫 NO-GO REASON ANALYSIS ({len(no_go_results)} cases):")
            
            reason_counts = defaultdict(int)
            for result in no_go_results:
                for reason in result.get('reasoning', []):
                    if 'Failed aviation check' in reason:
                        reason_counts['Not Aviation-Related'] += 1
                    elif 'SAR required' in reason:
                        reason_counts['SAR Required'] += 1
                    elif 'Sole source' in reason:
                        reason_counts['Sole Source'] += 1
                    elif 'Technical data' in reason:
                        reason_counts['Technical Data Required'] += 1
                    elif 'Security clearance' in reason:
                        reason_counts['Security Clearance'] += 1
                    else:
                        reason_counts['Other'] += 1
            
            for reason, count in sorted(reason_counts.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(no_go_results)) * 100
                print(f"  {reason}: {count} ({percentage:.1f}%)")
        
        return results
    
    def generate_debug_report(self):
        """Generate a comprehensive debug report"""
        
        print("SOS PIPELINE DEBUG REPORT")
        print("=" * 80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Run all analyses
        filter_decisions = self.analyze_filter_decisions()
        performance_data = self.analyze_performance_logs()
        error_data = self.analyze_error_patterns()
        results_data = self.analyze_results_distribution()
        
        # Summary recommendations
        print("\n🎯 RECOMMENDATIONS")
        print("=" * 50)
        
        recommendations = []
        
        # Check for performance issues
        if performance_data:
            avg_times = defaultdict(list)
            for entry in performance_data:
                avg_times[entry['function']].append(entry['time'])
            
            for func, times in avg_times.items():
                avg_time = sum(times) / len(times)
                if avg_time > 2.0:
                    recommendations.append(f"⚡ Optimize {func} - average {avg_time:.2f}s execution time")
        
        # Check for high NO-GO rates
        if results_data:
            decisions = [r['decision'] for r in results_data]
            no_go_rate = (decisions.count('NO-GO') / len(decisions)) * 100
            if no_go_rate > 95:
                recommendations.append(f"🎯 Very high NO-GO rate ({no_go_rate:.1f}%) - consider filter review")
            elif no_go_rate < 85:
                recommendations.append(f"⚠️  Lower NO-GO rate ({no_go_rate:.1f}%) - validate filter strictness")
        
        # Check for error patterns
        if error_data and len(error_data) > 10:
            recommendations.append(f"🚨 High error count ({len(error_data)}) - investigate error patterns")
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")
        else:
            print("✅ No critical issues identified")
        
        print("\n📝 For detailed analysis, check individual log files in the 'logs' directory")
        print("=" * 80)

def main():
    """Run comprehensive debug analysis"""
    analyzer = SOSDebugAnalyzer()
    analyzer.generate_debug_report()

if __name__ == "__main__":
    main()
