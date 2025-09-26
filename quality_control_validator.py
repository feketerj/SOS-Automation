#!/usr/bin/env python3
"""
Quality Control Validator - Comprehensive validation suite for bug fixes
Ensures all changes maintain system stability and data integrity
"""

import json
import time
import sys
from typing import Dict, List, Tuple, Any
from decision_sanitizer import DecisionSanitizer
from enhanced_output_manager import EnhancedOutputManager

class QualityControlValidator:
    """Validates bug fixes against quality control criteria"""

    def __init__(self):
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': [],
            'metrics': {}
        }

    def run_all_validations(self) -> bool:
        """Run complete validation suite"""
        print("=" * 70)
        print("QUALITY CONTROL VALIDATION SUITE")
        print("=" * 70)

        # Track overall success
        all_passed = True

        # 1. Schema Compliance
        print("\n1. SCHEMA COMPLIANCE VALIDATION")
        print("-" * 40)
        if not self.validate_schema_compliance():
            all_passed = False

        # 2. URL Field Preservation (Bug #4)
        print("\n2. URL FIELD PRESERVATION (Bug #4)")
        print("-" * 40)
        if not self.validate_url_preservation():
            all_passed = False

        # 3. Assessment Type Normalization (Bug #2)
        print("\n3. ASSESSMENT TYPE NORMALIZATION (Bug #2)")
        print("-" * 40)
        if not self.validate_assessment_types():
            all_passed = False

        # 4. Backward Compatibility
        print("\n4. BACKWARD COMPATIBILITY")
        print("-" * 40)
        if not self.validate_backward_compatibility():
            all_passed = False

        # 5. Performance Impact
        print("\n5. PERFORMANCE VALIDATION")
        print("-" * 40)
        if not self.validate_performance():
            all_passed = False

        # 6. Data Integrity
        print("\n6. DATA INTEGRITY CHECKS")
        print("-" * 40)
        if not self.validate_data_integrity():
            all_passed = False

        # Summary Report
        self.print_summary()

        return all_passed

    def validate_schema_compliance(self) -> bool:
        """Verify all outputs match unified schema"""
        test_cases = [
            {'decision': 'GO', 'title': 'Test'},
            {'result': 'NO-GO', 'solicitation_title': 'Test'},
            {'assessment': {'decision': 'INDETERMINATE'}, 'title': 'Test'}
        ]

        for i, test_input in enumerate(test_cases, 1):
            sanitized = DecisionSanitizer.sanitize(test_input)

            # Check required fields
            required_fields = [
                'solicitation_id', 'solicitation_title', 'summary',
                'result', 'knock_out_reasons', 'exceptions',
                'special_action', 'rationale', 'recommendation',
                'sam_url', 'hg_url', 'pipeline_stage', 'assessment_type'
            ]

            missing = [f for f in required_fields if f not in sanitized]
            if missing:
                self.results['failed'].append(f"Schema test {i}: Missing fields {missing}")
                print(f"  [FAIL] Test {i}: Missing required fields: {missing}")
                return False
            else:
                self.results['passed'].append(f"Schema test {i}: All fields present")
                print(f"  [PASS] Test {i}: All required fields present")

        return True

    def validate_url_preservation(self) -> bool:
        """Verify URL fields are preserved through pipeline"""
        test_data = {
            'sam_url': 'https://sam.gov/test123',
            'hg_url': 'https://highergov.com/test123',
            'title': 'Test Opportunity',
            'decision': 'GO'
        }

        # Test through sanitizer
        sanitized = DecisionSanitizer.sanitize(test_data)

        # Check URL preservation
        if sanitized.get('sam_url') != test_data['sam_url']:
            self.results['failed'].append("SAM URL not preserved")
            print(f"  [FAIL] SAM URL not preserved")
            return False

        if sanitized.get('hg_url') != test_data['hg_url']:
            self.results['failed'].append("HG URL not preserved")
            print(f"  [FAIL] HigherGov URL not preserved")
            return False

        self.results['passed'].append("URL fields properly preserved")
        print(f"  [PASS] Both URL fields preserved correctly")
        return True

    def validate_assessment_types(self) -> bool:
        """Verify assessment type normalization works"""

        # Test mapping of legacy types
        legacy_mappings = {
            'AGENT_VERIFIED': 'MISTRAL_ASSESSMENT',
            'REGEX_KNOCKOUT': 'APP_KNOCKOUT',
            'REGEX_ONLY': 'APP_KNOCKOUT',
            'BATCH_AI': 'MISTRAL_BATCH_ASSESSMENT'
        }

        all_correct = True
        for legacy, expected in legacy_mappings.items():
            test_data = {
                'processing_method': legacy,
                'decision': 'GO',
                'title': 'Test'
            }

            sanitized = DecisionSanitizer.sanitize(test_data)
            actual = sanitized.get('assessment_type', '')

            if actual != expected:
                self.results['failed'].append(f"{legacy} not mapped to {expected}")
                print(f"  [FAIL] {legacy} -> {actual} (expected {expected})")
                all_correct = False
            else:
                self.results['passed'].append(f"{legacy} correctly mapped")
                print(f"  [PASS] {legacy} -> {expected}")

        return all_correct

    def validate_backward_compatibility(self) -> bool:
        """Ensure existing data structures still work"""

        # Test legacy nested format
        legacy_data = {
            'assessment': {
                'decision': 'NO-GO',
                'reasoning': 'Test reason'
            },
            'title': 'Legacy Test'
        }

        sanitized = DecisionSanitizer.sanitize(legacy_data)

        # Check decision was extracted
        if sanitized.get('result') != 'NO-GO':
            self.results['failed'].append("Legacy nested format not handled")
            print(f"  [FAIL] Legacy nested decision not extracted")
            return False

        # Check reasoning was preserved
        if 'Test reason' not in sanitized.get('rationale', ''):
            self.results['failed'].append("Legacy reasoning not preserved")
            print(f"  [FAIL] Legacy reasoning not preserved")
            return False

        self.results['passed'].append("Backward compatibility maintained")
        print(f"  [PASS] Legacy formats handled correctly")
        return True

    def validate_performance(self) -> bool:
        """Ensure no significant performance degradation"""

        test_data = {
            'processing_method': 'AGENT_VERIFIED',
            'decision': 'GO',
            'title': 'Performance Test',
            'sam_url': 'https://sam.gov/test',
            'hg_url': 'https://highergov.com/test'
        }

        # Measure sanitization time
        iterations = 1000
        start_time = time.perf_counter()

        for _ in range(iterations):
            DecisionSanitizer.sanitize(test_data)

        end_time = time.perf_counter()
        avg_time_ms = ((end_time - start_time) / iterations) * 1000

        self.results['metrics']['avg_sanitization_ms'] = avg_time_ms

        # Check if under 1ms threshold
        if avg_time_ms > 1.0:
            self.results['warnings'].append(f"Sanitization taking {avg_time_ms:.2f}ms average")
            print(f"  [WARN] Average sanitization time: {avg_time_ms:.2f}ms (threshold: 1ms)")
            return False
        else:
            self.results['passed'].append(f"Performance acceptable: {avg_time_ms:.2f}ms")
            print(f"  [PASS] Average sanitization time: {avg_time_ms:.2f}ms")
            return True

    def validate_data_integrity(self) -> bool:
        """Verify no data loss during transformations"""

        # Test with fully populated data
        complete_data = {
            'solicitation_id': 'TEST123',
            'solicitation_title': 'Test Title',
            'summary': 'Test Summary',
            'decision': 'GO',
            'knock_pattern': 'Test Pattern',
            'agency': 'Test Agency',
            'sam_url': 'https://sam.gov/test',
            'hg_url': 'https://highergov.com/test',
            'processing_method': 'AGENT_VERIFIED',
            'naics': '123456',
            'psc': '1234',
            'set_aside': 'SBA',
            'value_low': 10000,
            'value_high': 50000
        }

        sanitized = DecisionSanitizer.sanitize(complete_data)

        # Check critical fields preserved
        critical_fields = ['solicitation_id', 'solicitation_title', 'agency',
                          'naics', 'psc', 'set_aside', 'value_low', 'value_high']

        lost_fields = []
        for field in critical_fields:
            if field in complete_data and field not in sanitized:
                lost_fields.append(field)

        if lost_fields:
            self.results['failed'].append(f"Data loss detected: {lost_fields}")
            print(f"  [FAIL] Fields lost during transformation: {lost_fields}")
            return False

        self.results['passed'].append("No data loss detected")
        print(f"  [PASS] All critical fields preserved")
        return True

    def print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)

        total_tests = len(self.results['passed']) + len(self.results['failed'])
        pass_rate = (len(self.results['passed']) / total_tests * 100) if total_tests > 0 else 0

        print(f"\nTests Run: {total_tests}")
        print(f"Passed: {len(self.results['passed'])}")
        print(f"Failed: {len(self.results['failed'])}")
        print(f"Warnings: {len(self.results['warnings'])}")
        print(f"Pass Rate: {pass_rate:.1f}%")

        if self.results['metrics']:
            print("\nPerformance Metrics:")
            for metric, value in self.results['metrics'].items():
                print(f"  {metric}: {value:.3f}")

        if self.results['failed']:
            print("\nFailed Tests:")
            for failure in self.results['failed']:
                print(f"  - {failure}")

        if self.results['warnings']:
            print("\nWarnings:")
            for warning in self.results['warnings']:
                print(f"  - {warning}")

        print("\n" + "=" * 70)
        if len(self.results['failed']) == 0:
            print("[SUCCESS] All quality control validations passed!")
        else:
            print("[FAILURE] Some validations failed. Review details above.")
        print("=" * 70)


def main():
    """Run the quality control validation suite"""
    validator = QualityControlValidator()
    success = validator.run_all_validations()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())