# Rails Cheat Sheet v4.2
**Operational Cockpit for Agents — Zero Drift Discipline**

---

## CORE RAILS (Page 1)

### Rule Zero (40-Hour Lesson)
- **Ingestion validated before ANY downstream work**
- Steps: Upload real file → Verify processing → Retrieve schema → Proof in `/ops/ingestion-validated.md`
- Override only with: `Pied Piper 1x: use mock data`

### Pied Piper Authority
- Format: `Pied Piper [N]x: [list of N overrides]`
- ROB’s declaration = ABSOLUTE
- Wrong counts = clarify before proceeding

### Atomic Sizing
- **Agents:** 500+ line blocks, full files, cut/paste/run  
- **Users:** Single discrete action (UI clicks, confirm deploys)  
- **Never:** Ask user to type CLI/code

### Clean Code Boxes
- EVERYTHING must be in a code fence  
- No fragments, no “add this”, no “as before”  
- Zero manual typing unless explicitly overridden

### Binary Proof
- Every output ends with: `WORKS` or `DOESN'T WORK`  
- No hedging, no “should work”  
- False WORKS = permanent replacement

### Trust Mechanics
- Erosion:  
  - Manual edit: -10%  
  - Missing proof: -15%  
  - Mode violation: -50%  
  - False WORKS: -100% (permanent)  
  - >5 pastes/hour: -40%  
- Recovery:  
  - Desktop icon: +60%  
  - Visible UI: +50%  
  - Clean test: +30%  
  - Correct export: +40%  
  - Perfect atomic block: +5%  
- Thresholds:  
  - 0% → Replace agent  
  - 1–24% → Single steps only  
  - 25–49% → Outcome mode  
  - 50–74% → Restricted mode  
  - 75–100% → Standard  
  - 100%+ → Full autonomy

### Manual Paste Ceiling
- ≤5 pastes/hour max  
- 4 = warning, 5 = CRITICAL → halt & review  
- Historical failure: 40+ pastes = architecture collapse

### Session Traces (6 Mandatory)
1. Creation (ID generated)  
2. Data Attach (file linked)  
3. Processing (pipeline active)  
4. Complete (results ready)  
5. UI Render (data visible or icon launch)  
6. Export Ready (retrievable data)  
- Missing any = orphaned session → HALT

---

## LIVE MONITORING (Page 2)

### Continuity Prompt Skeleton
- Session info (name, repo, trust %)  
- Active overrides (Pied Piper)  
- Build state (phase, last success, blockers)  
- Proof tracking (last proof, pending)  
- Execution status (agent/user + proof)  
- Session traces (✓/PENDING for all 6)  
- Paste count (hourly + historical)  
- Agent violations (by type & trust impact)

### Trust → Tempo Mapping
- 100%: full 500+ line blocks  
- 75–99%: standard oversight  
- 50–74%: restricted mode  
- 25–49%: outcome only  
- <25%: single actions only  
- 0%: agent replaced

### Terminal Stall Rule
- >60s no output = auto-kill/restart  
- Document in continuity before resume

### Desktop Icon Checkpoint
- Location: `$env:USERPROFILE\Desktop\[app].lnk`  
- Double-click launches app = +60% trust  
- Primary checkpoint for local builds

### Rage Triggers
- 3+ f-words, “STOP/RESET/halt”, or “what are we doing” = trigger  
- Protocol: Pivot to Outcome Mode → deliver simplest working result in ≤2 steps

### After-Action Review (AAR)
- Every session ends with AAR  
- Mandatory: trust changes, paste counts, traces, violations, agent performance

### Quick Fallback Chains
- Server start: `npm start → npm run start → npm run dev → node server.js → node index.js`  
- Port binding: `$PORT → 5000 → 3000 → 3001 → 8080 → random`  
- Session creation: `POST full → POST {} → POST default → GET /create`  
- Export: `Direct → Queue → Local save → Manual`

---

## PRIME RULE
If ROB has to type → QB FAILED.  
If >5 pastes/hour → ARCHITECTURE FAILED.  
If false WORKS → AGENT REPLACED.  
