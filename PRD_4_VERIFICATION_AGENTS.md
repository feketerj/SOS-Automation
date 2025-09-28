# PRODUCT REQUIREMENTS DOCUMENT
## Phase 4: Verification & Multi-Agent System

**Document Version:** 1.0
**Date:** September 27, 2025
**Author:** SOS Automation Team
**Status:** Draft
**Estimated Timeline:** 8-10 weeks
**Budget:** $95,000

---

## EXECUTIVE SUMMARY

This PRD outlines the implementation of a sophisticated multi-agent verification system that adds a fourth stage to our pipeline and introduces specialized agents for enhanced decision accuracy. This system will reduce false positives to under 5% while maintaining cost efficiency through intelligent agent orchestration.

### Vision
Transform the SOS Assessment Tool from a three-stage pipeline into an intelligent, multi-agent system that provides near-perfect accuracy on GO decisions through specialized verification and analysis agents working in concert.

### Strategic Goals
- **Accuracy:** Achieve >99% accuracy on GO decisions
- **Cost Efficiency:** Maintain <$0.15 per opportunity total cost
- **Specialization:** Deploy domain-specific agents for complex assessments
- **Confidence:** Provide high-confidence decisions for immediate action

---

## 1. VERIFICATION AGENT (Stage 4)

### 1.1 Problem Statement

**Current State:**
- 3-stage pipeline ends with single agent verification
- ~8-12% false positive rate on GO decisions
- No secondary validation for high-value opportunities
- Limited specialized analysis for complex cases

**Business Impact:**
- Wasted resources pursuing false positive GOs
- Missed opportunities due to conservative decisions
- Lack of confidence in automated assessments
- Manual review still required for critical decisions

### 1.2 Solution Architecture

#### 1.2.1 Pipeline Extension
```python
# Enhanced Pipeline Flow
Stage 1: Regex (FREE)
    ↓ (GO/INDETERMINATE)
Stage 2: Batch Model (50% off)
    ↓ (GO/INDETERMINATE)
Stage 3: Primary Agent (full price)
    ↓ (GO only)
Stage 4: Verification Agent (full price) ← NEW
    ↓
Final Decision with Confidence Score
```

#### 1.2.2 Verification Logic
```python
class VerificationAgent:
    """Stage 4 verification for GO decisions"""

    def __init__(self):
        self.model_id = "ag:d42144c7:20260101:verification-specialist:v1"
        self.verification_prompt = """
        You are a verification specialist. Your job is to:
        1. Challenge the GO decision from the primary agent
        2. Look for hidden disqualifiers
        3. Verify commercial viability
        4. Confirm no overlooked restrictions
        5. Provide confidence score (0-1)

        Be skeptical but fair. If you disagree, provide clear reasoning.
        """

    def verify_go_decision(self, opportunity, primary_decision):
        # Enhanced context for verification
        context = {
            'opportunity': opportunity,
            'primary_decision': primary_decision,
            'stage1_result': opportunity.get('stage1_regex'),
            'stage2_result': opportunity.get('stage2_batch'),
            'stage3_result': opportunity.get('stage3_agent'),
            'document_length': len(opportunity.get('document_text', '')),
            'red_flags': self.identify_red_flags(opportunity)
        }

        verification = self.call_verification_model(context)

        if verification['agrees']:
            return self.create_verified_go(opportunity, verification)
        else:
            return self.create_disputed_decision(opportunity, verification)

    def identify_red_flags(self, opportunity):
        """Identify potential issues for verification focus"""
        red_flags = []

        # Check for common false positive patterns
        if 'prototype' in opportunity.get('title', '').lower():
            red_flags.append('prototype_development')

        if 'study' in opportunity.get('title', '').lower():
            red_flags.append('study_contract')

        if opportunity.get('document_length', 0) < 500:
            red_flags.append('minimal_documentation')

        return red_flags
```

#### 1.2.3 Confidence Scoring System
```python
def calculate_final_confidence(pipeline_results):
    """
    Calculate final confidence based on all stages
    """
    base_confidence = 0.5

    # Agreement between stages increases confidence
    if all_stages_agree(pipeline_results):
        base_confidence += 0.3

    # Verification agreement is strongest signal
    if pipeline_results['stage4_verification']['agrees']:
        base_confidence += 0.2
    else:
        base_confidence -= 0.3

    # Document completeness
    doc_score = min(pipeline_results['document_length'] / 10000, 0.1)
    base_confidence += doc_score

    # Historical accuracy adjustment
    historical_adjustment = get_historical_accuracy_score(
        pipeline_results['agency'],
        pipeline_results['category']
    )
    base_confidence *= historical_adjustment

    return min(max(base_confidence, 0.0), 1.0)
```

### 1.3 Success Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| False Positive Rate | 8-12% | <5% | Verified GOs that fail |
| Verification Agreement | N/A | >85% | Stage 3 vs Stage 4 |
| High-Confidence GOs | Unknown | >70% | Confidence >0.8 |
| Processing Time | 30s | <45s | End-to-end |
| Cost per GO Verification | N/A | <$0.02 | API costs |

---

## 2. SPECIALIZED AGENT SYSTEM

### 2.1 Agent Roster

#### 2.1.1 Compliance Agent
**Purpose:** Verify regulatory and compliance requirements

```python
class ComplianceAgent:
    """Specialized agent for compliance verification"""

    specializations = [
        'export_controls',
        'security_clearances',
        'regulatory_requirements',
        'certification_standards',
        'contract_clauses'
    ]

    def assess_compliance(self, opportunity):
        compliance_check = {
            'export_control': self.check_itar_ear(opportunity),
            'clearance_required': self.check_clearance_requirements(opportunity),
            'certifications': self.check_required_certs(opportunity),
            'regulatory': self.check_regulatory_compliance(opportunity),
            'contract_terms': self.analyze_contract_clauses(opportunity)
        }

        return {
            'compliant': all(compliance_check.values()),
            'issues': [k for k, v in compliance_check.items() if not v],
            'recommendations': self.generate_compliance_recommendations(compliance_check)
        }
```

**Trigger Conditions:**
- Government contracts
- International opportunities
- Aerospace/Defense sector
- Regulated industries
- High-value contracts (>$1M)

#### 2.1.2 Risk Assessment Agent
**Purpose:** Evaluate operational and financial risks

```python
class RiskAssessmentAgent:
    """Specialized agent for risk evaluation"""

    risk_categories = {
        'technical': ['complexity', 'technology_readiness', 'integration_risk'],
        'financial': ['payment_terms', 'bonding', 'liability'],
        'operational': ['timeline', 'resources', 'location'],
        'competitive': ['incumbents', 'competition_level', 'price_sensitivity'],
        'contractual': ['terms_conditions', 'penalties', 'warranties']
    }

    def evaluate_risks(self, opportunity):
        risk_profile = {}

        for category, factors in self.risk_categories.items():
            category_score = 0
            category_details = []

            for factor in factors:
                score, details = self.assess_factor(opportunity, factor)
                category_score += score
                category_details.append({
                    'factor': factor,
                    'score': score,
                    'details': details
                })

            risk_profile[category] = {
                'score': category_score / len(factors),
                'level': self.score_to_level(category_score / len(factors)),
                'factors': category_details
            }

        return {
            'overall_risk': self.calculate_overall_risk(risk_profile),
            'risk_profile': risk_profile,
            'mitigation_strategies': self.suggest_mitigations(risk_profile),
            'go_nogo_impact': self.assess_decision_impact(risk_profile)
        }
```

**Output Schema:**
```json
{
    "overall_risk": "MEDIUM",
    "risk_score": 0.65,
    "high_risk_factors": [
        "tight_timeline",
        "bonding_requirement"
    ],
    "mitigation_required": true,
    "recommended_actions": [
        "Partner with established contractor",
        "Secure bond early"
    ]
}
```

#### 2.1.3 Pricing Intelligence Agent
**Purpose:** Estimate opportunity value and pricing strategy

```python
class PricingAgent:
    """Specialized agent for pricing and value analysis"""

    def analyze_opportunity_value(self, opportunity):
        # Historical data analysis
        similar_contracts = self.find_similar_historical(opportunity)

        # Price estimation
        estimated_value = self.estimate_contract_value(
            opportunity,
            similar_contracts
        )

        # Competition analysis
        competitive_landscape = self.analyze_competition(opportunity)

        # Margin analysis
        expected_margin = self.calculate_expected_margin(
            estimated_value,
            competitive_landscape
        )

        return {
            'estimated_value': estimated_value,
            'value_confidence': self.calculate_value_confidence(similar_contracts),
            'competitive_position': competitive_landscape,
            'expected_margin': expected_margin,
            'pricing_strategy': self.recommend_pricing_strategy(
                estimated_value,
                competitive_landscape,
                expected_margin
            ),
            'historical_comparisons': similar_contracts[:5]
        }
```

**Pricing Factors:**
- Historical similar contracts
- Market rates
- Competition level
- Urgency indicators
- Budget indicators
- Complexity factors

#### 2.1.4 Executive Summary Agent
**Purpose:** Generate concise executive-level summaries

```python
class SummaryAgent:
    """Specialized agent for executive summaries"""

    def generate_executive_summary(self, full_assessment):
        summary = {
            'headline': self.create_headline(full_assessment),
            'decision': full_assessment['final_decision'],
            'confidence': full_assessment['confidence_score'],
            'key_points': self.extract_key_points(full_assessment),
            'value_proposition': self.summarize_value(full_assessment),
            'risks': self.summarize_risks(full_assessment),
            'recommended_action': self.recommend_action(full_assessment),
            'next_steps': self.define_next_steps(full_assessment)
        }

        # Format for executive consumption
        return self.format_executive_summary(summary)

    def format_executive_summary(self, summary):
        return f"""
        **{summary['headline']}**

        Decision: {summary['decision']} (Confidence: {summary['confidence']:.0%})

        Value: {summary['value_proposition']}

        Key Points:
        {self.format_bullets(summary['key_points'])}

        Primary Risks: {summary['risks']}

        Recommendation: {summary['recommended_action']}

        Next Steps:
        {self.format_bullets(summary['next_steps'])}
        """
```

### 2.2 Agent Orchestration

#### 2.2.1 Orchestration Engine
```python
class AgentOrchestrator:
    """Manages multi-agent workflow and decisions"""

    def __init__(self):
        self.agents = {
            'verification': VerificationAgent(),
            'compliance': ComplianceAgent(),
            'risk': RiskAssessmentAgent(),
            'pricing': PricingAgent(),
            'summary': SummaryAgent()
        }

        self.routing_rules = {
            'GO': ['verification', 'pricing', 'risk', 'summary'],
            'NO-GO': ['summary'],
            'INDETERMINATE': ['compliance', 'risk', 'summary'],
            'HIGH_VALUE': ['verification', 'compliance', 'risk', 'pricing', 'summary']
        }

    def orchestrate_assessment(self, opportunity, stage3_result):
        # Determine which agents to invoke
        agents_to_run = self.determine_agents(opportunity, stage3_result)

        # Run agents in parallel where possible
        agent_results = self.run_agents_parallel(agents_to_run, opportunity)

        # Resolve any conflicts
        final_decision = self.resolve_conflicts(agent_results)

        # Generate unified assessment
        return self.create_unified_assessment(
            opportunity,
            agent_results,
            final_decision
        )

    def determine_agents(self, opportunity, stage3_result):
        agents = []

        # Base routing
        decision = stage3_result.get('decision')
        agents.extend(self.routing_rules.get(decision, []))

        # Conditional routing
        if opportunity.get('estimated_value', 0) > 1000000:
            agents.extend(self.routing_rules['HIGH_VALUE'])

        if opportunity.get('agency') in HIGH_RISK_AGENCIES:
            agents.append('compliance')
            agents.append('risk')

        # Remove duplicates, maintain order
        return list(dict.fromkeys(agents))

    def resolve_conflicts(self, agent_results):
        """Resolve disagreements between agents"""

        decisions = [r.get('decision') for r in agent_results.values()]

        # If verification disagrees, it wins
        if 'verification' in agent_results:
            if agent_results['verification']['decision'] == 'NO-GO':
                return 'NO-GO'

        # If compliance fails, automatic NO-GO
        if 'compliance' in agent_results:
            if not agent_results['compliance']['compliant']:
                return 'NO-GO'

        # High risk with low confidence = REVIEW
        if 'risk' in agent_results:
            if agent_results['risk']['overall_risk'] == 'HIGH':
                if self.calculate_aggregate_confidence(agent_results) < 0.7:
                    return 'NEEDS_REVIEW'

        # Otherwise, majority rules
        return self.majority_decision(decisions)
```

#### 2.2.2 Parallel Processing
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ParallelAgentProcessor:
    """Process multiple agents in parallel for efficiency"""

    def __init__(self, max_workers=5):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def process_agents_async(self, agents, opportunity):
        tasks = []

        for agent_name, agent in agents.items():
            task = asyncio.create_task(
                self.run_agent_async(agent_name, agent, opportunity)
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return self.compile_results(agents.keys(), results)

    async def run_agent_async(self, agent_name, agent, opportunity):
        """Run single agent asynchronously"""
        try:
            start_time = time.time()

            result = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                agent.process,
                opportunity
            )

            result['processing_time'] = time.time() - start_time
            result['agent_name'] = agent_name

            return result

        except Exception as e:
            return {
                'agent_name': agent_name,
                'error': str(e),
                'decision': 'ERROR'
            }
```

### 2.3 Decision Aggregation

#### 2.3.1 Confidence Aggregation
```python
def aggregate_confidence(agent_results):
    """
    Combine confidence scores from multiple agents
    using weighted average based on agent expertise
    """

    agent_weights = {
        'verification': 0.35,
        'compliance': 0.20,
        'risk': 0.20,
        'pricing': 0.15,
        'summary': 0.10
    }

    weighted_sum = 0
    weight_total = 0

    for agent_name, result in agent_results.items():
        if 'confidence' in result:
            weight = agent_weights.get(agent_name, 0.1)
            weighted_sum += result['confidence'] * weight
            weight_total += weight

    if weight_total > 0:
        aggregate_confidence = weighted_sum / weight_total
    else:
        aggregate_confidence = 0.5

    # Adjust for disagreement
    disagreement_penalty = calculate_disagreement_penalty(agent_results)
    aggregate_confidence *= (1 - disagreement_penalty)

    return min(max(aggregate_confidence, 0.0), 1.0)
```

#### 2.3.2 Decision Matrix
```python
DECISION_MATRIX = {
    # (verification, compliance, risk) -> final_decision
    ('GO', 'PASS', 'LOW'): 'GO',
    ('GO', 'PASS', 'MEDIUM'): 'GO',
    ('GO', 'PASS', 'HIGH'): 'REVIEW',
    ('GO', 'FAIL', 'LOW'): 'NO-GO',
    ('GO', 'FAIL', 'MEDIUM'): 'NO-GO',
    ('GO', 'FAIL', 'HIGH'): 'NO-GO',
    ('NO-GO', 'PASS', 'LOW'): 'NO-GO',
    ('NO-GO', 'PASS', 'MEDIUM'): 'NO-GO',
    ('NO-GO', 'PASS', 'HIGH'): 'NO-GO',
    ('NO-GO', 'FAIL', 'LOW'): 'NO-GO',
    ('NO-GO', 'FAIL', 'MEDIUM'): 'NO-GO',
    ('NO-GO', 'FAIL', 'HIGH'): 'NO-GO',
    ('REVIEW', 'PASS', 'LOW'): 'REVIEW',
    ('REVIEW', 'PASS', 'MEDIUM'): 'REVIEW',
    ('REVIEW', 'PASS', 'HIGH'): 'NO-GO',
    ('REVIEW', 'FAIL', 'LOW'): 'NO-GO',
    ('REVIEW', 'FAIL', 'MEDIUM'): 'NO-GO',
    ('REVIEW', 'FAIL', 'HIGH'): 'NO-GO'
}

def apply_decision_matrix(agent_results):
    key = (
        agent_results.get('verification', {}).get('decision', 'REVIEW'),
        'PASS' if agent_results.get('compliance', {}).get('compliant', True) else 'FAIL',
        agent_results.get('risk', {}).get('overall_risk', 'MEDIUM')
    )
    return DECISION_MATRIX.get(key, 'REVIEW')
```

---

## 3. IMPLEMENTATION PLAN

### 3.1 Development Phases

#### Phase 1: Verification Agent (Weeks 1-3)
- [ ] Develop verification model prompts
- [ ] Implement Stage 4 pipeline integration
- [ ] Create confidence scoring system
- [ ] Build disagreement resolution logic
- [ ] Test with 1000+ historical assessments

#### Phase 2: Specialized Agents (Weeks 4-6)
- [ ] Develop Compliance Agent
- [ ] Develop Risk Assessment Agent
- [ ] Develop Pricing Agent
- [ ] Develop Summary Agent
- [ ] Create agent-specific prompts and logic

#### Phase 3: Orchestration (Weeks 7-8)
- [ ] Build orchestration engine
- [ ] Implement parallel processing
- [ ] Create routing rules
- [ ] Develop conflict resolution
- [ ] Build decision aggregation

#### Phase 4: Testing & Optimization (Weeks 9-10)
- [ ] Integration testing
- [ ] Performance optimization
- [ ] Cost optimization
- [ ] User acceptance testing
- [ ] Production deployment

### 3.2 Technical Architecture

```yaml
Architecture:
  API Gateway:
    - Rate limiting
    - Request routing
    - Response caching

  Orchestration Layer:
    - Agent routing
    - Parallel execution
    - Result aggregation
    - Conflict resolution

  Agent Services:
    - Verification Agent API
    - Compliance Agent API
    - Risk Agent API
    - Pricing Agent API
    - Summary Agent API

  Data Layer:
    - Agent results store
    - Confidence metrics
    - Historical accuracy
    - Performance logs

  Monitoring:
    - Agent performance
    - Cost tracking
    - Accuracy metrics
    - Disagreement rates
```

### 3.3 Cost Model

#### Per-Opportunity Costs
```
Current 3-Stage:
- Regex: $0.00
- Batch: $0.02
- Agent: $0.05
- Total: $0.07

With Multi-Agent (Average):
- Regex: $0.00
- Batch: $0.02
- Primary Agent: $0.05
- Verification: $0.04
- Specialized Agents (2 avg): $0.06
- Total: $0.17

High-Value Opportunities:
- All agents invoked: $0.25
- Justified by opportunity value
```

#### Monthly Projections
```
Assumptions:
- 2000 opportunities/month
- 60% stopped at regex
- 30% need verification
- 10% need full agent suite

Monthly Costs:
- Basic pipeline: $140
- Verification: $240
- Specialized agents: $120
- Total: $500/month

ROI:
- One prevented false positive: $5,000+ saved
- One found opportunity: $50,000+ value
- Break-even: <1 success per month
```

---

## 4. SUCCESS METRICS

### 4.1 Key Performance Indicators

| KPI | Baseline | Target | Measurement |
|-----|----------|--------|-------------|
| GO Accuracy | 88% | >99% | Validated GOs that succeed |
| False Positive Rate | 12% | <5% | Failed GO pursuits |
| Processing Time | 30s | <60s | End-to-end average |
| Cost per Assessment | $0.07 | <$0.15 | Average all opportunities |
| Agent Agreement | N/A | >80% | Inter-agent agreement rate |
| Confidence Score Accuracy | N/A | >90% | Confidence vs actual outcome |
| High-Value Identification | Unknown | >95% | >$1M opportunities caught |

### 4.2 Quality Metrics

#### Agent Performance
```python
agent_metrics = {
    'verification': {
        'accuracy': 0.95,  # Target
        'false_negative_rate': 0.02,
        'processing_time': 15,  # seconds
        'cost_per_call': 0.04
    },
    'compliance': {
        'accuracy': 0.98,
        'coverage': 0.95,  # % of regulations checked
        'processing_time': 10,
        'cost_per_call': 0.03
    },
    'risk': {
        'risk_identification': 0.90,
        'mitigation_quality': 0.85,
        'processing_time': 12,
        'cost_per_call': 0.03
    }
}
```

---

## 5. RISKS AND MITIGATION

### 5.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Agent response latency | High | Medium | Implement caching, parallel processing |
| Model disagreement cascades | High | Low | Clear precedence rules, human escalation |
| Cost overrun | Medium | Medium | Dynamic agent invocation, cost caps |
| Integration complexity | High | Medium | Phased rollout, extensive testing |
| False negative increase | High | Low | Conservative verification, A/B testing |

### 5.2 Business Risks

- **Over-reliance on automation**: Maintain human review capability
- **Regulatory compliance**: Regular audit of compliance agent
- **Cost justification**: Track ROI meticulously
- **User trust**: Transparent confidence scoring

---

## 6. TESTING STRATEGY

### 6.1 Test Scenarios

#### Verification Agent Testing
```python
test_scenarios = [
    {
        'name': 'High-confidence GO validation',
        'input': 'Clear commercial opportunity',
        'expected': 'Verification agrees',
        'confidence': '>0.9'
    },
    {
        'name': 'Hidden restriction detection',
        'input': 'GO with buried clearance requirement',
        'expected': 'Verification disagrees',
        'confidence': '<0.5'
    },
    {
        'name': 'Edge case handling',
        'input': 'Ambiguous military/commercial',
        'expected': 'Requests review',
        'confidence': '0.4-0.6'
    }
]
```

#### Multi-Agent Testing
```python
multi_agent_tests = [
    {
        'scenario': 'All agents agree GO',
        'expected_confidence': '>0.95',
        'expected_decision': 'GO'
    },
    {
        'scenario': 'Compliance fails, others GO',
        'expected_confidence': '<0.3',
        'expected_decision': 'NO-GO'
    },
    {
        'scenario': 'Split decision',
        'expected_confidence': '0.4-0.6',
        'expected_decision': 'REVIEW'
    }
]
```

### 6.2 Performance Testing

- **Load Testing**: 100 concurrent assessments
- **Stress Testing**: 1000 assessments in 1 hour
- **Endurance Testing**: 24-hour continuous operation
- **Spike Testing**: Sudden 10x volume increase

---

## 7. ROLLOUT PLAN

### 7.1 Phased Deployment

#### Phase 1: Shadow Mode (Week 1-2)
- Run verification in parallel without affecting decisions
- Collect accuracy data
- Tune confidence thresholds

#### Phase 2: Limited Production (Week 3-4)
- Enable for 10% of GO decisions
- Monitor false positive rate
- Gather user feedback

#### Phase 3: Full Verification (Week 5-6)
- Enable verification for all GOs
- Monitor performance impact
- Optimize processing

#### Phase 4: Specialized Agents (Week 7-8)
- Deploy one specialized agent at a time
- Compliance → Risk → Pricing → Summary
- Monitor cost impact

#### Phase 5: Full Production (Week 9-10)
- All agents operational
- Dynamic routing enabled
- Cost optimization active

### 7.2 Rollback Criteria

Automatic rollback if:
- False negative rate increases >2%
- Processing time exceeds 90 seconds
- Costs exceed $0.25 per assessment
- System errors >1%
- User satisfaction drops >10%

---

## 8. APPENDICES

### Appendix A: Agent Prompt Templates
[Detailed prompts for each agent]

### Appendix B: Cost Analysis Spreadsheet
[Detailed cost breakdown and projections]

### Appendix C: Integration Specifications
[API specifications and data schemas]

### Appendix D: Training Data Requirements
[Data needed for agent training]

---

## APPROVAL

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | | | |
| Technical Lead | | | |
| Finance | | | |
| Operations | | | |

**Review Period:** September 27 - October 10, 2025
**Implementation Start:** October 15, 2025
**Target Completion:** December 20, 2025