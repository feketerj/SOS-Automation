#!/usr/bin/env python3
"""
PRODUCTION SETTINGS - LOCKED CONFIGURATION
Version: 1.4
Date: September 2, 2025
DO NOT MODIFY WITHOUT AUTHORIZATION
"""

# REGEX PACK VERSION - LOCKED
REGEX_PACK_FILE = 'packs/regex_pack_v14_production.yaml'
REGEX_VERSION = '1.4'

# OUTPUT CONFIGURATION - HARDWIRED
OUTPUT_FORMATS = ['JSON', 'CSV']  # Both REQUIRED
GENERATE_CSV = True  # HARDWIRED - Must always be True
GENERATE_GO_REPORTS = True
GENERATE_DAILY_SUMMARY = True
CSV_REQUIRED = True  # CSV generation is mandatory

# FOLDER STRUCTURE - STANDARD
REPORTS_BASE = 'Reports'
DATE_FORMAT = '%Y-%m-%d'
TIMESTAMP_FORMAT = '%Y%m%d_%H%M%S'

# SUBFOLDERS
ASSESSMENTS_FOLDER = 'HigherGov-Assessments'
GO_FOLDER = 'GO-Opportunities'
SUMMARY_FILE = 'DAILY_SUMMARY.md'

# CSV FIELDS - STANDARD ORDER
CSV_FIELDS = [
    'opportunity_id',
    'title', 
    'agency',
    'decision',
    'primary_blocker',
    'naics',
    'psc',
    'set_aside',
    'posted_date',
    'response_deadline',
    'url',
    'value_low',
    'value_high',
    'has_documents'
]

# PROCESSING SETTINGS
FETCH_DOCUMENTS = True
DOCUMENT_THRESHOLD = 500  # Characters to consider "has documents"
MAX_TIMEOUT = 120000  # 2 minutes per run

# API CONFIGURATION
HIGHERGOV_API_KEY = '9874995194174018881c567d92a2c4d2'
HIGHERGOV_BASE_URL = 'https://www.highergov.com/api/v2'

# ASSESSMENT ENGINE
GATE_VERSION = 'v419'
PATTERN_COUNT = 497

# DO NOT MODIFY BELOW THIS LINE
PRODUCTION_LOCKED = True
CONFIG_VERSION = '1.4-FINAL'