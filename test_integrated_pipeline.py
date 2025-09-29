"""
Test the integrated multi-stage pipeline with unified output
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

# Import the integrated pipeline
from multi_stage_pipeline import MultiStagePipeline
from unified_pipeline_output import UnifiedPipelineOutput


async def test_integrated_pipeline():
    """Test the pipeline with unified output"""
    print("\n" + "="*70)
    print("INTEGRATED PIPELINE TEST WITH UNIFIED OUTPUT")
    print("="*70)
    print(f"Started: {datetime.now()}")

    # Initialize pipeline in mock mode
    pipeline = MultiStagePipeline(mock_mode=True)

    # Test opportunity
    test_opportunity = {
        "search_id": "INTEGRATED-TEST-001",
        "metadata": {
            "title": "Integrated Test Opportunity",
            "agency": "Test Agency",
            "office": "Test Office",
            "response_date_time": "2025-12-31 17:00:00",
            "sam_url": "https://sam.gov/opp/test",
            "url": "https://app.highergov.com/opportunities/INTEGRATED-TEST-001"
        },
        "documents": [
            {
                "file_name": "test_doc.pdf",
                "text": "This is a test with deadline December 31, 2025. Full and open. Secret clearance required."
            }
        ],
        "combined_text": "Test opportunity with Secret clearance requirement.",
        "fetch_status": "complete"
    }

    try:
        # Process through pipeline
        result = await pipeline.process_opportunity(test_opportunity)

        print("\nPIPELINE OUTPUT:")
        print(json.dumps(result, indent=2, default=str))

        # Check key fields
        print("\nKEY FIELDS CHECK:")
        print(f"  result: {result.get('result')}")
        print(f"  announcement_title: {result.get('announcement_title')}")
        print(f"  pipeline_stage: {result.get('pipeline_stage')}")
        print(f"  assessment_type: {result.get('assessment_type')}")
        print(f"  knockout_category: {result.get('knockout_category')}")

        # Validate against schema
        is_valid = UnifiedPipelineOutput.validate_against_schema(result, "agent")
        print(f"\nSchema Validation: {'PASS' if is_valid else 'FAIL'}")

        # Write output files
        output_dir = Path("integrated_test_output")
        UnifiedPipelineOutput.write_all_formats(result, output_dir)
        print(f"\nOutput files written to: {output_dir}")

        # List the files created
        if output_dir.exists():
            print("\nFiles created:")
            for file in output_dir.iterdir():
                print(f"  - {file.name}")

        return is_valid

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run the integrated test"""
    success = asyncio.run(test_integrated_pipeline())

    print("\n" + "="*70)
    if success:
        print("SUCCESS: Integrated pipeline with unified output is working!")
    else:
        print("FAILED: Integration issues detected")
    print("="*70)

    return 0 if success else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())