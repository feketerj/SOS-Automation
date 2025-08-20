# Ingestion Module

## Purpose
Entry point for all documents and data into the system. Handles file validation, sanitization, and session initialization.

## Components
- `file_monitor.py`: Watches designated folders for new files
- `validator.py`: Validates file formats and content structure
- `sanitizer.py`: Removes potentially harmful content
- `session_creator.py`: Initializes new processing sessions
- `metadata_extractor.py`: Extracts initial document metadata

## Architecture Reference
See [/architecture.md](/architecture.md#1-ingestion-module-srcingestion) for detailed specifications.

## Trust Requirements
- Minimum trust level: 25% for basic ingestion
- Enhanced features require 50%+
- Batch ingestion requires 75%+

## Trace Points
- Records trace point: **Creation**