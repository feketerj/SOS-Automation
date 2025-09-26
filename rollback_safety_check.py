#!/usr/bin/env python3
"""
Rollback Safety Check - Verify system can safely rollback changes if needed
"""

import os
import sys
import hashlib
from datetime import datetime

class RollbackSafetyCheck:
    """Verify rollback readiness and create safety checkpoints"""

    def __init__(self):
        self.critical_files = [
            'decision_sanitizer.py',
            'enhanced_output_manager.py',
            'highergov_batch_fetcher.py',
            'Mistral_Batch_Processor/FULL_BATCH_PROCESSOR.py'
        ]
        self.checksums = {}
        self.rollback_ready = True

    def create_safety_checkpoint(self):
        """Create a safety checkpoint with file checksums"""
        print("=" * 60)
        print("ROLLBACK SAFETY CHECKPOINT")
        print("=" * 60)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("-" * 60)

        checkpoint_data = []

        for file_path in self.critical_files:
            if os.path.exists(file_path):
                # Calculate checksum
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()

                self.checksums[file_path] = file_hash
                file_size = os.path.getsize(file_path)

                print(f"\n[FILE] {file_path}")
                print(f"  Size: {file_size} bytes")
                print(f"  SHA256: {file_hash[:16]}...")

                # Check for backup
                backup_path = file_path + '.backup'
                if os.path.exists(backup_path):
                    print(f"  Backup: EXISTS")
                else:
                    print(f"  Backup: NOT FOUND (recommend creating)")
                    self.rollback_ready = False

                checkpoint_data.append({
                    'file': file_path,
                    'size': file_size,
                    'sha256': file_hash,
                    'backup_exists': os.path.exists(backup_path)
                })
            else:
                print(f"\n[WARNING] File not found: {file_path}")

        # Save checkpoint
        checkpoint_file = f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(checkpoint_file, 'w') as f:
            f.write("ROLLBACK SAFETY CHECKPOINT\n")
            f.write(f"Created: {datetime.now().isoformat()}\n")
            f.write("=" * 60 + "\n\n")

            for item in checkpoint_data:
                f.write(f"File: {item['file']}\n")
                f.write(f"Size: {item['size']} bytes\n")
                f.write(f"SHA256: {item['sha256']}\n")
                f.write(f"Backup: {'YES' if item['backup_exists'] else 'NO'}\n")
                f.write("-" * 40 + "\n")

        print(f"\n[SAVED] Checkpoint saved to: {checkpoint_file}")
        return checkpoint_file

    def verify_rollback_capability(self):
        """Verify system can be safely rolled back"""
        print("\n" + "=" * 60)
        print("ROLLBACK CAPABILITY CHECK")
        print("=" * 60)

        issues = []

        # Check 1: Backup files exist
        print("\n1. Checking backup files...")
        for file_path in self.critical_files:
            backup_path = file_path + '.backup'
            if not os.path.exists(backup_path):
                issues.append(f"No backup for {file_path}")
                print(f"  [WARN] No backup: {file_path}")
            else:
                print(f"  [OK] Backup exists: {file_path}")

        # Check 2: Translation can be disabled
        print("\n2. Checking translation toggle...")
        try:
            from decision_sanitizer import DecisionSanitizer
            # Check if monitoring hook exists
            if hasattr(DecisionSanitizer, '_normalize_assessment_type'):
                print("  [OK] Assessment type normalization can be disabled")
            else:
                issues.append("Assessment type normalization method not found")
                print("  [WARN] Normalization method not found")
        except Exception as e:
            issues.append(f"Cannot import decision_sanitizer: {e}")
            print(f"  [ERROR] Import failed: {e}")

        # Check 3: Documentation exists
        print("\n3. Checking documentation...")
        docs = [
            'FIELD_MAPPING_DOCUMENTATION.md',
            'CLAUDE.md'
        ]
        for doc in docs:
            if os.path.exists(doc):
                print(f"  [OK] Documentation found: {doc}")
            else:
                issues.append(f"Documentation missing: {doc}")
                print(f"  [WARN] Missing: {doc}")

        # Check 4: Test coverage
        print("\n4. Checking test coverage...")
        tests = [
            'test_assessment_type_fix.py',
            'test_url_preservation.py',
            'test_backward_compat.py',
            'quality_control_validator.py'
        ]
        for test in tests:
            if os.path.exists(test):
                print(f"  [OK] Test found: {test}")
            else:
                issues.append(f"Test missing: {test}")
                print(f"  [WARN] Missing: {test}")

        # Summary
        print("\n" + "=" * 60)
        if len(issues) == 0:
            print("[SUCCESS] System is rollback-ready!")
            print("\nRollback procedure:")
            print("1. Copy .backup files over current files")
            print("2. Or use git to revert to previous commit")
            print("3. Run quality_control_validator.py to verify")
        else:
            print("[WARNING] Rollback readiness issues found:")
            for issue in issues:
                print(f"  - {issue}")
            print("\nRecommendations:")
            print("1. Create backups: cp file.py file.py.backup")
            print("2. Document current state in CLAUDE.md")
            print("3. Run all tests before making changes")
        print("=" * 60)

        return len(issues) == 0

    def create_rollback_script(self):
        """Generate a rollback script"""
        script_content = """#!/usr/bin/env python3
# AUTO-GENERATED ROLLBACK SCRIPT
# Created: {timestamp}

import os
import shutil
from datetime import datetime

def rollback():
    print("Starting rollback...")
    print("-" * 40)

    files_to_rollback = {files}

    success_count = 0
    fail_count = 0

    for file_path in files_to_rollback:
        backup_path = file_path + '.backup'
        if os.path.exists(backup_path):
            try:
                # Create safety copy of current
                safety_copy = file_path + f'.before_rollback_{timestamp}'
                shutil.copy2(file_path, safety_copy)

                # Restore from backup
                shutil.copy2(backup_path, file_path)
                print(f"[OK] Rolled back: {{file_path}}")
                success_count += 1
            except Exception as e:
                print(f"[FAIL] Could not rollback {{file_path}}: {{e}}")
                fail_count += 1
        else:
            print(f"[SKIP] No backup for: {{file_path}}")
            fail_count += 1

    print("-" * 40)
    print(f"Rollback complete: {{success_count}} succeeded, {{fail_count}} failed")

    if fail_count == 0:
        print("[SUCCESS] All files rolled back successfully!")
    else:
        print("[WARNING] Some files could not be rolled back")

    return fail_count == 0

if __name__ == "__main__":
    import sys
    success = rollback()
    sys.exit(0 if success else 1)
""".format(
            timestamp=datetime.now().strftime('%Y%m%d_%H%M%S'),
            files=self.critical_files
        )

        script_file = 'emergency_rollback.py'
        with open(script_file, 'w') as f:
            f.write(script_content)

        print(f"\n[CREATED] Emergency rollback script: {script_file}")
        return script_file


def main():
    """Run rollback safety checks"""
    checker = RollbackSafetyCheck()

    # Create checkpoint
    checkpoint = checker.create_safety_checkpoint()

    # Verify rollback capability
    rollback_ready = checker.verify_rollback_capability()

    # Create rollback script
    if rollback_ready:
        rollback_script = checker.create_rollback_script()

    return 0 if rollback_ready else 1


if __name__ == "__main__":
    sys.exit(main())