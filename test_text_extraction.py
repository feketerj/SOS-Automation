#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test our text extraction function
from importlib import import_module
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Import the function from the main script
main_module = import_module('import os')
extract_critical_text_segments = main_module.extract_critical_text_segments

# Test with sample text
sample_text = """
This is a test solicitation for aircraft parts.

The contractor shall provide F-16 aircraft components with full traceability.

Source approval request (SAR) is required for all parts.

This is a sole source procurement to Boeing Company.

Commercial items are preferred under FAR Part 12.

Security clearance is mandatory for all personnel.

The part number is 12345-ABC-789 for the engine assembly.

Must meet all technical data package requirements.

Drawings and specifications will be provided separately.

End of solicitation document.
"""

print("Testing text extraction...")
print(f"Original text length: {len(sample_text)}")

# Test with different max lengths
for max_len in [500, 1000, 10000]:
    result = extract_critical_text_segments(sample_text, "F-16 Aircraft Parts", max_length=max_len)
    print(f"\nMax length {max_len}: Result length {len(result)}")
    if result:
        print("First 200 chars:", result[:200])
    else:
        print("NO RESULT!")
