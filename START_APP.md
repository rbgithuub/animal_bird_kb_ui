# Animal KB App - Agent Startup Runbook

## Project Metadata
- **Project Name:** Animal & Bird Knowledge Base UI
- **Root Path:** `/Users/balajiraja/holy999d/holy999d/animal_bird_kb_ui`
- **Working Branch:** `agent_animal_kb_app_local`
- **Platform:** macOS
- **Runtime:** Python (Flask)
- **Broker:** Redis (via Homebrew)
- **Task Queue:** Celery (Worker + Beat + Flower)
- **Entry Point:** `app.py`

---

## Pre-Flight Checks (Do These First)

Before executing any startup step, verify the following:

1. You are inside the correct project root:
   ```
   /Users/balajiraja/holy999d/holy999d/animal_bird_kb_ui
   ```
2. The active Git branch is `agent_animal_kb_app_local`. If not, switch to it:
   ```bash
   git checkout agent_animal_kb_app_local
   ```
3. Confirm `requirements.txt` exists in the root folder.
4. Confirm `celery_worker.py` exists in the root folder (used by all Celery commands).
5. Confirm `app.py` exists in the root folder.

---

## Startup Sequence

> ⚠️ **Important:** Execute steps in the exact order listed below. Do NOT skip or reorder.

---

### Step 1 — Install Python Dependencies

**Run from:** Project root  
**Terminal:** Current/main terminal session  
**Command:**
```bash
cd /Users/balajiraja/holy999d/holy999d/animal_bird_kb_ui
pip install -r requirements.txt
```
**Wait for:** `Successfully installed ...` or `Requirement already satisfied` messages for all packages.  
**On failure:** Check for missing system dependencies or Python version mismatch. Report the exact error.

---

### Step 2 — Start Redis Broker (macOS Homebrew)

**Run from:** Any terminal  
**Terminal:** Current/main terminal session  
**Command:**
```bash
brew services start redis
```
**Verify Redis is running:**
```bash
redis-cli ping
```
**Expected response:** `PONG`  
**On failure:** Try `brew services restart redis` or check `brew services list` for status.

---

### Step 3 — Start Celery Worker

**Run from:** Project root  
**Terminal:** Open a **new dedicated terminal session** for this process  
**Command:**
```bash
cd /Users/balajiraja/holy999d/holy999d/animal_bird_kb_ui
celery -A celery_worker worker --loglevel=info
```
**Wait for:** Log line containing `ready` or `celery@<hostname> ready`.  
**Keep this terminal open** — do not close it.  
**On failure:** Ensure Redis is running (Step 2) and `celery_worker.py` is present in root.

---

### Step 4 — Start Celery Beat (Scheduler)

**Run from:** Project root  
**Terminal:** Open a **new dedicated terminal session** for this process  
**Command:**
```bash
cd /Users/balajiraja/holy999d/holy999d/animal_bird_kb_ui
celery -A celery_worker beat --loglevel=info
```
**Wait for:** Log line containing `beat: Starting...`  
**Keep this terminal open** — do not close it.  
**On failure:** Check if a stale `celerybeat-schedule` file exists — delete it and retry:
```bash
rm -f celerybeat-schedule
```

---

### Step 5 — Start Celery Flower (Monitoring UI)

**Run from:** Project root  
**Terminal:** Open a **new dedicated terminal session** for this process  
**Command:**
```bash
cd /Users/balajiraja/holy999d/holy999d/animal_bird_kb_ui
celery -A celery_worker flower --loglevel=info
```
**Wait for:** Log line containing `Visit me at http://localhost:5555`  
**Keep this terminal open** — do not close it.  
**Flower UI:** [http://localhost:5555](http://localhost:5555)

---

### Step 6 — Start Flask Application

**Run from:** Project root  
**Terminal:** Open a **new dedicated terminal session** for this process (or use main terminal)  
**Command:**
```bash
cd /Users/balajiraja/holy999d/holy999d/animal_bird_kb_ui
python ./app.py
```
**Wait for:** Log line like `Running on http://127.0.0.1:5000` or similar Flask startup output.  
**Keep this terminal open** — do not close it.

---

## Health Check Summary

Once all steps are complete, verify the following endpoints/services are healthy:

| Service        | Check Command / URL                        | Expected Result            |
|----------------|--------------------------------------------|----------------------------|
| Redis          | `redis-cli ping`                           | `PONG`                     |
| Celery Worker  | Terminal logs                              | `ready` in output          |
| Celery Beat    | Terminal logs                              | `beat: Starting...`        |
| Celery Flower  | http://localhost:5555                      | Flower dashboard loads     |
| Flask App      | http://localhost:5000                      | App homepage loads         |

---

## Shutdown Sequence

To cleanly stop all services:

1. In each Celery terminal (Worker, Beat, Flower): press `Ctrl+C`
2. In Flask terminal: press `Ctrl+C`
3. Stop Redis:
   ```bash
   brew services stop redis
   ```

---

## Troubleshooting

| Symptom                              | Likely Cause                        | Fix                                              |
|--------------------------------------|-------------------------------------|--------------------------------------------------|
| `redis-cli ping` returns error       | Redis not started                   | Run `brew services start redis`                  |
| Celery worker can't connect          | Redis not running                   | Verify Step 2 completed successfully             |
| `ModuleNotFoundError` on Flask start | Missing dependency                  | Re-run Step 1 (`pip install -r requirements.txt`)|
| `celerybeat-schedule` lock error     | Stale schedule file                 | `rm -f celerybeat-schedule` then restart beat    |
| Flask port 5000 already in use       | Another process on port 5000        | `lsof -i :5000` then `kill -9 <PID>`            |
| Wrong Git branch                     | Checked out wrong branch            | `git checkout agent_animal_kb_app_local`         |

---

## Notes for Agent Execution

- All Celery processes (Step 3, 4, 5) **must run in separate terminal sessions** — they are long-running foreground processes.
- Always `cd` to the project root before running any command.
- Steps 3, 4, and 5 can be started in parallel (after Step 2 confirms Redis is up).
- Step 6 (Flask) must be the **last** process started.
- If any step fails, **stop and report the error** before proceeding to the next step.
