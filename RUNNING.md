# Running Provenance Guard

Provenance Guard is a local Python/Flask service that analyzes submitted writing using a GPT-2 language-model signal and a writing-style signal. It returns a cautious estimate (`human`, `ai`, or `unsure`), supports appeals, and records structured logs.

**Unit 10 Demo Day:** Start with the quick start below. [README.md](README.md) contains the project explanation, original criteria, real before/after results, and limitations. You do not need to rerun the Unit 9 tests for the demo.

## Demo Day quick start (Windows PowerShell)

**Already have this repository and its `.venv`?** Open PowerShell in the project folder. If you have not updated your working copy, run `git pull` before starting.

**Terminal 1: start the service**

~~~powershell
.\.venv\Scripts\Activate.ps1
$env:AI201_DEBUG = "0"
python app.py
~~~

Leave this terminal running. The service should listen at `http://127.0.0.1:5000`. The first classification may take longer because the model loads into memory.

**Terminal 2: check health and submit writing**

~~~powershell
Invoke-RestMethod http://127.0.0.1:5000/health

$body = @{
    creator_id = "demo_student"
    text = "This is a demonstration of Provenance Guard. The service evaluates the writing, combines two signals, and records a classification that can be reviewed later."
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "http://127.0.0.1:5000/submit" -Method Post -ContentType "application/json" -Body $body
$result | Format-List
~~~

The response includes `content_id`, `guess`, `confidence`, `label`, `model_score`, `style_score`, and `status`. Those scores are estimates, not proof of authorship. Keep `$result` available for the appeal example below.

**Show that the request was recorded**

~~~powershell
Invoke-RestMethod "http://127.0.0.1:5000/log?limit=5" | ConvertTo-Json -Depth 7
Get-Content .\logs\requests.jsonl -Tail 3
~~~

The `/log` route reads the audit history. `logs/requests.jsonl` contains request-level telemetry, including HTTP status, duration, and a limited input summary. Both logs rotate at 1 MiB per file, preserve numbered archives, and remain available through archive-aware readers.

**Optional: demonstrate a failed request and an appeal**

~~~powershell
$badBody = @{ creator_id = "demo_invalid"; text = "" } | ConvertTo-Json
try {
    Invoke-RestMethod -Uri "http://127.0.0.1:5000/submit" -Method Post -ContentType "application/json" -Body $badBody
} catch {
    $_.ErrorDetails.Message
}

$appeal = @{
    content_id = $result.content_id
    reasoning = "I would like a human to review this result."
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/appeal" -Method Post -ContentType "application/json" -Body $appeal
~~~

The empty input should be rejected with HTTP 400 and logged. The appeal should return `under_review` and appear in the audit log. You can stop the service with Ctrl+C in Terminal 1.

## Setup on a different computer

**Requirements:** Python 3.11, 3.12, or 3.13; enough free memory and disk for PyTorch and the local GPT-2 model; and internet access for the initial package/model download. `requirements.txt` provides the dependency constraints, and `requirements-lock.txt` records the packages installed during the measured capstone run. No API key or paid AI service is needed.

**Windows PowerShell, new checkout**

~~~powershell
git clone https://github.com/SilentRequiem/ai201-project4-provenance-guard-starter-v2026.git
cd ai201-project4-provenance-guard-starter-v2026
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python test.py
python detector.py
~~~

If Python 3.13 is not installed, use a supported Python 3.11 or 3.12 installation and adjust the `py -3.13` command. Running `python detector.py` downloads the GPT-2 weights (roughly 550 MB) if they are not cached, then scores a sample.

Start the app from the root folder after activation:

~~~powershell
$env:AI201_DEBUG = "0"
python app.py
~~~

**macOS or Linux**

~~~bash
git clone https://github.com/SilentRequiem/ai201-project4-provenance-guard-starter-v2026.git
cd ai201-project4-provenance-guard-starter-v2026
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python test.py
python detector.py
AI201_DEBUG=0 python app.py
~~~

Use a Python version from 3.11 through 3.13. The local app is intended for a single machine. These clean-checkout steps are documented for reproducibility, but a fresh installation on someone else's computer was not independently verified during Unit 9.

**For Unit 10 peer testing:** Give your partner this file. If they cannot install dependencies and load the model in the allotted five minutes, record the exact step that blocked them. If your laptop is already set up, let them try the live local endpoints as well. Model installation can take longer than the five-minute peer-testing window.

## API routes

| Route | Status | Purpose |
|---|---|---|
| `POST /ping` | Implemented | Basic request/response control |
| `GET /health` | Implemented | Reports service health, model-load status, rate limiting, and audit entry count |
| `POST /submit` | Implemented | Validates writing, computes both signals, returns a label, and writes a decision |
| `POST /appeal` | Implemented | Records a challenge to an existing `content_id` as `under_review` |
| `GET /log?limit=5` | Implemented | Shows recent audit records; defaults to 50, maximum 1,000 |

Submissions require a nonempty `creator_id` and valid text. Very short, unsupported, or oversized inputs are rejected rather than being assigned an unreliable classification. Rate limiting is enabled by default at 10 submissions/minute and 200/day per creator. A busy or recently used demo creator ID may receive HTTP 429; use a new creator ID or wait for the limit to reset.

## Project files

| File | Purpose |
|---|---|
| `app.py` | Flask endpoints and request-timing hooks |
| `detector.py` | Local GPT-2 signal |
| `stylometry.py` | Writing-style signal |
| `scoring.py` | Combined score and cautious labels |
| `config.py` | Model, score thresholds, limits, log paths, and 1 MiB rotation size |
| `audit.py` | Decision, appeal, and rejection audit records |
| `request_telemetry.py` | Per-request input/output and elapsed-time logging |
| `log_rotation.py` | Numbered archives and archive-aware reads |
| `criteria.md` | User-authored acceptance criteria from Units 7 and 9 |
| `logs/audit.jsonl` | Active audit file |
| `logs/requests.jsonl` | Active request telemetry |
| `results/` | Actual Unit 8/9 test logs, results, and benchmark evidence |
| `test_capstone_rotation.py` | Isolated log rotation regression tests |
| `capstone_eval.py` | Unit 9 five-criterion, three-trial evaluation |
| `capstone_tail_benchmark.py` | Controlled old-versus-new log lookup benchmark |

## Troubleshooting

| Symptom | What to check |
|---|---|
| `.venv\Scripts\Activate.ps1` not found | Create the virtual environment and install `requirements.txt` as shown above |
| `python` not recognized | Install a supported Python version and open a new terminal |
| `Address already in use` | Another service is running on port 5000; stop that process before starting another |
| `/health` works but `detector_loaded` is `false` | The model loads on the first actual submission; `python detector.py` can download/cache it in advance |
| A first request is unusually slow | GPT-2 is loading into memory; later warm requests are usually faster |
| HTTP 400 | Missing or invalid JSON, text, or creator ID |
| HTTP 413 | Submitted text exceeds 20,000 characters |
| HTTP 422 | Text was judged unscorable by the input guard (for example, emoji-only or fewer than three English words) |
| HTTP 429 | Creator hit the configured rate limit |
| HTTP 503 | The local detector could not load or run; check installation, model files, memory, and the server terminal |
| `curl` behaves strangely in Windows PowerShell | Prefer `Invoke-RestMethod` as in this file, or use `curl.exe` rather than PowerShell's `curl` alias |
| Appeal returns HTTP 404 | Check that the submitted `content_id` exists in the audit history |

The classifier's signals are imperfect. Predictable human writing can resemble generated text, and edited AI text can evade confident detection. The service deliberately includes `unsure` and an appeal route because a score is not proof. Log rotation limits each individual file, **not the total space** used by retained archives. This single-process local configuration is not production hosting.

## Reproducing earlier course results (optional)

Unit 7 built the two signals, score combination, labels, and appeal path. Unit 8 enabled rate limiting and tested 56 staff attacks; the final validation change improved the count held from 42/56 to 47/56, with nine AI-evasion cases still broken. Unit 9 added structured timing logs and rotation, then measured one recent-log lookup optimization without changing the detector.

The capstone criteria were committed before results. The actual BEFORE and AFTER evaluations are already saved in `results/` and summarized in [README.md](README.md). You **do not need to rerun them** for Demo Day. If you are deliberately reproducing the unit instead, use `run_unit9_before.ps1` and `run_unit9_after.ps1` only with awareness that those scripts generate and commit new evidence.

For Demo Day, keep `criteria.md`, the Capstone tables in `README.md`, and this quick-start section open. The recorded recent-log benchmark was **23.55 ms vs. 2.11 ms** on the same synthetic 1,200-entry fixture, about **11.14 times faster**.
