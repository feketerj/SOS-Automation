#!/usr/bin/env python3
"""
Model Configuration for SOS Assessment
Easy swap between holding agent and production model
"""

# Model IDs - Update these as models become available
MODELS = {
    # Holding/Test Agent
    "holding_agent": "ag:d42144c7:20250902:sos-triage-holding-agent:80b28a97",
    
    # Production Model (TRAINED ON 8,482 EXAMPLES)
    "production_model": "ag:d42144c7:20250902:sos-triage-agent:73e9cddd",
    
    # Fallback
    "dummy_model": "mistral-medium-latest"
}

# Current active model
ACTIVE_MODEL = "production_model"  # Using trained model

def get_model_id():
    """Get the currently active model ID"""
    model_id = MODELS.get(ACTIVE_MODEL)
    if not model_id:
        print(f"WARNING: {ACTIVE_MODEL} not configured, using dummy model")
        return MODELS["dummy_model"]
    return model_id

def get_model_info():
    """Get info about current model"""
    return {
        "active": ACTIVE_MODEL,
        "model_id": get_model_id(),
        "is_production": ACTIVE_MODEL == "production_model",
        "is_holding": ACTIVE_MODEL == "holding_agent"
    }

# Training status tracker
TRAINING_STATUS = {
    "completed": "2025-09-02",
    "model_id": "ag:d42144c7:20250902:sos-triage-agent:73e9cddd",
    "training_file": "SOS-Mistral-Train.jsonl",
    "validation_file": "SOS-Mistral-Val.jsonl",
    "examples": 8482,
    "epochs": 8,
    "tokens_processed": "~12M"
}

print(f"Current Model: {ACTIVE_MODEL}")
print(f"Model ID: {get_model_id()}")
print(f"Production Ready: {ACTIVE_MODEL == 'production_model'}")