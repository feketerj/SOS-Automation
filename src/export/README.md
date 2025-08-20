# Export Module

## Purpose
Generate and deliver assessment results in multiple formats including reports, API responses, and notifications.

## Components
- `report_generator.py`: Creates formatted reports
- `json_exporter.py`: Produces JSON output
- `csv_exporter.py`: Generates CSV summaries
- `pdf_renderer.py`: Creates PDF reports
- `api_responder.py`: Formats API responses
- `notification_sender.py`: Sends alerts and notifications

## Architecture Reference
See [/architecture.md](/architecture.md#3-export-module-srcexport) for detailed specifications.

## Export Formats
- JSON (structured data)
- CSV (tabular summaries)
- PDF (formatted reports)
- HTML (web display)
- XML (system integration)
- Plain text (simple output)

## Trace Points
- Records trace point: **Export Ready**