"""
SOS Pipeline Runner
Simple script to run the complete assessment pipeline
"""

import os
import sys
from pathlib import Path

def check_setup():
    """Check if everything is set up correctly"""
    env_file = Path(".env")
    if not env_file.exists():
        print("ERROR: No .env file found!")
        print("Please create a .env file with your API key and daily URL")
        return False
    
    # Check for required variables
    with open(env_file, 'r') as f:
        content = f.read()
    
    if 'HIGHERGOV_API_KEY=' not in content:
        print("ERROR: No HIGHERGOV_API_KEY found in .env file")
        return False
    
    if 'SAVED_SEARCH_ID=' not in content:
        print("ERROR: No SAVED_SEARCH_ID found in .env file")
        print("This should be stable and not change daily")
        return False
    
    return True

def main():
    """Main runner"""
    print("SOS OPPORTUNITY ASSESSMENT PIPELINE")
    print("=" * 50)
    
    # Check setup
    if not check_setup():
        print("\nSetup incomplete. Please fix the issues above.")
        return
    
    print("Setup validated successfully.")
    print("\nChoose an option:")
    print("1. Run assessment on 100 opportunities (test)")
    print("2. Run assessment on ALL opportunities (full run)")
    print("3. Organize existing results into folders")
    print("4. Show current configuration")
    print("5. Run enhanced pipeline with detailed logging")
    print("6. Analyze logs and debug information")
    print("7. Test filter patterns against sample data")
    
    choice = input("\nEnter choice (1-7): ").strip()
    
    if choice == "1":
        print("\nRunning test assessment (100 opportunities)...")
        os.system("python main_pipeline.py")
    
    elif choice == "2":
        print("\nRunning full assessment (ALL opportunities)...")
        print("This may take a while...")
        # You can modify the limit in main_pipeline.py or pass it as parameter
        os.system("python main_pipeline.py --full")
    
    elif choice == "3":
        print("\nOrganizing existing results...")
        os.system("python organize_official_results.py")
    
    elif choice == "4":
        print("\nCurrent Configuration:")
        env_file = Path(".env")
        with open(env_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('HIGHERGOV_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
                    print(f"API Key: {'*' * (len(api_key) - 4)}{api_key[-4:]}")
                elif line.startswith('SAVED_SEARCH_ID='):
                    search_id = line.split('=', 1)[1].strip()
                    print(f"Saved Search ID: {search_id}")
    
    elif choice == "5":
        print("\nRunning enhanced pipeline with comprehensive logging...")
        print("Detailed logs will be saved to 'logs' directory")
        print("Starting enhanced assessment...")
        os.system("python main_pipeline_enhanced.py")
        print("\nEnhanced pipeline completed!")
        print("Run option 6 to analyze the detailed logs")
    
    elif choice == "6":
        print("\nAnalyzing logs and debug information...")
        if not Path("logs").exists():
            print("No logs directory found. Run the enhanced pipeline first (option 5)")
        else:
            os.system("python debug_analyzer.py")
    
    elif choice == "7":
        print("\nTesting filter patterns...")
        os.system("python analyze_filter_gaps.py")
        
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
