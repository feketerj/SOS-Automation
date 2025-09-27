#!/usr/bin/env python3
"""Direct test of pipeline with specific endpoint"""

import sys
import os

# Set environment variables to prevent interactive prompts
os.environ['MONITOR_BATCH'] = 'n'
os.environ['SKIP_AGENT_VERIFICATION'] = '1'

# Write the endpoint
endpoint = "AR1yyM0PV54_Ila0ZV6J6"
print(f"Testing with endpoint: {endpoint}")
print(f"Expected: 4 opportunities, all NO-GO (8(a) set-asides)")

# Write to endpoints.txt
with open("endpoints.txt", "w") as f:
    f.write(endpoint + "\n")

print("Wrote endpoint to endpoints.txt")

# Now run the batch processor directly
print("\nRunning batch processor...")
result = os.system("python Mistral_Batch_Processor\\FULL_BATCH_PROCESSOR.py")

if result == 0:
    print("\n✓ Pipeline ran successfully!")
    print("Check SOS_Output for results")
    print("Results should show 4 opportunities, all NO-GO with 8(a) set-aside reason")
else:
    print(f"\n✗ Pipeline failed with exit code: {result}")

print("\nDone!")