"""
Unified Pipeline Output Manager
Ensures ALL pipelines output the same schema format
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json


class UnifiedPipelineOutput:
    """
    Converts any pipeline output to the standard schema defined in schemas/
    Supports both 3-stage and 20-stage pipelines
    """

    @staticmethod
    def format_for_20_stage_pipeline(
        opportunity: Dict[str, Any],
        pipeline_results: Dict[str, Any],
        stage_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Convert 20-stage pipeline output to standard schema

        Args:
            opportunity: Original opportunity data with metadata
            pipeline_results: Results from multi_stage_pipeline
            stage_results: Individual stage results
        """

        # Determine which stage made the final decision
        final_stage = stage_results[-1] if stage_results else None
        knockout_stage = pipeline_results.get("knockout_stage", "")

        # Map stage name to pipeline_stage value
        stage_mapping = {
            "TIMING": "TIMING",
            "SET-ASIDES": "SET_ASIDES",
            "SECURITY": "SECURITY",
            # Add all 20 stages here
            "SCOPE": "SCOPE"
        }

        # Normalize the result to ensure it's valid
        final_decision = pipeline_results.get("final_decision", "INDETERMINATE")
        if final_decision not in ["GO", "NO-GO", "INDETERMINATE", "FURTHER_ANALYSIS", "CONTACT_CO"]:
            final_decision = "INDETERMINATE"

        # Build standard output
        output = {
            # Core decision fields (Required)
            "result": final_decision,

            # Rationale from the deciding stage
            "rationale": final_stage.get("rationale", "") if final_stage else "",

            # Pipeline title (construct from stages)
            "sos_pipeline_title": f"20-Stage Assessment - Stopped at {knockout_stage}" if knockout_stage else "20-Stage Complete Assessment",

            # URLs (from opportunity metadata)
            "sam_url": opportunity.get("metadata", {}).get("sam_url", ""),
            "highergov_url": opportunity.get("metadata", {}).get("url") or f"https://app.highergov.com/opportunities/{opportunity.get('search_id', '')}",

            # Announcement details (ensure required fields have values)
            "announcement_number": opportunity.get("search_id") or "UNKNOWN",
            "announcement_title": opportunity.get("metadata", {}).get("title") or "No Title Available",
            "agency": opportunity.get("metadata", {}).get("agency") or "Unknown Agency",

            # Pipeline stage where decision was made
            "pipeline_stage": knockout_stage or "COMPLETE",

            # Assessment type for 20-stage
            "assessment_type": "MULTI_STAGE_ASSESSMENT",

            # Additional fields for tracking
            "stages_processed": pipeline_results.get("stages_processed", 0),
            "total_stages": pipeline_results.get("total_stages", 20),

            # If there was a knockout, add the pattern
            "knock_pattern": final_stage.get("evidence", []) if final_stage and pipeline_results.get("final_decision") == "NO-GO" else None,

            # Knockout category based on stage
            "knockout_category": UnifiedPipelineOutput._get_knockout_category(knockout_stage) if knockout_stage else None,

            # Stage details (extended field)
            "stage_results": stage_results,

            # Timing
            "processing_time": pipeline_results.get("processing_time", 0),
            "timestamp": pipeline_results.get("timestamp", datetime.now().isoformat())
        }

        # Remove None values to match schema
        output = {k: v for k, v in output.items() if v is not None}

        return output

    @staticmethod
    def format_for_3_stage_pipeline(assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure 3-stage pipeline output matches schema
        This is mostly pass-through since it should already match
        """
        # The existing pipeline should already match the schema
        # This just ensures consistency

        required_fields = {
            "result": assessment.get("result", assessment.get("final_decision", "INDETERMINATE")),
            "announcement_title": assessment.get("announcement_title", assessment.get("solicitation_title", "")),
        }

        # Merge with existing data
        return {**assessment, **required_fields}

    @staticmethod
    def format_for_specialized_agent(
        agent_name: str,
        stage_name: str,
        agent_response: Dict[str, Any],
        opportunity: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format output from a specialized agent (future state)

        Args:
            agent_name: Name of the specialized agent (e.g., "timing_specialist")
            stage_name: Stage being processed (e.g., "TIMING")
            agent_response: Response from the agent
            opportunity: Original opportunity data
        """

        output = {
            # Core fields
            "result": agent_response.get("decision", "INDETERMINATE"),
            "rationale": agent_response.get("rationale", ""),

            # Agent-specific title
            "sos_pipeline_title": f"{agent_name} Assessment - Stage {stage_name}",

            # URLs and metadata from opportunity
            "sam_url": opportunity.get("metadata", {}).get("sam_url", ""),
            "highergov_url": opportunity.get("metadata", {}).get("url", ""),
            "announcement_number": opportunity.get("search_id", ""),
            "announcement_title": opportunity.get("metadata", {}).get("title", ""),
            "agency": opportunity.get("metadata", {}).get("agency", ""),

            # Pipeline tracking
            "pipeline_stage": stage_name,
            "assessment_type": f"SPECIALIST_{stage_name}",

            # Agent tracking
            "agent_used": agent_name,
            "agent_confidence": agent_response.get("confidence", 0),

            # Evidence from agent
            "evidence": agent_response.get("evidence", []),

            # Timestamp
            "timestamp": datetime.now().isoformat()
        }

        return output

    @staticmethod
    def _get_knockout_category(stage_name: str) -> str:
        """
        Map stage names to knockout category codes
        """
        category_map = {
            "TIMING": "KO-01",
            "SET-ASIDES": "KO-02",
            "SECURITY": "KO-03",
            "NON-STANDARD": "KO-04",
            "CONTRACT-VEHICLE": "KO-05",
            "EXPORT-CONTROL": "KO-06",
            "AMC-AMSC": "KO-07",
            "SOURCE-RESTRICTIONS": "KO-08",
            "SAR": "KO-09",
            "PLATFORM": "KO-10",
            "DOMAIN": "KO-11",
            "TECHNICAL-DATA": "KO-12",
            "IT-SYSTEMS": "KO-13",
            "CERTIFICATIONS": "KO-14",
            "SUBCONTRACTING": "KO-15",
            "PROCUREMENT": "KO-16",
            "COMPETITION": "KO-17",
            "MAINTENANCE": "KO-18",
            "CAD-CAM": "KO-19",
            "SCOPE": "KO-20"
        }

        return category_map.get(stage_name, "KO-00")

    @staticmethod
    def validate_against_schema(output: Dict[str, Any], stage_type: str = "agent") -> bool:
        """
        Validate output against the appropriate schema

        Args:
            output: The formatted output
            stage_type: One of "regex", "batch", "agent"
        """
        # Check required fields based on stage type
        if stage_type == "regex":
            required = ["result", "announcement_title"]
            expected_stage = "APP"
            expected_type = "APP_KNOCKOUT"
        elif stage_type == "batch":
            required = ["result", "announcement_title"]
            expected_stage = "BATCH"
            expected_type = "MISTRAL_BATCH_ASSESSMENT"
        else:  # agent
            required = ["result", "announcement_title"]
            expected_stage = "AGENT"
            expected_type = "MISTRAL_ASSESSMENT"

        # Check required fields
        for field in required:
            if field not in output or not output[field]:
                print(f"Missing required field: {field}")
                return False

        # Check result enum
        valid_results = ["GO", "NO-GO", "INDETERMINATE", "FURTHER_ANALYSIS", "CONTACT_CO"]
        if output.get("result") not in valid_results:
            print(f"Invalid result value: {output.get('result')}")
            return False

        return True

    @staticmethod
    def write_all_formats(output: Dict[str, Any], output_dir: Path):
        """
        Write output in all required formats

        Args:
            output: Formatted output matching schema
            output_dir: Directory to write files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 1. JSON (complete data)
        with open(output_dir / "assessment.json", "w") as f:
            json.dump(output, f, indent=2)

        # 2. CSV (key fields)
        import csv
        csv_fields = [
            "result", "announcement_title", "agency", "announcement_number",
            "sam_url", "highergov_url", "rationale", "pipeline_stage",
            "knockout_category", "processing_time"
        ]

        with open(output_dir / "assessment.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=csv_fields)
            writer.writeheader()
            writer.writerow({k: output.get(k, "") for k in csv_fields})

        # 3. Markdown report
        with open(output_dir / "report.md", "w") as f:
            f.write(f"# SOS Assessment Report\n\n")
            f.write(f"**Generated:** {output.get('timestamp', datetime.now().isoformat())}\n\n")
            f.write(f"## Decision: {output.get('result')}\n\n")
            f.write(f"**Opportunity:** {output.get('announcement_title')}\n")
            f.write(f"**ID:** {output.get('announcement_number')}\n")
            f.write(f"**Agency:** {output.get('agency')}\n\n")
            f.write(f"### Rationale\n{output.get('rationale', 'No rationale provided')}\n\n")

            if output.get("stage_results"):
                f.write("### Stage Progression\n")
                for stage in output.get("stage_results", []):
                    f.write(f"- **{stage.get('stage_name')}**: {stage.get('decision')} ")
                    f.write(f"(confidence: {stage.get('confidence', 0):.2f})\n")

            f.write(f"\n### Links\n")
            if output.get("sam_url"):
                f.write(f"- [SAM.gov]({output.get('sam_url')})\n")
            if output.get("highergov_url"):
                f.write(f"- [HigherGov]({output.get('highergov_url')})\n")

        # 4. GO-only CSV (if applicable)
        if output.get("result") == "GO":
            with open(output_dir / "GO_opportunities.csv", "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=csv_fields)
                writer.writeheader()
                writer.writerow({k: output.get(k, "") for k in csv_fields})

        print(f"Outputs written to: {output_dir}")


# Example usage for 20-stage pipeline integration
def integrate_with_multi_stage_pipeline():
    """
    Example of how to integrate with multi_stage_pipeline.py
    """
    from multi_stage_pipeline import MultiStagePipeline

    # In multi_stage_pipeline.py, update _build_output method:
    """
    def _build_output(self, opportunity, context, results):
        # Get raw pipeline output
        raw_output = {
            "opportunity_id": opportunity.get("id"),
            "final_decision": results[-1].decision.value if results else "INDETERMINATE",
            "stages_processed": len(results),
            # ... etc
        }

        # Convert to standard schema
        from unified_pipeline_output import UnifiedPipelineOutput

        stage_results = [
            {
                "stage_name": r.stage_name,
                "decision": r.decision.value,
                "confidence": r.confidence,
                "evidence": r.evidence,
                "rationale": r.rationale,
                "processing_time": r.processing_time
            }
            for r in results
        ]

        formatted_output = UnifiedPipelineOutput.format_for_20_stage_pipeline(
            opportunity=opportunity,
            pipeline_results=raw_output,
            stage_results=stage_results
        )

        # Validate against schema
        if UnifiedPipelineOutput.validate_against_schema(formatted_output, "agent"):
            return formatted_output
        else:
            print("WARNING: Output does not match schema!")
            return formatted_output
    """
    pass


if __name__ == "__main__":
    # Test the formatter
    test_opportunity = {
        "search_id": "fa860624r0076",
        "metadata": {
            "title": "Aircraft Parts for P-8",
            "agency": "Department of Navy",
            "url": "https://app.highergov.com/opportunities/fa860624r0076"
        }
    }

    test_pipeline_results = {
        "final_decision": "NO-GO",
        "stages_processed": 3,
        "total_stages": 20,
        "knockout_stage": "SECURITY",
        "processing_time": 45.2,
        "timestamp": datetime.now().isoformat()
    }

    test_stage_results = [
        {"stage_name": "TIMING", "decision": "GO", "confidence": 0.99, "rationale": "Deadline in future"},
        {"stage_name": "SET-ASIDES", "decision": "GO", "confidence": 0.99, "rationale": "Full and open"},
        {"stage_name": "SECURITY", "decision": "NO-GO", "confidence": 0.99, "rationale": "Secret clearance required"}
    ]

    # Format for 20-stage pipeline
    formatted = UnifiedPipelineOutput.format_for_20_stage_pipeline(
        test_opportunity,
        test_pipeline_results,
        test_stage_results
    )

    print("Formatted Output:")
    print(json.dumps(formatted, indent=2))

    # Validate
    is_valid = UnifiedPipelineOutput.validate_against_schema(formatted, "agent")
    print(f"\nValid against schema: {is_valid}")

    # Write all formats
    UnifiedPipelineOutput.write_all_formats(formatted, Path("test_output"))