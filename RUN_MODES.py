#!/usr/bin/env python3
"""
RUN_MODES.py - Control which processing modes to use

USAGE:
    python RUN_MODES.py --mode [batch|agent|batch-agent] [--verify]
    
MODES:
    batch       : Regex + Batch only (cheapest)
    agent       : Regex + Agent only (most accurate) 
    batch-agent : Regex + Batch + Agent verification (balanced)

OPTIONS:
    --verify    : In batch mode, also run agent verification on GOs/INDETERMINATEs
    --skip-regex: Skip regex filtering (not recommended - it's free!)
"""

import sys
import os
import subprocess
import json
from datetime import datetime

def _load_config_env():
    """Optionally load centralized config and set env vars if missing.
    Preserves existing behavior by only filling unset values.
    """
    try:
        from config.loader import get_config  # type: ignore
        cfg = get_config()
        os.environ.setdefault('HIGHERGOV_API_KEY', str(cfg.get('highergov.api_key', '') or os.environ.get('HIGHERGOV_API_KEY', '')))
        os.environ.setdefault('HG_API_BASE_URL', str(cfg.get('highergov.base_url', '') or os.environ.get('HG_API_BASE_URL', '')))
        os.environ.setdefault('MISTRAL_API_KEY', str(cfg.get('mistral.api_key', '') or os.environ.get('MISTRAL_API_KEY', '')))
        os.environ.setdefault('MISTRAL_API_BASE_URL', str(cfg.get('mistral.base_url', '') or os.environ.get('MISTRAL_API_BASE_URL', '')))
    except Exception:
        pass

def print_header(mode):
    """Print mode header"""
    print("=" * 80)
    print(f"SOS ASSESSMENT PIPELINE - {mode.upper()} MODE")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 80)

def run_batch_only():
    """Run Regex + Batch processing only (no agent verification)"""
    print_header("BATCH ONLY")
    print("Pipeline: Regex (FREE) -> Batch (50% off)")
    print("Cost: CHEAPEST - Maximum savings")
    print("Accuracy: Good - Fine-tuned model with system prompt")
    print("-" * 80)
    
    # Set environment variable to skip agent verification
    os.environ['SKIP_AGENT_VERIFICATION'] = '1'
    _load_config_env()
    
    # Run batch processor
    os.chdir('Mistral_Batch_Processor')
    result = subprocess.run([sys.executable, 'FULL_BATCH_PROCESSOR.py'], 
                          capture_output=False, text=True)
    
    return result.returncode

def run_agent_only():
    """Run Regex + Agent processing only (no batch)"""
    print_header("AGENT ONLY")
    print("Pipeline: Regex (FREE) -> Agent (full price)")
    print("Cost: HIGHER - But most accurate")
    print("Accuracy: BEST - Production agent with full training")
    print("-" * 80)
    
    _load_config_env()
    # Run regular batch runner (which uses agent)
    result = subprocess.run([sys.executable, 'BATCH_RUN.py'], 
                          capture_output=False, text=True)
    
    return result.returncode

def run_batch_with_agent():
    """Run full three-stage pipeline"""
    print_header("BATCH + AGENT VERIFICATION")
    print("Pipeline: Regex (FREE) -> Batch (50% off) -> Agent (selective)")
    print("Cost: BALANCED - Good savings with accuracy check")
    print("Accuracy: EXCELLENT - Agent verifies GOs/INDETERMINATEs")
    print("-" * 80)
    
    # Ensure agent verification is enabled
    os.environ.pop('SKIP_AGENT_VERIFICATION', None)
    _load_config_env()
    
    # Run batch processor with full pipeline
    os.chdir('Mistral_Batch_Processor')
    result = subprocess.run([sys.executable, 'FULL_BATCH_PROCESSOR.py'], 
                          capture_output=False, text=True)
    
    return result.returncode

def show_cost_comparison():
    """Show cost comparison between modes"""
    print("\n" + "=" * 80)
    print("COST COMPARISON (per 100 opportunities)")
    print("=" * 80)
    print("Assuming: 40% regex knockouts, $0.002 per API call")
    print("-" * 80)
    
    # No pipeline (worst case)
    no_pipeline = 100 * 0.002
    
    # Batch only
    batch_only = 60 * 0.001  # 60 remaining after regex, 50% discount
    
    # Agent only  
    agent_only = 60 * 0.002  # 60 remaining after regex, full price
    
    # Batch + Agent (assuming 20% need verification)
    batch_agent = (60 * 0.001) + (12 * 0.002)  # 60 batch + 12 agent
    
    print(f"1. No Pipeline (all agent):     ${no_pipeline:.3f} (100%)")
    print(f"2. Regex + Batch:               ${batch_only:.3f} ({batch_only/no_pipeline*100:.0f}%)")
    print(f"3. Regex + Agent:               ${agent_only:.3f} ({agent_only/no_pipeline*100:.0f}%)")
    print(f"4. Regex + Batch + Agent:       ${batch_agent:.3f} ({batch_agent/no_pipeline*100:.0f}%)")
    print("-" * 80)
    print(f"SAVINGS with Batch only:        ${no_pipeline - batch_only:.3f} (70% savings)")
    print(f"SAVINGS with Batch + Agent:     ${no_pipeline - batch_agent:.3f} (58% savings)")
    print("=" * 80)

def main():
    """Main entry point"""
    
    # Parse arguments
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        show_cost_comparison()
        return 0
    
    mode = None
    verify = False
    
    for arg in sys.argv[1:]:
        if arg == '--mode':
            continue
        elif arg in ['batch', 'agent', 'batch-agent']:
            mode = arg
        elif arg == '--verify':
            verify = True
    
    if not mode:
        # Default to showing menu
        print("=" * 80)
        print("SOS ASSESSMENT PIPELINE - MODE SELECTOR")
        print("=" * 80)
        print("\nSelect processing mode:")
        print("1. Batch Only     (Regex + Batch) - CHEAPEST")
        print("2. Agent Only     (Regex + Agent) - MOST ACCURATE")
        print("3. Batch + Agent  (All three stages) - BALANCED")
        print("4. Show cost comparison")
        print("5. Exit")
        print("-" * 80)
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            mode = 'batch'
        elif choice == '2':
            mode = 'agent'
        elif choice == '3':
            mode = 'batch-agent'
        elif choice == '4':
            show_cost_comparison()
            return 0
        else:
            print("Exiting...")
            return 0
    
    # Run selected mode
    if mode == 'batch':
        if verify:
            print("\nNote: --verify flag converts batch mode to batch-agent mode")
            return run_batch_with_agent()
        else:
            return run_batch_only()
    elif mode == 'agent':
        return run_agent_only()
    elif mode == 'batch-agent':
        return run_batch_with_agent()
    else:
        print(f"Unknown mode: {mode}")
        return 1

if __name__ == "__main__":
    exit(main())
