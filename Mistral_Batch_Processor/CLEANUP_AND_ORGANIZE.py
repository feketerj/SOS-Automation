"""
CLEANUP AND ORGANIZE SCRIPT
Moves all batch files to proper SOS_Output folders
Cleans up the Mistral_Batch_Processor directory
"""

import os
import shutil
from datetime import datetime
import glob

def cleanup_batch_processor():
    """Move all JSONL and test files to organized folders"""
    
    batch_dir = os.path.dirname(__file__)
    base_output = os.path.join(os.path.dirname(batch_dir), "SOS_Output", "2025-09")
    
    # Create organized folders
    batch_inputs_dir = os.path.join(base_output, "_BATCH_INPUTS")
    batch_results_dir = os.path.join(base_output, "_BATCH_RESULTS")
    test_files_dir = os.path.join(base_output, "_TEST_FILES")
    
    os.makedirs(batch_inputs_dir, exist_ok=True)
    os.makedirs(batch_results_dir, exist_ok=True)
    os.makedirs(test_files_dir, exist_ok=True)
    
    moved_count = 0
    
    # Move batch input files
    for file in glob.glob(os.path.join(batch_dir, "batch_input_*.jsonl")):
        dest = os.path.join(batch_inputs_dir, os.path.basename(file))
        shutil.move(file, dest)
        print(f"Moved: {os.path.basename(file)} -> _BATCH_INPUTS/")
        moved_count += 1
    
    # Move batch metadata files
    for file in glob.glob(os.path.join(batch_dir, "batch_metadata_*.json")):
        dest = os.path.join(batch_inputs_dir, os.path.basename(file))
        shutil.move(file, dest)
        print(f"Moved: {os.path.basename(file)} -> _BATCH_INPUTS/")
        moved_count += 1
    
    # Move batch results
    for file in glob.glob(os.path.join(batch_dir, "batch_results_*.jsonl")):
        dest = os.path.join(batch_results_dir, os.path.basename(file))
        shutil.move(file, dest)
        print(f"Moved: {os.path.basename(file)} -> _BATCH_RESULTS/")
        moved_count += 1
    
    # Move test files
    for pattern in ["test_*.jsonl", "validation_*.jsonl", "quick_test_*.jsonl", "*Test*.jsonl"]:
        for file in glob.glob(os.path.join(batch_dir, pattern)):
            dest = os.path.join(test_files_dir, os.path.basename(file))
            shutil.move(file, dest)
            print(f"Moved: {os.path.basename(file)} -> _TEST_FILES/")
            moved_count += 1
    
    print(f"\n[OK] Moved {moved_count} files to SOS_Output/2025-09/")
    
    # Clean up empty folders in SOS_Output
    cleanup_empty_folders()
    
    return moved_count

def cleanup_empty_folders():
    """Remove unused empty folders from SOS_Output"""
    
    sos_output = os.path.join(os.path.dirname(os.path.dirname(__file__)), "SOS_Output")
    
    empty_folders = ["Analytics", "Archive", "Assessments", "Daily", "Export", 
                     "GO_Opportunities", "Reports", "Master_Database"]
    
    removed = 0
    for folder in empty_folders:
        folder_path = os.path.join(sos_output, folder)
        try:
            if os.path.exists(folder_path) and not os.listdir(folder_path):
                os.rmdir(folder_path)
                print(f"Removed empty folder: {folder}")
                removed += 1
        except PermissionError:
            print(f"Skipped folder (permission denied): {folder}")
        except Exception as e:
            print(f"Skipped folder {folder}: {e}")
    
    if removed > 0:
        print(f"[OK] Removed {removed} empty folders")

def show_new_structure():
    """Display the new organized structure"""
    
    print("\n" + "=" * 60)
    print("NEW ORGANIZED STRUCTURE:")
    print("=" * 60)
    
    print("""
SOS_Output/
├── 2025-09/
│   ├── Run_[timestamp]_[searchID]/      # Individual runs
│   │   ├── assessment.csv
│   │   ├── assessment.json
│   │   └── assessment.md
│   │
│   ├── BatchRun_[timestamp]_BATCH/      # Batch runs
│   │   ├── assessment.csv
│   │   ├── assessment.json
│   │   └── assessment.md
│   │
│   ├── _BATCH_INPUTS/                   # All input JSONLs
│   │   ├── batch_input_*.jsonl
│   │   └── batch_metadata_*.json
│   │
│   ├── _BATCH_RESULTS/                  # Raw Mistral results
│   │   └── batch_results_*.jsonl
│   │
│   └── _TEST_FILES/                     # Test files
│       └── test_*.jsonl
│
└── 2025-10/  (when October comes)
    """)
    
    print("Mistral_Batch_Processor/ folder is now CLEAN!")
    print("Only Python scripts remain, all data moved to SOS_Output")

if __name__ == "__main__":
    print("CLEANING UP BATCH PROCESSOR DIRECTORY")
    print("=" * 60)
    
    # Perform cleanup
    moved = cleanup_batch_processor()
    
    # Show new structure
    show_new_structure()
    
    print("\n[OK] CLEANUP COMPLETE!")
    print(f"  Moved {moved} files to organized folders")
    print("  All outputs now in SOS_Output/2025-09/")
    print("  Batch processor directory is clean!")