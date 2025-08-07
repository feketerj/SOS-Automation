"""
Simple import module for the standardized SOS filter logic.
This file now imports the centralized InitialChecklistFilterV2 instead of maintaining an embedded copy.
"""

# Import the standardized filter logic
from filters.initial_checklist_v2 import InitialChecklistFilterV2, Decision, CheckResult

# Export the same interface for backward compatibility
__all__ = ['InitialChecklistFilterV2', 'Decision', 'CheckResult']

# For any code that might be importing this module directly, 
# provide the same classes
InitialChecklistFilterV2 = InitialChecklistFilterV2
Decision = Decision  
CheckResult = CheckResult
