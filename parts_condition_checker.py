#!/usr/bin/env python3
"""
Parts Condition Checker V4.19
Determines if surplus/refurbished parts are acceptable based on solicitation requirements.
SOS specializes in FAA-certified refurbished and surplus parts.
"""

import re
from enum import Enum
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class PartsCondition(Enum):
    """Parts condition requirements."""
    NEW_ONLY = "NEW_ONLY"           # Factory new required - NO-GO for SOS
    REFURB_OK = "REFURB_OK"          # Refurbished acceptable - GO for SOS
    SURPLUS_OK = "SURPLUS_OK"        # Surplus acceptable - GO for SOS
    ANY_CONDITION = "ANY_CONDITION"  # Any condition acceptable - GO for SOS
    UNSPECIFIED = "UNSPECIFIED"      # Not specified - needs analysis


class ConditionDecision(Enum):
    """Assessment decision for parts condition."""
    GO = "GO"                        # SOS can bid
    NO_GO = "NO-GO"                  # SOS cannot provide
    CONDITIONAL = "CONDITIONAL"      # Depends on other factors


class PartsConditionChecker:
    """
    Analyzes solicitation text to determine if refurbished/surplus parts are acceptable.
    """
    
    def __init__(self):
        """Initialize the condition checker with comprehensive patterns."""
        self.new_only_patterns = self._compile_new_only_patterns()
        self.refurb_prohibited_patterns = self._compile_refurb_prohibited_patterns()
        self.refurb_acceptable_patterns = self._compile_refurb_acceptable_patterns()
        self.surplus_acceptable_patterns = self._compile_surplus_acceptable_patterns()
        self.any_condition_patterns = self._compile_any_condition_patterns()
        self.override_patterns = self._compile_override_patterns()
        self.military_only_patterns = self._compile_military_only_patterns()
        self.negated_far_patterns = self._compile_negated_far_patterns()
    
    def _compile_new_only_patterns(self) -> List[re.Pattern]:
        """Compile patterns that indicate new parts only."""
        patterns = [
            # Explicit new only requirements
            r'\b(?:factory\s+)?new\s+(?:parts?\s+)?only\b',
            r'\bnew\s+manufacture(?:d)?\s+only\b',
            r'\bonly\s+new\s+(?:parts?|items?|components?)\b',
            r'\bmust\s+be\s+(?:factory\s+)?new\b',
            r'\b(?:all\s+)?parts?\s+must\s+be\s+new\b',
            r'\bfactory\s+new\s+condition\s+required\b',
            r'\bfactory\s+new\b',  # Match "factory new" anywhere
            r'\bnew\s+and\s+unused\s+only\b',
            r'\bbrand\s+new\s+(?:parts?\s+)?(?:only|required)\b',
            r'\bbrand\s+new\b',  # Match "brand new" anywhere
            r'\boriginal\s+equipment\s+new\b',
            r'\bOEM\s+new\s+(?:parts?\s+)?only\b',
            r'\bnew\s+production\s+only\b',
            r'\bcurrent\s+production\s+only\b',
            r'\blatest\s+production\s+(?:parts?\s+)?only\b',
            r'\bnew\s+from\s+manufacturer\b',
            r'\bdirect\s+from\s+(?:manufacturer|OEM)\b',
            r'\bfactory\s+direct\s+only\b',
            r'\bnew\s+(?:parts?\s+)?without\s+exception\b',
            r'\bstrictly\s+new\s+(?:parts?|items?)\b',
            r'\bnew\s+condition\s+mandatory\b',
            r'\bmint\s+condition\s+only\b',
        ]
        return [re.compile(p, re.IGNORECASE) for p in patterns]
    
    def _compile_refurb_prohibited_patterns(self) -> List[re.Pattern]:
        """Compile patterns that prohibit refurbished/rebuilt parts."""
        patterns = [
            # No refurbished
            r'\bno\s+refurbish(?:ed|ing)\b',
            r'\bno\s+rebuilt\b',
            r'\bno\s+reman(?:ufactured?)?\b',
            r'\bno\s+reconditioned\b',
            r'\bno\s+overhauled?\b',
            r'\bno\s+repaired?\b',
            r'\bno\s+used\s+(?:parts?|items?|components?)\b',
            r'\bno\s+surplus\b',
            r'\bno\s+secondary\s+market\b',
            r'\bno\s+aftermarket\b',
            r'\bno\s+recycled?\b',
            r'\bno\s+salvage(?:d)?\b',
            r'\bno\s+previously\s+used\b',
            r'\bno\s+second[\s\-]?hand\b',
            r'\bprohibit(?:ed|s)?\s+refurbish',
            r'\bprohibit(?:ed|s)?\s+surplus',
            r'\bexclud(?:e|es|ing)\s+refurbish',
            r'\bexclud(?:e|es|ing)\s+surplus',
            r'\bnot\s+accept\s+refurbish',
            r'\bnot\s+accept\s+surplus',
            r'\bwill\s+not\s+accept\s+(?:refurbish|surplus|used)',
            r'\brefurbish(?:ed)?\s+not\s+accept',
            r'\bsurplus\s+not\s+accept',
            # Rejection of non-new
            r'\breject\s+(?:all\s+)?(?:refurbish|surplus|used)',
            r'\b(?:refurbish|surplus|used)\s+will\s+be\s+rejected\b',
        ]
        return [re.compile(p, re.IGNORECASE) for p in patterns]
    
    def _compile_refurb_acceptable_patterns(self) -> List[re.Pattern]:
        """Compile patterns that indicate refurbished parts are acceptable."""
        patterns = [
            # Explicit acceptance
            r'\brefurbish(?:ed|ing)?\s+(?:is\s+)?accept(?:able|ed)?\b',
            r'\baccept(?:able|s|ing)?\s+refurbish',
            r'\brebuilt\s+(?:is\s+)?accept(?:able|ed)?\b',
            r'\baccept(?:able|s|ing)?\s+rebuilt\b',
            r'\breman(?:ufactured?)?\s+(?:is\s+)?accept',
            r'\baccept(?:able|s|ing)?\s+reman',
            r'\boverhaul(?:ed)?\s+(?:is\s+)?accept',
            r'\baccept(?:able|s|ing)?\s+overhaul',
            r'\brecondition(?:ed)?\s+(?:is\s+)?accept',
            r'\baccept(?:able|s|ing)?\s+recondition',
            # Options including refurbished
            r'\bnew\s+or\s+refurbish(?:ed)?\b',
            r'\bnew\s+or\s+rebuilt\b',
            r'\bnew\s+or\s+overhaul(?:ed)?\b',
            r'\bnew\s+or\s+reman(?:ufactured?)?\b',
            r'\bnew\s+or\s+recondition(?:ed)?\b',
            r'\bnew[\s,]+refurbish(?:ed)?[\s,]+(?:or\s+)?rebuilt\b',
            r'\bfactory\s+new\s+or\s+refurbish',
            # FAA certified refurbished
            r'\bFAA[\s\-]?(?:certified\s+)?refurbish',
            r'\bFAA[\s\-]?8130[\s\-]?3?\s+refurbish',
            r'\bairworthy\s+refurbish',
            r'\bcertified\s+refurbish',
            # May be refurbished
            r'\bmay\s+be\s+refurbish(?:ed)?\b',
            r'\bcan\s+be\s+refurbish(?:ed)?\b',
            r'\ballow(?:s|ed|ing)?\s+refurbish',
            r'\bpermit(?:s|ted|ting)?\s+refurbish',
            # Including refurbished
            r'\binclud(?:e|es|ing)\s+refurbish',
            r'\brefurbish(?:ed)?\s+includ(?:ed)?\b',
        ]
        return [re.compile(p, re.IGNORECASE) for p in patterns]
    
    def _compile_surplus_acceptable_patterns(self) -> List[re.Pattern]:
        """Compile patterns that indicate surplus parts are acceptable."""
        patterns = [
            # Explicit surplus acceptance
            r'\bsurplus\s+(?:is\s+)?accept(?:able|ed)?\b',
            r'\baccept(?:able|s|ing)?\s+surplus\b',
            r'\bexcess\s+(?:is\s+)?accept(?:able|ed)?\b',
            r'\baccept(?:able|s|ing)?\s+excess\b',
            r'\bgovernment\s+surplus\s+(?:is\s+)?(?:ok|okay|accept)',
            r'\bmilitary\s+surplus\s+(?:is\s+)?(?:ok|okay|accept)',
            # Options including surplus
            r'\bnew\s+or\s+surplus\b',
            r'\bnew[\s,]+surplus[\s,]+(?:or\s+)?refurbish',
            r'\bfactory\s+new\s+or\s+surplus',
            # May be surplus
            r'\bmay\s+be\s+surplus\b',
            r'\bcan\s+be\s+surplus\b',
            r'\ballow(?:s|ed|ing)?\s+surplus',
            r'\bpermit(?:s|ted|ting)?\s+surplus',
            # Including surplus
            r'\binclud(?:e|es|ing)\s+surplus',
            r'\bsurplus\s+includ(?:ed)?\b',
            r'\bsurplus\s+consider(?:ed)?\b',
            # Condition codes allowing surplus
            r'\bcondition\s+code\s+[A-C]\b',  # Usually allows surplus
            r'\bserviceable\s+condition\b',
            r'\bany\s+serviceable\s+condition\b',
        ]
        return [re.compile(p, re.IGNORECASE) for p in patterns]
    
    def _compile_any_condition_patterns(self) -> List[re.Pattern]:
        """Compile patterns that indicate any condition is acceptable."""
        patterns = [
            r'\bany\s+(?:condition|state)\b',
            r'\bcondition\s+not\s+specified\b',
            r'\bno\s+condition\s+requirement',
            r'\ball\s+conditions?\s+accept',
            r'\bregardless\s+of\s+condition\b',
            r'\bcondition\s+(?:is\s+)?irrelevant\b',
            r'\bas[\s\-]is\s+(?:condition\s+)?accept',
            r'\bused\s+(?:parts?\s+)?(?:is\s+)?accept(?:able|ed)?\b',
            r'\baccept(?:able|s|ing)?\s+used\b',
            r'\bpre[\s\-]?owned\s+(?:is\s+)?accept',
            r'\bsecond[\s\-]?hand\s+(?:is\s+)?accept',
        ]
        return [re.compile(p, re.IGNORECASE) for p in patterns]
    
    def _compile_override_patterns(self) -> List[re.Pattern]:
        """Compile patterns that override new-only requirements."""
        patterns = [
            # FAA certification overrides
            r'\bFAA[\s\-]?8130[\s\-]?3?\s+(?:certified|form|tag)',
            r'\bFAA[\s\-]?certified\b',
            r'\bairworth(?:y|iness)\s+certifi',
            r'\bEASA\s+Form\s+1\b',
            r'\bTC[\s\-]?STC\s+approved\b',
            # Commercial item designation - EXPANDED
            r'\bcommercial\s+item\b',
            r'\bcommercial\s+(?:parts?|components?|products?)\b',
            r'\bcommercially\s+available\b',
            r'\bFAR\s+Part\s+12\b',
            r'\bFAR\s+12\b',
            r'\bPart\s+12\s+(?:commercial|acquisition)\b',
            r'\bCOTS\b',  # Commercial Off-The-Shelf
            r'\bcommercial[\s\-]?off[\s\-]?the[\s\-]?shelf\b',
            r'\bcommercial\s+practices\b',
            r'\bcommercial\s+market\b',
            r'\bcommercial\s+supplier\b',
            r'\bcommercial\s+catalog\b',
            r'\bcommercial\s+price\s+list\b',
            # Special patterns for direct commercial language
            r'\bfactory\s+new\s+commercial\b',
            r'\bnew\s+commercial\b',
            r'\bnew\s+COTS\b',
            # Equal to new
            r'\bequal\s+to\s+new\b',
            r'\blike[\s\-]?new\s+condition\b',
            r'\bas[\s\-]?new\s+condition\b',
            r'\bequivalent\s+to\s+new\b',
            # DIBBS marketplace
            r'\bDIBBS\b',
            r'\bDefense\s+Logistics\s+Agency\b',
            r'\bDLA\s+disposition\b',
            # Surplus specific
            r'\bgovernment\s+furnished\b',
            r'\bGFE\b',  # Government Furnished Equipment
            r'\bGFP\b',  # Government Furnished Property
        ]
        return [re.compile(p, re.IGNORECASE) for p in patterns]
    
    def _compile_military_only_patterns(self) -> List[re.Pattern]:
        """Compile patterns that indicate military-only (no commercial override)."""
        patterns = [
            r'\bmilitary\s+specification\b',
            r'\bmil[\s\-]?spec\b',
            r'\bmil\-spec\b',
            r'\bmil[\s\-]?std\b',
            r'\bQPL\s+required\b',
            r'\bQML\s+required\b',
            r'\bqualified\s+products?\s+list\b',
            r'\bqualified\s+manufacturers?\s+list\b',
            r'\bmilitary\s+standard\b',
            r'\bdefense\s+standard\b',
            r'\bmilitary[\s\-]?only\b',
            r'\bno\s+commercial\s+equivalent\b',
            r'\bnon[\s\-]?commercial\b',
            r'\bmilitary\s+unique\b',
        ]
        return [re.compile(p, re.IGNORECASE) for p in patterns]
    
    def _compile_negated_far_patterns(self) -> List[re.Pattern]:
        """Compile patterns that indicate FAR Part 12 is NOT being used."""
        patterns = [
            # Direct negation of FAR Part 12
            r'\bnot\b.*\bFAR\s+(?:Part\s+)?12\b',
            r'\bdoes\s+not\b.*\bFAR\s+(?:Part\s+)?12\b',
            r'\bdo\s+not\b.*\bFAR\s+(?:Part\s+)?12\b',
            r'\bis\s+not\b.*\bFAR\s+(?:Part\s+)?12\b',
            r'\bare\s+not\b.*\bFAR\s+(?:Part\s+)?12\b',
            r'\bwill\s+not\b.*\bFAR\s+(?:Part\s+)?12\b',
            r'\bwithout\b.*\bFAR\s+(?:Part\s+)?12\b',
            r'\bNOT\s+using\b.*\bFAR\s+(?:Part\s+)?12\b',
            # Negation of commercial items
            r'\bnot\s+(?:a\s+)?commercial',
            r'\bnon[\s\-]?commercial',
            r'\bno\s+commercial',
            # Specific phrases from data
            r'\bnot\s+using\s+the\s+policies\s+contained\s+in\s+FAR',
            r'\bnot\s+intend\s+to\s+acquire\s+a\s+commercial',
            r'\bnot\s+conducted\s+under\s+FAR',
        ]
        return [re.compile(p, re.IGNORECASE | re.DOTALL) for p in patterns]
    
    def check_far_negation(self, text: str) -> bool:
        """
        Check if FAR Part 12 is mentioned in a negative context.
        Returns True if FAR Part 12 is negated (should NOT trigger override).
        """
        # Compile patterns if not already done
        if not hasattr(self, 'negated_far_patterns'):
            self.negated_far_patterns = self._compile_negated_far_patterns()
        
        # Check for any negation pattern
        for pattern in self.negated_far_patterns:
            if pattern.search(text):
                return True
        return False
    
    def check_parts_condition(self, text: str) -> Dict:
        """
        Analyze text to determine parts condition requirements.
        
        Returns:
            Dict with:
                - condition: PartsCondition enum
                - decision: ConditionDecision enum
                - evidence: List of matched patterns
                - has_override: Boolean
                - confidence: Float (0-1)
        """
        result = {
            'condition': PartsCondition.UNSPECIFIED,
            'decision': ConditionDecision.CONDITIONAL,
            'evidence': [],
            'has_override': False,
            'confidence': 0.0
        }
        
        # Check for override conditions first
        override_matches = []
        for pattern in self.override_patterns:
            matches = pattern.findall(text)
            if matches:
                override_matches.append(pattern.pattern)
                result['has_override'] = True
        
        # CRITICAL: Check if FAR Part 12 or commercial is negated
        if result['has_override']:
            if self.check_far_negation(text):
                # FAR Part 12 is negated - remove override
                result['has_override'] = False
                result['evidence'].append('FAR Part 12 negated - no commercial override')
        
        # Check for military-only patterns (blocks commercial override)
        military_only_matches = []
        for pattern in self.military_only_patterns:
            if pattern.search(text):
                military_only_matches.append(pattern.pattern)
        
        # Check for new-only requirements
        new_only_matches = []
        for pattern in self.new_only_patterns:
            if pattern.search(text):
                new_only_matches.append(pattern.pattern)
        
        # Check for refurbished prohibited
        refurb_prohibited_matches = []
        for pattern in self.refurb_prohibited_patterns:
            if pattern.search(text):
                refurb_prohibited_matches.append(pattern.pattern)
        
        # Check for refurbished acceptable
        refurb_acceptable_matches = []
        for pattern in self.refurb_acceptable_patterns:
            if pattern.search(text):
                refurb_acceptable_matches.append(pattern.pattern)
        
        # Check for surplus acceptable
        surplus_acceptable_matches = []
        for pattern in self.surplus_acceptable_patterns:
            if pattern.search(text):
                surplus_acceptable_matches.append(pattern.pattern)
        
        # Check for any condition acceptable
        any_condition_matches = []
        for pattern in self.any_condition_patterns:
            if pattern.search(text):
                any_condition_matches.append(pattern.pattern)
        
        # Determine condition and decision based on matches
        if any_condition_matches:
            result['condition'] = PartsCondition.ANY_CONDITION
            result['decision'] = ConditionDecision.GO
            result['evidence'] = any_condition_matches[:2]
            result['confidence'] = 0.95
        elif refurb_acceptable_matches or surplus_acceptable_matches:
            if refurb_acceptable_matches and surplus_acceptable_matches:
                result['condition'] = PartsCondition.ANY_CONDITION
            elif refurb_acceptable_matches:
                result['condition'] = PartsCondition.REFURB_OK
            else:
                result['condition'] = PartsCondition.SURPLUS_OK
            result['decision'] = ConditionDecision.GO
            result['evidence'] = (refurb_acceptable_matches + surplus_acceptable_matches)[:2]
            result['confidence'] = 0.9
        elif new_only_matches or refurb_prohibited_matches:
            result['condition'] = PartsCondition.NEW_ONLY
            # Check if override applies AND no military-only blocker
            if result['has_override'] and not military_only_matches:
                # Commercial override allows refurbished/surplus
                result['decision'] = ConditionDecision.GO
                result['evidence'] = ['Commercial override: ' + override_matches[0]]
                if new_only_matches:
                    result['evidence'].append('New requirement overridden')
                result['confidence'] = 0.85
            elif result['has_override'] and military_only_matches:
                # Military spec blocks commercial override
                result['decision'] = ConditionDecision.NO_GO
                result['evidence'] = ['Military spec blocks override: ' + military_only_matches[0]]
                if new_only_matches:
                    result['evidence'].extend(new_only_matches[:1])
                result['confidence'] = 0.95
            else:
                # No override available
                result['decision'] = ConditionDecision.NO_GO
                result['evidence'] = (new_only_matches + refurb_prohibited_matches)[:2]
                result['confidence'] = 0.95
        else:
            # No specific condition found
            result['condition'] = PartsCondition.UNSPECIFIED
            result['decision'] = ConditionDecision.CONDITIONAL
            result['confidence'] = 0.3
        
        return result
    
    def assess_for_sos(self, text: str) -> Tuple[ConditionDecision, str]:
        """
        Simplified assessment for SOS capabilities.
        
        Returns:
            Tuple of (decision, reason)
        """
        check_result = self.check_parts_condition(text)
        
        if check_result['decision'] == ConditionDecision.GO:
            if check_result['condition'] == PartsCondition.ANY_CONDITION:
                return (ConditionDecision.GO, "Any condition acceptable")
            elif check_result['condition'] == PartsCondition.REFURB_OK:
                return (ConditionDecision.GO, "Refurbished parts acceptable")
            elif check_result['condition'] == PartsCondition.SURPLUS_OK:
                return (ConditionDecision.GO, "Surplus parts acceptable")
            elif 'Commercial override' in str(check_result['evidence']):
                return (ConditionDecision.GO, "Commercial items - refurbished/surplus acceptable")
            else:
                return (ConditionDecision.GO, "Alternative conditions acceptable")
        
        elif check_result['decision'] == ConditionDecision.NO_GO:
            if 'Military spec blocks' in str(check_result['evidence']):
                return (ConditionDecision.NO_GO, "Military specification - no commercial equivalent")
            elif check_result['condition'] == PartsCondition.NEW_ONLY:
                return (ConditionDecision.NO_GO, "Factory new only - no commercial override")
            else:
                return (ConditionDecision.NO_GO, "Refurbished/surplus prohibited")
        
        else:  # CONDITIONAL
            if check_result['has_override']:
                return (ConditionDecision.CONDITIONAL, "New required but FAA/commercial override present")
            else:
                return (ConditionDecision.CONDITIONAL, "Parts condition unspecified - needs analysis")


def test_condition_checker():
    """Test the parts condition checker with various scenarios."""
    
    checker = PartsConditionChecker()
    
    test_cases = [
        # Military spec - Should be NO-GO even with commercial
        ("Factory new only military specification", ConditionDecision.NO_GO),
        ("Factory new mil-spec parts required", ConditionDecision.NO_GO),
        ("Factory new only, QPL required", ConditionDecision.NO_GO),
        ("New parts only, military standard", ConditionDecision.NO_GO),
        ("No refurbished, military unique", ConditionDecision.NO_GO),
        
        # Commercial override - Should be GO
        ("Factory new commercial items", ConditionDecision.GO),
        ("New COTS components required", ConditionDecision.GO),
        ("Factory new only. Commercial parts acceptable", ConditionDecision.GO),
        ("New parts only. FAR Part 12 acquisition", ConditionDecision.GO),
        ("Factory new commercially available parts", ConditionDecision.GO),
        
        # Standard NO-GO (no commercial)
        ("Factory new only parts required", ConditionDecision.NO_GO),
        ("All parts must be new manufacture only", ConditionDecision.NO_GO),
        ("No refurbished parts accepted", ConditionDecision.NO_GO),
        ("No rebuilt or overhauled components", ConditionDecision.NO_GO),
        ("No surplus parts will be accepted", ConditionDecision.NO_GO),
        
        # Should be GO (refurb/surplus acceptable)
        ("New or refurbished parts acceptable", ConditionDecision.GO),
        ("Refurbished acceptable with FAA 8130-3", ConditionDecision.GO),
        ("May be surplus or refurbished", ConditionDecision.GO),
        ("Surplus considered for this procurement", ConditionDecision.GO),
        ("Condition code A, B, or C acceptable", ConditionDecision.GO),
        ("Any serviceable condition", ConditionDecision.GO),
        ("Used parts acceptable", ConditionDecision.GO),
        
        # Should be CONDITIONAL
        ("Parts for Boeing 737", ConditionDecision.CONDITIONAL),  # Unspecified
        ("Aircraft maintenance services", ConditionDecision.CONDITIONAL),  # Unspecified
    ]
    
    print("Parts Condition Checker Test Results")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for text, expected in test_cases:
        decision, reason = checker.assess_for_sos(text)
        
        if decision == expected:
            passed += 1
            print(f"[PASS] {text[:50]}...")
            print(f"       Decision: {decision.value}, Reason: {reason}")
        else:
            failed += 1
            print(f"[FAIL] {text[:50]}...")
            print(f"       Expected: {expected.value}, Got: {decision.value}")
            print(f"       Reason: {reason}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{len(test_cases)} passed, {failed} failed")
    print(f"Success Rate: {(passed/len(test_cases))*100:.1f}%")
    
    return passed, failed


if __name__ == "__main__":
    passed, failed = test_condition_checker()
    
    if failed == 0:
        print("\nAll tests passed! Parts condition checker ready.")
        exit(0)
    else:
        print(f"\n{failed} tests failed. Review the logic.")
        exit(1)