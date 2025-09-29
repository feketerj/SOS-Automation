"""
Test Multi-Stage Pipeline with Mock Mode
Tests the pipeline without making real API calls
"""

import asyncio
import json
import sys
from datetime import datetime

# Import pipeline components
from multi_stage_pipeline import MultiStagePipeline
from pipeline_config import PIPELINE_CONFIG


async def test_mock_pipeline():
    """Test pipeline in mock mode"""
    print("\n" + "="*70)
    print("TESTING MULTI-STAGE PIPELINE (MOCK MODE)")
    print("="*70)
    print(f"Started: {datetime.now()}")
    print("\nThis test uses mock responses - no real API calls will be made")

    # Initialize pipeline in mock mode
    pipeline = MultiStagePipeline(mock_mode=True)

    # Test opportunities
    test_cases = [
        {
            "id": "MOCK-001",
            "name": "Commercial Aircraft Parts",
            "description": "Should pass all stages - commercial Boeing 737 parts"
        },
        {
            "id": "MOCK-002",
            "name": "Expired Opportunity",
            "description": "Should fail at TIMING stage - expired deadline"
        },
        {
            "id": "MOCK-003",
            "name": "Small Business Set-Aside",
            "description": "Should fail at SET-ASIDES stage - 8(a) requirement"
        },
        {
            "id": "MOCK-004",
            "name": "Security Clearance Required",
            "description": "Should fail at SECURITY stage - Top Secret required"
        },
        {
            "id": "MOCK-005",
            "name": "Military Platform",
            "description": "Should fail at PLATFORM stage - F-16 fighter jet"
        }
    ]

    results = []

    for test_case in test_cases:
        print(f"\n{'='*50}")
        print(f"Test Case: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"ID: {test_case['id']}")
        print("="*50)

        try:
            # Process through pipeline
            result = await pipeline.process_opportunity_with_documents(test_case['id'])

            # Display key results
            print(f"\nRESULT:")
            print(f"  Final Decision: {result.get('final_decision')}")
            print(f"  Stages Processed: {result.get('stages_processed')}/{result.get('total_stages')}")

            if result.get('knockout_stage'):
                print(f"  Knockout Stage: {result['knockout_stage']}")

            # Show stage-by-stage results
            if result.get('stage_results'):
                print("\n  Stage Results:")
                for stage_result in result['stage_results']:
                    print(f"    - {stage_result['stage_name']}: "
                          f"{stage_result['decision']} "
                          f"(confidence: {stage_result['confidence']:.2f})")

                    # Stop at knockout
                    if stage_result['decision'] == 'NO_GO':
                        break

            results.append({
                "test_case": test_case['name'],
                "expected": test_case['description'],
                "actual": result.get('final_decision'),
                "knockout_stage": result.get('knockout_stage'),
                "success": True
            })

        except Exception as e:
            print(f"\nERROR: {e}")
            results.append({
                "test_case": test_case['name'],
                "expected": test_case['description'],
                "actual": "ERROR",
                "error": str(e),
                "success": False
            })

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    for i, result in enumerate(results, 1):
        status = "PASS" if result['success'] else "FAIL"
        print(f"{i}. {result['test_case']}: {status}")
        if result.get('error'):
            print(f"   Error: {result['error']}")
        else:
            print(f"   Result: {result['actual']}")
            if result.get('knockout_stage'):
                print(f"   Knockout: {result['knockout_stage']}")

    # Overall success
    total_pass = sum(1 for r in results if r['success'])
    total = len(results)
    print(f"\nOverall: {total_pass}/{total} tests passed")

    return results


def test_synchronous():
    """Test using synchronous wrapper"""
    print("\n" + "="*70)
    print("SYNCHRONOUS TEST WITH MOCK MODE")
    print("="*70)

    pipeline = MultiStagePipeline(mock_mode=True)

    # Create a simple test opportunity
    test_opp = {
        "search_id": "SYNC-TEST-001",
        "metadata": {
            "title": "Test Synchronous Opportunity",
            "agency": "Test Agency",
            "response_date_time": "2025-12-31 17:00:00"
        },
        "documents": [],
        "combined_text": "Test opportunity with deadline December 31, 2025. Full and open competition.",
        "fetch_status": "complete"
    }

    # Process synchronously
    result = asyncio.run(pipeline.process_opportunity(test_opp))

    print(f"\nSynchronous Test Result:")
    print(f"  Decision: {result.get('final_decision')}")
    print(f"  Stages: {result.get('stages_processed')}/{result.get('total_stages')}")

    return result


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("MULTI-STAGE PIPELINE MOCK TEST SUITE")
    print("="*70)

    # Test 1: Async mock pipeline
    print("\nRunning async mock tests...")
    async_results = asyncio.run(test_mock_pipeline())

    # Test 2: Synchronous test
    print("\nRunning synchronous test...")
    sync_result = test_synchronous()

    # Final summary
    print("\n" + "="*70)
    print("ALL TESTS COMPLETE")
    print("="*70)

    async_pass = sum(1 for r in async_results if r['success'])
    print(f"Async Tests: {async_pass}/{len(async_results)} passed")
    print(f"Sync Test: {'PASS' if sync_result.get('final_decision') else 'FAIL'}")

    # Check if everything works
    all_pass = async_pass == len(async_results) and sync_result.get('final_decision')

    if all_pass:
        print("\nSUCCESS: All mock tests passed - pipeline is working correctly")
        return 0
    else:
        print("\nWARNING: Some tests failed - review results above")
        return 1


if __name__ == "__main__":
    sys.exit(main())