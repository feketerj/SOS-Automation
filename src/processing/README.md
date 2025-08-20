# Processing Module

## Purpose
Core assessment and evaluation engine that applies business rules, pattern matching, and scoring algorithms.

## Components
- `pipeline_orchestrator.py`: Manages processing workflow
- `pattern_matcher.py`: Applies regex and NLP patterns
- `rule_engine.py`: Evaluates business rules
- `score_calculator.py`: Computes opportunity scores
- `decision_tree.py`: Navigates assessment logic
- `ml_evaluator.py`: Machine learning model inference

## Architecture Reference
See [/architecture.md](/architecture.md#2-processing-module-srcprocessing) for detailed specifications.

## Processing Stages
1. Text extraction and normalization
2. Entity recognition
3. Contract clause identification
4. Compliance requirement extraction
5. Risk factor identification
6. Opportunity scoring
7. Recommendation formulation

## Trace Points
- Records trace points: **Data Attach**, **Processing**