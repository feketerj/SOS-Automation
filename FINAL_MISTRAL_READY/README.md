# MISTRAL FINE-TUNING FILES - PRODUCTION READY

## PRIMARY FILES (USE THESE):
- **MISTRAL_TRAIN_8482_examples.jsonl** - Training set
- **MISTRAL_VAL_942_examples.jsonl** - Validation set
- **MISTRAL_FULL_9424_examples.jsonl** - Complete dataset

## FORMAT:
```json
{
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

## CONTENT:
- Real SOS contracts (KC-46, Navy, DLA, NASA)
- Contract numbers: FA860925FB031 ($39M), etc.
- Platforms: Boeing, Airbus, military derivatives
- GO/NO-GO/FURTHER decisions with confidence
- YAML v1.4 aligned

## USAGE:
```python
# Mistral API
from mistralai.client import MistralClient
client = MistralClient(api_key="your-key")

# Upload and fine-tune
job = client.jobs.create(
    model="open-mistral-7b",
    training_file="MISTRAL_TRAIN_8482_examples.jsonl",
    validation_file="MISTRAL_VAL_942_examples.jsonl"
)
```

Generated: 2025-09-02 17:03
