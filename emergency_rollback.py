#!/usr/bin/env python3
# AUTO-GENERATED ROLLBACK SCRIPT
# Created: 20250913_113505

import os
import shutil
from datetime import datetime

def rollback():
    print("Starting rollback...")
    print("-" * 40)

    files_to_rollback = ['decision_sanitizer.py', 'enhanced_output_manager.py', 'highergov_batch_fetcher.py', 'Mistral_Batch_Processor/FULL_BATCH_PROCESSOR.py']

    success_count = 0
    fail_count = 0

    for file_path in files_to_rollback:
        backup_path = file_path + '.backup'
        if os.path.exists(backup_path):
            try:
                # Create safety copy of current
                safety_copy = file_path + f'.before_rollback_20250913_113505'
                shutil.copy2(file_path, safety_copy)

                # Restore from backup
                shutil.copy2(backup_path, file_path)
                print(f"[OK] Rolled back: {file_path}")
                success_count += 1
            except Exception as e:
                print(f"[FAIL] Could not rollback {file_path}: {e}")
                fail_count += 1
        else:
            print(f"[SKIP] No backup for: {file_path}")
            fail_count += 1

    print("-" * 40)
    print(f"Rollback complete: {success_count} succeeded, {fail_count} failed")

    if fail_count == 0:
        print("[SUCCESS] All files rolled back successfully!")
    else:
        print("[WARNING] Some files could not be rolled back")

    return fail_count == 0

if __name__ == "__main__":
    import sys
    success = rollback()
    sys.exit(0 if success else 1)
