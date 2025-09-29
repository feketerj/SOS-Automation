"""
Test Script for Multi-Stage Pipeline Proof of Concept
Tests the first 3 stages of the 20-stage pipeline
"""

import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List

# Import pipeline components
from multi_stage_pipeline import MultiStagePipeline, Decision, StageResult
from context_accumulator import ContextAccumulator
from qc_agents import QCAgent

# Import stage processors
from stage_processors.stage_01_timing import TimingStage
from stage_processors.stage_02_set_asides import SetAsidesStage
from stage_processors.stage_03_security import SecurityStage

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TestPipeline:
    """Test harness for multi-stage pipeline"""

    def __init__(self):
        self.timing_stage = TimingStage()
        self.set_asides_stage = SetAsidesStage()
        self.security_stage = SecurityStage()
        self.qc_agent = QCAgent()

    def create_test_opportunities(self) -> List[Dict]:
        """Create test opportunities with known outcomes"""
        future_date = (datetime.now() + timedelta(days=30)).strftime("%B %d, %Y")
        past_date = (datetime.now() - timedelta(days=5)).strftime("%B %d, %Y")

        return [
            {
                "id": "TEST-001",
                "title": "Commercial Aircraft Parts",
                "text": f"""
                Solicitation for Boeing 737 spare parts.
                Response deadline: {future_date}
                This is an unrestricted, full and open competition.
                No security clearance required.
                Commercial items only.
                """,
                "expected": "GO",
                "expected_stage": "COMPLETE"
            },
            {
                "id": "TEST-002",
                "title": "Expired Opportunity",
                "text": f"""
                F-16 maintenance services required.
                Proposals were due by {past_date}.
                Secret clearance required.
                """,
                "expected": "NO-GO",
                "expected_stage": "TIMING"
            },
            {
                "id": "TEST-003",
                "title": "Small Business Set-Aside",
                "text": f"""
                IT Support Services
                Response due: {future_date}
                This procurement is set aside for 8(a) certified small businesses.
                NAICS 541512, Size Standard $30M
                """,
                "expected": "NO-GO",
                "expected_stage": "SET-ASIDES"
            },
            {
                "id": "TEST-004",
                "title": "Security Clearance Required",
                "text": f"""
                Cybersecurity Assessment Services
                Closing date: {future_date}
                Full and open competition
                Contractor must possess Secret clearance and facility clearance.
                Work involves classified systems.
                """,
                "expected": "NO-GO",
                "expected_stage": "SECURITY"
            },
            {
                "id": "TEST-005",
                "title": "P-8 Poseidon Parts (Navy)",
                "text": f"""
                Department of Navy
                P-8 Poseidon aircraft spare parts
                Deadline: {future_date}
                Unrestricted procurement
                FAA Form 8130-3 certification acceptable
                No security clearance required
                """,
                "expected": "GO",
                "expected_stage": "COMPLETE",
                "note": "P-8 is commercial 737 derivative"
            }
        ]

    async def process_opportunity_through_stages(self, opportunity: Dict) -> Dict:
        """Process opportunity through first 3 stages"""
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {opportunity['id']} - {opportunity['title']}")
        logger.info(f"Expected: {opportunity['expected']} at stage {opportunity['expected_stage']}")

        # Initialize context
        context_accumulator = ContextAccumulator(opportunity)
        results = []

        # Stage 1: Timing
        logger.info("\nStage 1: TIMING")
        timing_result = self.timing_stage.process(
            context_accumulator.get_context_for_stage(1),
            opportunity["text"]
        )
        results.append(timing_result)
        context_accumulator.add_stage_result("TIMING", timing_result)
        logger.info(f"  Decision: {timing_result['decision']} (confidence: {timing_result['confidence']})")

        if timing_result["decision"] == "NO-GO":
            logger.info("  KNOCKOUT at TIMING stage")
            # Run QC verification
            qc_result = await self._mock_qc_verification("TIMING", timing_result, context_accumulator)
            if not qc_result or qc_result.qc_decision == "NO-GO":
                return self._build_result(opportunity, results, context_accumulator, "TIMING")

        # Stage 2: Set-Asides
        logger.info("\nStage 2: SET-ASIDES")
        set_aside_result = self.set_asides_stage.process(
            context_accumulator.get_context_for_stage(2),
            opportunity["text"]
        )
        results.append(set_aside_result)
        context_accumulator.add_stage_result("SET-ASIDES", set_aside_result)
        logger.info(f"  Decision: {set_aside_result['decision']} (confidence: {set_aside_result['confidence']})")

        if set_aside_result["decision"] == "NO-GO":
            logger.info("  KNOCKOUT at SET-ASIDES stage")
            # Run QC verification
            qc_result = await self._mock_qc_verification("SET-ASIDES", set_aside_result, context_accumulator)
            if not qc_result or qc_result.qc_decision == "NO-GO":
                return self._build_result(opportunity, results, context_accumulator, "SET-ASIDES")

        # Stage 3: Security
        logger.info("\nStage 3: SECURITY")
        security_result = self.security_stage.process(
            context_accumulator.get_context_for_stage(3),
            opportunity["text"]
        )
        results.append(security_result)
        context_accumulator.add_stage_result("SECURITY", security_result)
        logger.info(f"  Decision: {security_result['decision']} (confidence: {security_result['confidence']})")

        if security_result["decision"] == "NO-GO":
            logger.info("  KNOCKOUT at SECURITY stage")
            # Run QC verification
            qc_result = await self._mock_qc_verification("SECURITY", security_result, context_accumulator)
            if not qc_result or qc_result.qc_decision == "NO-GO":
                return self._build_result(opportunity, results, context_accumulator, "SECURITY")

        # All 3 stages passed
        logger.info("\nAll 3 stages passed - would continue to remaining 17 stages")
        return self._build_result(opportunity, results, context_accumulator, "COMPLETE")

    async def _mock_qc_verification(self, stage_name: str, result: Dict, context: ContextAccumulator):
        """Mock QC verification (would call actual API)"""
        logger.info(f"  Running QC verification for {stage_name} NO-GO...")
        # For testing, we'll accept all NO-GOs
        logger.info(f"  QC confirms NO-GO decision")
        return None

    def _build_result(self, opportunity: Dict, results: List[Dict],
                     context: ContextAccumulator, final_stage: str) -> Dict:
        """Build final result structure"""
        final_decision = "NO-GO" if any(r["decision"] == "NO-GO" for r in results) else "GO"

        return {
            "opportunity_id": opportunity["id"],
            "title": opportunity["title"],
            "final_decision": final_decision,
            "final_stage": final_stage,
            "stages_processed": len(results),
            "expected_outcome": opportunity["expected"],
            "expected_stage": opportunity["expected_stage"],
            "test_passed": final_decision == opportunity["expected"] and final_stage == opportunity["expected_stage"],
            "stage_results": results,
            "accumulated_context": context.get_full_context()
        }

    async def run_tests(self):
        """Run all test cases"""
        logger.info("Starting Multi-Stage Pipeline Test")
        logger.info("Testing first 3 stages: TIMING, SET-ASIDES, SECURITY")

        test_opportunities = self.create_test_opportunities()
        results = []

        for opportunity in test_opportunities:
            result = await self.process_opportunity_through_stages(opportunity)
            results.append(result)

        # Summary
        logger.info(f"\n{'='*60}")
        logger.info("TEST SUMMARY")
        logger.info(f"{'='*60}")

        passed = sum(1 for r in results if r["test_passed"])
        total = len(results)

        for result in results:
            status = "✓ PASS" if result["test_passed"] else "✗ FAIL"
            logger.info(f"{status} - {result['opportunity_id']}: "
                       f"Expected {result['expected_outcome']} at {result['expected_stage']}, "
                       f"Got {result['final_decision']} at {result['final_stage']}")

        logger.info(f"\nResults: {passed}/{total} tests passed")

        # Save detailed results
        with open("test_pipeline_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        logger.info("\nDetailed results saved to test_pipeline_results.json")

        return passed == total


async def main():
    """Main test execution"""
    tester = TestPipeline()
    success = await tester.run_tests()

    if success:
        logger.info("\n✓ All tests passed! Ready to implement remaining 17 stages.")
    else:
        logger.info("\n✗ Some tests failed. Review results before proceeding.")

    return success


if __name__ == "__main__":
    # Run the test
    success = asyncio.run(main())
    exit(0 if success else 1)