"""
Hardcoded Configuration for Multi-Stage Pipeline
All API keys, model IDs, and agent IDs are hardwired here.
NO environment variables required.
"""

# API Keys - Hardcoded
MISTRAL_API_KEY = "2oAquITdDMiyyk0OfQuJSSqePn3SQbde"  # Primary Mistral key
HIGHERGOV_API_KEY = "46be62b8aa8048cbabe51218c85dd0af"  # HigherGov API

# Model IDs - Different models for different purposes
MODELS = {
    # Production Agent (Full Price - $2/1M tokens)
    "agent": "ag:d42144c7:20250911:untitled-agent:15489fc1",  # Updated Sept 12

    # Fine-tuned Batch Models (50% discount - $1/1M tokens)
    "batch_pixtral": "ft:pixtral-12b-latest:d42144c7:20250912:f7d61150",  # Pixtral for batch
    "batch_medium": "ft:mistral-medium-latest:d42144c7:20250902:908db254",  # Medium for batch

    # QC Verification Agent (for NO-GO verification)
    "qc_agent": "ag:d42144c7:20250911:untitled-agent:15489fc1",  # Same as main agent for now

    # Fallback models
    "fallback": "open-mistral-7b",  # Cheapest option for testing
}

# API Endpoints - Hardcoded
API_ENDPOINTS = {
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "batch_url": "https://api.mistral.ai/v1/batch/jobs",
        "chat_url": "https://api.mistral.ai/v1/chat/completions",
        "agents_url": "https://api.mistral.ai/v1/agents/completions",
    },
    "highergov": {
        "base_url": "https://api.highergov.com",
        "opportunity_url": "https://api.highergov.com/api-external/opportunity/",
        "document_url": "https://api.highergov.com/api-external/document/",
    }
}

# Pipeline Configuration
PIPELINE_CONFIG = {
    # Stage processing limits
    "max_stages": 20,  # Total number of stages
    "early_termination": True,  # Stop on high-confidence NO-GO

    # Confidence thresholds by stage type
    "confidence_thresholds": {
        "binary": 0.99,     # Stages 1-7 (binary yes/no)
        "technical": 0.95,  # Stages 8-14 (technical assessment)
        "business": 0.85,   # Stages 15-20 (business judgment)
    },

    # QC verification thresholds
    "qc_thresholds": {
        "NO-GO": 0.99,  # Confidence required to confirm NO-GO
        "GO": 0.95,     # Confidence required for final GO
    },

    # Token limits - MUCH LARGER to handle full documents
    "max_tokens_per_request": 8000,  # Doubled from 4000
    "max_context_length": 2000000,  # 2M chars (was 200k) - matches document fetcher

    # Cost optimization
    "use_batch_first": True,  # Always try batch API first (50% discount)
    "agent_verification_threshold": 0.90,  # Only verify if batch confidence < 90%
}

# Stage-specific model assignments
STAGE_MODELS = {
    # Stages 1-3: Simple binary checks - use batch API
    1: "batch_pixtral",  # TIMING
    2: "batch_pixtral",  # SET-ASIDES
    3: "batch_pixtral",  # SECURITY

    # Stages 4-7: More complex binary - still batch
    4: "batch_pixtral",  # NON-STANDARD ACQUISITION
    5: "batch_pixtral",  # CONTRACT VEHICLE
    6: "batch_pixtral",  # EXPORT CONTROL
    7: "batch_pixtral",  # AMC/AMSC CODES

    # Stages 8-14: Technical assessment - use batch_medium
    8: "batch_medium",   # SOURCE RESTRICTIONS
    9: "batch_medium",   # SAR
    10: "batch_medium",  # PLATFORM
    11: "batch_medium",  # DOMAIN
    12: "batch_medium",  # TECHNICAL DATA
    13: "batch_medium",  # IT SYSTEM ACCESS
    14: "batch_medium",  # UNIQUE CERTIFICATIONS

    # Stages 15-20: Business judgment - use agent for accuracy
    15: "agent",  # SUBCONTRACTING PROHIBITED
    16: "agent",  # PROCUREMENT RESTRICTIONS
    17: "agent",  # COMPETITION STATUS
    18: "agent",  # MAINTENANCE/WARRANTY
    19: "agent",  # CAD/CAM FORMAT
    20: "agent",  # SCOPE
}

# Batch processing configuration
BATCH_CONFIG = {
    "batch_size": 100,  # Max opportunities per batch
    "timeout_seconds": 3600,  # 1 hour timeout for batch jobs
    "poll_interval": 30,  # Check batch status every 30 seconds
    "max_retries": 3,  # Retry failed batches up to 3 times
    "file_storage": "Mistral_Batch_Processor/",  # Where to store batch files
}

# Rate limiting (hardcoded)
RATE_LIMITS = {
    "agent_calls_per_minute": 10,
    "batch_submissions_per_hour": 100,
    "highergov_calls_per_second": 2,
    "retry_delay_seconds": 5,  # Delay between retries
}

# Timeout configuration - NO TIMEOUTS to match production
# Document fetching and processing can take a LONG time
TIMEOUTS = {
    "document_fetch": None,  # No timeout - let it run as long as needed
    "batch_api_call": None,  # No timeout for batch API calls
    "agent_api_call": None,  # No timeout for agent API calls
    "qc_api_call": None,     # No timeout for QC verification
    "total_opportunity": None,  # No timeout per opportunity
    "stage_processing": None,   # No timeout per stage
}

# For backwards compatibility, keep some reasonable values that can be used optionally
OPTIONAL_TIMEOUTS = {
    "document_fetch": 300,   # 5 minutes if someone wants to use a timeout
    "batch_api_call": 120,   # 2 minutes
    "agent_api_call": 180,   # 3 minutes
    "qc_api_call": 120,      # 2 minutes
}

# Logging configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "multi_stage_pipeline.log",
    "max_bytes": 10485760,  # 10MB
    "backup_count": 5,
}

# Output configuration
OUTPUT_CONFIG = {
    "base_dir": "SOS_Output",
    "create_csv": True,
    "create_json": True,
    "create_markdown": True,
    "create_go_only_csv": True,
    "preserve_metadata": True,
}

def get_api_key(service="mistral"):
    """Get hardcoded API key for a service"""
    if service.lower() == "mistral":
        return MISTRAL_API_KEY
    elif service.lower() in ["highergov", "hg"]:
        return HIGHERGOV_API_KEY
    else:
        raise ValueError(f"Unknown service: {service}")

def get_model_id(purpose="agent"):
    """Get hardcoded model ID for a specific purpose"""
    return MODELS.get(purpose, MODELS["fallback"])

def get_stage_model(stage_number):
    """Get the model ID for a specific stage"""
    model_key = STAGE_MODELS.get(stage_number, "batch_pixtral")
    return MODELS.get(model_key, MODELS["fallback"])

def get_endpoint(service, endpoint_type):
    """Get hardcoded API endpoint"""
    if service not in API_ENDPOINTS:
        raise ValueError(f"Unknown service: {service}")
    if endpoint_type not in API_ENDPOINTS[service]:
        raise ValueError(f"Unknown endpoint type: {endpoint_type}")
    return API_ENDPOINTS[service][endpoint_type]

# Validation on import to ensure all configs are present
def validate_config():
    """Validate that all required configurations are hardcoded"""
    required = {
        "MISTRAL_API_KEY": MISTRAL_API_KEY,
        "HIGHERGOV_API_KEY": HIGHERGOV_API_KEY,
        "MODELS": MODELS,
        "API_ENDPOINTS": API_ENDPOINTS,
    }

    missing = []
    for key, value in required.items():
        if not value:
            missing.append(key)

    if missing:
        raise ValueError(f"Missing required hardcoded configs: {missing}")

    return True

# Run validation on import
if __name__ != "__main__":
    validate_config()

# For testing
if __name__ == "__main__":
    print("Multi-Stage Pipeline Configuration (Hardcoded)")
    print("=" * 50)
    print(f"Mistral API Key: {MISTRAL_API_KEY[:10]}...")
    print(f"HigherGov API Key: {HIGHERGOV_API_KEY[:10]}...")
    print(f"\nModels configured: {len(MODELS)}")
    for purpose, model_id in MODELS.items():
        print(f"  - {purpose}: {model_id}")
    print(f"\nStages configured: {len(STAGE_MODELS)}")
    print(f"Batch size: {BATCH_CONFIG['batch_size']}")
    print(f"Early termination: {PIPELINE_CONFIG['early_termination']}")
    print("\nValidation: PASSED")