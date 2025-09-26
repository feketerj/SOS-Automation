# UI DASHBOARD - SESSION START INSTRUCTIONS

## CRITICAL: THIS IS A SEPARATE PROJECT

### Opening a New Session for UI Work

**1. Start fresh Claude session**

**2. Set working directory:**
```
C:\Users\feket\OneDrive\Desktop\excelsior\r_staff\r_3\Deployed_Code_Op_Locations\SOS-Assessment-Automation-Tool\SOS_UI_Dashboard
```

**3. Your opening prompt:**
```
I need to work on a UI dashboard project. 

Current directory: C:\Users\feket\OneDrive\Desktop\excelsior\r_staff\r_3\Deployed_Code_Op_Locations\SOS-Assessment-Automation-Tool\SOS_UI_Dashboard

Please read UI_CONTINUITY.md and PROJECT_PLAN.md to understand the project.

CRITICAL RULES:
1. This UI is completely separate from the parent directory's code
2. Never import anything from ../
3. Only communicate with parent system via subprocess or file I/O
4. Use dummy_assessment.csv in data/ folder for all testing
5. The UI should work even if the parent system doesn't exist

This is a standalone UI that happens to call an external script when needed.
```

## DO NOT IN UI SESSION

- Navigate to parent directory
- Import from parent modules
- Modify any files outside SOS_UI_Dashboard/
- Assume parent system behavior
- Mix engine code with UI code

## CAN DO IN UI SESSION

- Read CSVs from ../SOS_Output/ (read-only)
- Write to ../endpoints.txt (for input)
- Call ../BATCH_RUN.py via subprocess
- Create any files within SOS_UI_Dashboard/
- Build complete UI with dummy data

## File Structure You're Working With

```
SOS_UI_Dashboard/           <-- YOUR WORKING DIRECTORY
├── SESSION_START.md        (this file)
├── UI_CONTINUITY.md        (project principles)
├── PROJECT_PLAN.md         (development roadmap)
├── data/
│   ├── dummy_assessment.csv    (20 test records)
│   ├── sample_urls.txt         (test URLs)
│   └── sample_endpoints.txt    (test IDs)
├── components/             (your UI code goes here)
├── mockups/               (design docs)
└── assets/                (styles/images)

Parent Directory Structure (READ ONLY):
../                        <-- DO NOT MODIFY
├── BATCH_RUN.py          (can call via subprocess)
├── endpoints.txt         (can write for input)
└── SOS_Output/          (can read CSVs from here)
```

## Integration Points (The ONLY connections)

### Input: Write endpoints
```python
# Write search IDs for processing
with open('../endpoints.txt', 'w') as f:
    f.write('\n'.join(search_ids))
```

### Process: Call batch runner
```python
import subprocess
result = subprocess.run(
    ['python', '../BATCH_RUN.py'],
    capture_output=True,
    text=True,
    cwd='..'  # Run from parent directory
)
```

### Output: Read results
```python
import pandas as pd
import glob

# Find latest results
csv_files = glob.glob('../SOS_Output/2025-09/*/assessment.csv')
df = pd.read_csv(csv_files[-1])  # Read most recent
```

## Testing Strategy

**Phase 1: Pure UI Development**
- Use only dummy_assessment.csv
- No integration with parent
- Perfect the interface
- All features working with test data

**Phase 2: Integration Testing**
- Test subprocess calls
- Verify file paths
- Check error handling
- Ensure no imports from parent

**Phase 3: Production**
- Real endpoints
- Actual processing
- Live results
- Still no direct imports

## Tech Stack for UI

**Recommended: Streamlit**
```bash
pip install streamlit pandas plotly
streamlit run app.py
```

**Alternative: Flask**
```bash
pip install flask pandas
python app.py
# Opens at http://localhost:5000
```

## Remember

1. **This is an island** - The UI should work even if moved to another computer without the engine
2. **CSV is the contract** - The format in dummy_assessment.csv is what you'll get from the real system
3. **No coupling** - If you find yourself wanting to import from parent, stop and rethink
4. **Test with dummy first** - Get everything working with test data before integration

## Success Criteria

You know you've maintained separation if:
- UI runs without parent directory
- No imports from ../
- All visualizations work with dummy data
- Integration is just 3 functions (write file, call subprocess, read CSV)

## Next Session

When returning to UI work:
1. Open fresh Claude session
2. Use this SESSION_START.md as guide
3. Check if dummy CSV format still matches real outputs
4. Continue from where PROJECT_PLAN.md left off

---

**THE PRIME DIRECTIVE: Keep UI and Engine separate. They communicate through files, not imports.**