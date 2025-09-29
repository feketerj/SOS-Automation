"""
Context Accumulator for Multi-Stage Pipeline
Manages context passing between stages and accumulates findings
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field, asdict


@dataclass
class StageDecision:
    """Record of a stage's decision"""
    stage: str
    decision: str
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class KeyFinding:
    """Important finding from a stage"""
    stage: str
    finding_type: str
    value: str
    evidence: str


class ContextAccumulator:
    """Accumulates and manages context across pipeline stages"""

    def __init__(self, opportunity: Dict[str, Any]):
        """Initialize with opportunity data including documents and metadata"""
        # Handle None values properly
        self.opportunity_id = opportunity.get("id") or opportunity.get("search_id") or "unknown"
        self.opportunity_title = opportunity.get("title") or ""
        self.opportunity_text = opportunity.get("text") or opportunity.get("combined_text") or ""

        # PRESERVE ALL METADATA - critical for downstream processing
        self.metadata = opportunity.get("metadata", {})
        self.documents = opportunity.get("documents", [])
        self.original_opportunity = opportunity  # Keep complete original

        # Core accumulation structures
        self.decisions_made: List[StageDecision] = []
        self.key_findings: List[KeyFinding] = []
        self.flags: List[str] = []
        self.knockout_reasons: List[str] = []
        self.exceptions: List[str] = []

        # Summary that grows with each stage
        self.summary = self._initialize_summary(opportunity)

        # Track specific elements found
        self.entities = {
            "platforms": [],
            "companies": [],
            "certifications": [],
            "codes": [],
            "dates": [],
            "dollar_amounts": [],
            "set_asides": [],
            "clearance_levels": []
        }

        # Track document processing
        self.document_stats = {
            "total_documents": len(self.documents),
            "total_chars": len(self.opportunity_text),
            "has_attachments": len(self.documents) > 0,
            "document_types": list(set(d.get("file_type", "unknown") for d in self.documents))
        }

        # Metadata
        self.start_time = datetime.now()
        self.current_stage = 0

    def _initialize_summary(self, opportunity: Dict[str, Any]) -> str:
        """Create initial summary from opportunity"""
        summary_parts = []

        # Try metadata first, then top-level
        metadata = opportunity.get("metadata", {})

        # Extract key info from title
        title = metadata.get("title") or opportunity.get("title")
        if title:
            summary_parts.append(f"Title: {title[:100]}")

        # Extract agency if available
        agency = metadata.get("agency") or opportunity.get("agency")
        if agency:
            summary_parts.append(f"Agency: {agency}")

        # Extract location if available
        location = metadata.get("office") or opportunity.get("location")
        if location:
            summary_parts.append(f"Location: {location}")

        # Add document stats
        if self.documents:
            summary_parts.append(f"Docs: {len(self.documents)}")

        return " | ".join(summary_parts) if summary_parts else "New opportunity"

    def add_stage_result(self, stage_name: str, result: Any):
        """Add results from a completed stage"""
        self.current_stage += 1

        # Handle both dict and object results
        if isinstance(result, dict):
            decision = result.get('decision', 'INDETERMINATE')
            confidence = result.get('confidence', 0.0)
            rationale = result.get('rationale', '')
            evidence = result.get('evidence', [])
        else:
            decision = result.decision.value if hasattr(result.decision, 'value') else str(result.decision)
            confidence = result.confidence
            rationale = getattr(result, 'rationale', '')
            evidence = getattr(result, 'evidence', [])

        # Record decision
        self.decisions_made.append(StageDecision(
            stage=stage_name,
            decision=decision,
            confidence=confidence
        ))

        # Update summary with stage findings
        self._update_summary_with_values(stage_name, decision, rationale)

        # Extract and store key findings
        if evidence:
            for ev in evidence:
                self.key_findings.append(KeyFinding(
                    stage=stage_name,
                    finding_type="evidence",
                    value=ev[:200],  # Truncate long evidence
                    evidence=ev
                ))

        # Add knockout reasons if NO-GO
        if decision == "NO-GO":
            self.knockout_reasons.append(f"{stage_name}: {rationale}")

        # Extract entities based on stage
        self._extract_stage_entities(stage_name, result)

    def _update_summary_with_values(self, stage_name: str, decision: str, rationale: str):
        """Update running summary with stage findings"""
        addition = f" | {stage_name}: {decision}"

        if rationale:
            addition += f" ({rationale[:50]})"

        self.summary += addition

    def _extract_stage_entities(self, stage_name: str, result: Any):
        """Extract specific entities based on stage type"""
        # Handle both dict and object results
        if isinstance(result, dict):
            get_attr = lambda x: result.get(x)
        else:
            get_attr = lambda x: getattr(result, x, None)

        if stage_name == "TIMING":
            deadline = get_attr('deadline_found')
            if deadline:
                self.entities["dates"].append(deadline)

        elif stage_name == "SET-ASIDES":
            set_aside_types = get_attr('set_aside_types')
            if set_aside_types:
                self.entities["set_asides"].extend(set_aside_types if isinstance(set_aside_types, list) else [set_aside_types])

        elif stage_name == "SECURITY":
            clearance = get_attr('clearance_level')
            if clearance:
                self.entities["clearance_levels"].append(clearance)

        elif stage_name == "PLATFORM":
            platforms = get_attr('platforms_found')
            if platforms:
                self.entities["platforms"].extend(platforms if isinstance(platforms, list) else [platforms])

    def add_flag(self, flag: str):
        """Add a flag for special handling"""
        if flag not in self.flags:
            self.flags.append(flag)

    def add_exception(self, exception: str):
        """Add an exception that might allow GO despite knockouts"""
        if exception not in self.exceptions:
            self.exceptions.append(exception)

    def get_context_for_stage(self, stage_number: int) -> Dict[str, Any]:
        """Get context formatted for a specific stage - INCLUDES ALL METADATA AND DOCS"""
        return {
            "opportunity_id": self.opportunity_id,
            "current_stage": stage_number,
            "summary": self.summary,
            "decisions_made": [asdict(d) for d in self.decisions_made],
            "key_findings": [f.value for f in self.key_findings[-10:]],  # Last 10 findings
            "flags": self.flags,
            "entities_found": {k: v for k, v in self.entities.items() if v},
            "has_knockouts": len(self.knockout_reasons) > 0,
            "opportunity_text": self.opportunity_text,  # Full text for analysis
            "metadata": self.metadata,  # ALWAYS forward metadata
            "document_stats": self.document_stats,  # Document info
            "has_documents": len(self.documents) > 0,
            "document_count": len(self.documents)
        }

    def get_full_context(self) -> Dict[str, Any]:
        """Get complete accumulated context - PRESERVES EVERYTHING"""
        processing_time = (datetime.now() - self.start_time).total_seconds()

        return {
            "opportunity_id": self.opportunity_id,
            "opportunity_title": self.opportunity_title,
            "stages_processed": self.current_stage,
            "processing_time": processing_time,
            "summary": self.summary,
            "decisions_made": [asdict(d) for d in self.decisions_made],
            "key_findings": [asdict(f) for f in self.key_findings],
            "knockout_reasons": self.knockout_reasons,
            "exceptions": self.exceptions,
            "flags": self.flags,
            "entities": self.entities,
            "metadata": self.metadata,  # PRESERVE ALL METADATA
            "documents": [{"file_name": d.get("file_name"), "file_type": d.get("file_type")}
                         for d in self.documents],  # Document list without full text
            "document_stats": self.document_stats,
            "final_decision": self._determine_final_decision()
        }

    def _determine_final_decision(self) -> str:
        """Determine overall decision based on accumulated context"""
        # If any NO-GO without override
        for decision in self.decisions_made:
            if decision.decision == "NO-GO":
                return "NO-GO"

        # If all stages passed
        if self.current_stage == 20:  # All stages complete
            return "GO"

        return "INDETERMINATE"

    def to_json(self) -> str:
        """Export context as JSON"""
        return json.dumps(self.get_full_context(), indent=2)


if __name__ == "__main__":
    # Test the context accumulator
    test_opportunity = {
        "id": "FA8606-24-R-0021",
        "title": "P-8 Poseidon Spare Parts",
        "text": "Navy procurement for P-8 aircraft parts...",
        "agency": "Department of Navy",
        "location": "Jacksonville, FL"
    }

    accumulator = ContextAccumulator(test_opportunity)
    print(f"Initial summary: {accumulator.summary}")

    # Simulate adding stage results
    class MockResult:
        def __init__(self, decision, confidence, rationale):
            self.decision = type('Decision', (), {'value': decision})()
            self.confidence = confidence
            self.rationale = rationale
            self.evidence = ["Test evidence"]

    # Add some stage results
    accumulator.add_stage_result("TIMING", MockResult("GO", 0.99, "Deadline in future"))
    accumulator.add_stage_result("SET-ASIDES", MockResult("GO", 0.99, "No set-asides found"))

    print(f"\nContext after 2 stages:")
    print(accumulator.to_json())