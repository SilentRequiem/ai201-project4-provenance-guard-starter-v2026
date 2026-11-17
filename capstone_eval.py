#!/usr/bin/env python3
"""
Unit 9 before/after evaluation: five user-authored criteria, three trials each.

Run only after the Unit 9 criteria have been committed. This script starts
and restarts the existing local service, collects real HTTP and log outputs,
and saves evidence without inventing verdicts. It uses synthetic text only.

    python capstone_eval.py --label before
    python capstone_eval.py --label after

Close any other app.py process before running. The BEFORE results must be
reviewed and one improvement committed before running AFTER.
"""

import argparse
from datetime import datetime, timezone
import json
import os
import shutil
from pathlib import Path
import socket
import statistics
import subprocess
import sys
import tempfile
import time
import uuid

import requests

import audit
import config
import log_rotation
import request_telemetry


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
BASE = "http://127.0.0.1:5000"
TEXT = (
    "I am testing request logging in a local service. The same text is "
    "submitted with different identifiers so response times can be compared. "
    "This is synthetic test data and makes no claim about real authorship."
)
REQUIRED = {
    "timestamp", "request_id", "method", "route", "input",
    "output", "duration_ms", "cpu_seconds",
}
ERROR_PAYLOADS = [
    ("missing_text", lambda c: {"creator_id": c}),
    ("empty_text", lambda c: {"creator_id": c, "text": ""}),
    ("null_text", lambda c: {"creator_id": c, "text": None}),
    ("unsupported_text", lambda c: {"creator_id": c, "text": "🙂🙂🙂"}),
    ("oversize_text", lambda c: {"creator_id": c, "text": "word " * 4500}),
]


def port_in_use() -> bool:
    try:
        with socket.create_connection(("127.0.0.1", 5000), timeout=0.5):
            return True
    except OSError:
        return False


class LocalService:
    def __init__(self, label):
        self.process = None
        self.output_path = RESULTS / f"capstone_server_{label}.txt"
        self.handle = None

    def start(self):
        env = os.environ.copy()
        env["AI201_DEBUG"] = "0"
        env["HOST"] = "127.0.0.1"
        env["PORT"] = "5000"
        self.handle = self.output_path.open("a", encoding="utf-8")
        self.process = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd=str(ROOT),
            env=env,
            stdout=self.handle,
            stderr=subprocess.STDOUT,
        )
        for _ in range(100):
            if self.process.poll() is not None:
                raise RuntimeError("Local service exited. Check " + str(self.output_path))
            try:
                r = requests.get(BASE + "/health", timeout=2)
                if r.status_code == 200 and r.json().get("ok"):
                    return
            except (requests.RequestException, ValueError):
                pass
            time.sleep(0.2)
        raise RuntimeError("Local service did not pass /health. Check " + str(self.output_path))

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)
        self.process = None
        if self.handle:
            self.handle.close()
            self.handle = None
        # Make sure the next run can bind the same local port.
        for _ in range(50):
            if not port_in_use():
                return
            time.sleep(0.1)

    def restart(self):
        self.stop()
        self.start()


def summary_rows(ids):
    return [
        entry for entry in request_telemetry.read_requests()
        if entry.get("input", {}).get("creator_id") in ids
    ]


def rotation_probe() -> dict:
    """Force real 1 MiB rollover in isolated files without fabricating HTTP logs.

    Keep the files on disk until after restarting the service, when they will
    be reopened to check whether the archive survived.
    """
    folder = tempfile.mkdtemp(prefix="unit9_archive_")
    test_path = Path(folder) / "requests.jsonl"
    names = []
    for index in range(140):
        identity = f"probe-{index:03d}"
        names.append(identity)
        log_rotation.append_jsonl(test_path, {
            "timestamp": "2026-11-17T00:00:00+00:00",
            "request_id": identity,
            "method": "POST",
            "route": "/submit",
            "input": {"creator_id": identity, "text_chars": 9000},
            "output": {"http_status": 200},
            "duration_ms": 1.2,
            "cpu_seconds": 0.0007,
            "padding": "x" * 9000,
        })
    files = log_rotation.all_paths(test_path)
    found = [x.get("request_id") for x in log_rotation.read_jsonl(test_path)]
    sizes = [file.stat().st_size for file in files]
    return {
        "rotated": len(files) > 1,
        "files": [p.name for p in files],
        "file_sizes_bytes": sizes,
        "limit_bytes": config.LOG_ROTATION_BYTES,
        "all_files_within_limit": all(x <= config.LOG_ROTATION_BYTES for x in sizes),
        "records_recovered": len(found),
        "expected_records": 140,
        "records_in_original_order": found == names,
        "_temporary_path": str(test_path),
    }


def one_submission(creator_id):
    started = time.perf_counter()
    try:
        r = requests.post(
            BASE + "/submit",
            json={"text": TEXT, "creator_id": creator_id},
            timeout=180,
        )
        try:
            body = r.json()
        except ValueError:
            body = {"unparseable_body": r.text[:500]}
        return {
            "creator_id": creator_id,
            "status": r.status_code,
            "client_duration_ms": round((time.perf_counter() - started) * 1000, 3),
            "response": body,
        }
    except requests.RequestException as exc:
        return {
            "creator_id": creator_id,
            "status": None,
            "client_duration_ms": round((time.perf_counter() - started) * 1000, 3),
            "error": str(exc),
        }


def test_trial(trial, label, service):
    prefix = f"u9_{label}_{trial}_{uuid.uuid4().hex[:8]}"
    print(f"Trial {trial}/3: warming the local model...", flush=True)
    warmup = one_submission(prefix + "_warmup")
    if warmup["status"] != 200:
        raise RuntimeError("Warmup failed: " + json.dumps(warmup)[:500])

    # Reuse the exact ten successful calls for criteria 1, 2 and 5.
    samples = [one_submission(f"{prefix}_good_{i:02d}") for i in range(1, 11)]
    by_id = {x["creator_id"]: x for x in samples}
    telemetry = summary_rows(set(by_id))
    records = {x["input"]["creator_id"]: x for x in telemetry}

    good_logs = {}
    timing_differences = {}
    for cid, sent in by_id.items():
        row = records.get(cid)
        good_logs[cid] = bool(
            sent.get("status") == 200
            and row is not None
            and REQUIRED.issubset(row)
            and isinstance(row.get("input"), dict)
            and row["input"].get("text_sha256")
            and isinstance(row.get("output"), dict)
            and row["output"].get("http_status") == 200
            and isinstance(row.get("duration_ms"), (int, float))
            and isinstance(row.get("cpu_seconds"), (int, float))
        )
        if row and isinstance(row.get("duration_ms"), (int, float)):
            timing_differences[cid] = round(
                abs(sent["client_duration_ms"] - row["duration_ms"]), 3
            )

    probe = rotation_probe()
    complete = sum(good_logs.values())
    pass1 = (complete == 10 and probe["rotated"]
             and probe["all_files_within_limit"]
             and probe["records_recovered"] == 140
             and probe["records_in_original_order"])
    accurate = sum(diff <= 200 for diff in timing_differences.values())
    pass2 = accurate == 10 and len(timing_differences) == 10

    # Five genuinely rejected HTTP inputs, each with its own audit+telemetry.
    invalid = []
    for case, payload_func in ERROR_PAYLOADS:
        creator = f"{prefix}_{case}"
        payload = payload_func(creator)
        try:
            response = requests.post(BASE + "/submit", json=payload, timeout=30)
            invalid.append({
                "case": case,
                "creator_id": creator,
                "status": response.status_code,
                "response": response.json(),
            })
        except (requests.RequestException, ValueError) as exc:
            invalid.append({
                "case": case,
                "creator_id": creator,
                "status": None,
                "error": str(exc),
            })

    failures_telemetry = {
        x["input"]["creator_id"]: x for x in summary_rows({
            x["creator_id"] for x in invalid
        })
    }
    failures_audit = {}
    for x in audit.read_entries():
        if x.get("creator_id") in {y["creator_id"] for y in invalid}:
            failures_audit.setdefault(x["creator_id"], []).append(x)

    each_failure = {}
    for record in invalid:
        creator = record["creator_id"]
        row = failures_telemetry.get(creator)
        rejection = failures_audit.get(creator, [])
        each_failure[creator] = bool(
            record["status"] in (400, 413, 422)
            and row
            and row.get("output", {}).get("http_status") == record["status"]
            and isinstance(row.get("duration_ms"), (int, float))
            and row.get("timestamp")
            and len([x for x in rejection if x.get("event") == "rejected"
                     and x.get("reason")]) == 1
        )
    pass4 = sum(each_failure.values()) == 5
    timings = [x["client_duration_ms"] for x in samples if x["status"] == 200]
    mean_ms = statistics.mean(timings) if len(timings) == 10 else None
    pass5 = mean_ms is not None and mean_ms < 2000

    # Confirm that the ten original HTTP records survive a process restart.
    service.restart()
    after_restart = summary_rows(set(by_id))
    found = {x["input"].get("creator_id") for x in after_restart}
    survived = len(set(by_id) & found)
    # The archive fixture is still present after the server restart. Reopen
    # it afresh and verify that all archived entries remain readable.
    probe_path = Path(probe.pop("_temporary_path"))
    archived_after_restart = log_rotation.read_jsonl(probe_path)
    probe["recovered_after_restart"] = len(archived_after_restart)
    probe["archives_survived_restart"] = (
        len(log_rotation.archived_paths(probe_path)) >= 1
        and [x.get("request_id") for x in archived_after_restart]
            == [f"probe-{i:03d}" for i in range(140)]
    )
    shutil.rmtree(probe_path.parent)
    pass3 = (survived == 10 and probe["rotated"]
             and probe["archives_survived_restart"])

    checks = [
        {
            "criterion": 1,
            "name": "Logging completeness and 1 MiB rotation",
            "target": "10/10 detailed records and safe 1 MiB rotation",
            "value": f"{complete}/10 with rotation={probe['rotated']}",
            "met": pass1,
            "evidence": {"requests": samples, "telemetry": telemetry,
                         "completeness_by_creator": good_logs,
                         "isolated_rotation_probe": probe},
        },
        {
            "criterion": 2,
            "name": "Timing accuracy",
            "target": "10/10 client vs server gaps <= 200 ms",
            "value": f"{accurate}/10 gaps <= 200 ms",
            "met": pass2,
            "evidence": {"timing_difference_ms": timing_differences,
                         "requests": samples, "telemetry": telemetry},
        },
        {
            "criterion": 3,
            "name": "Log persistence",
            "target": "10/10 service logs survive restart including archived history",
            "value": f"{survived}/10 after restart; archived probe={probe['rotated']}",
            "met": pass3,
            "evidence": {"telemetry_after_restart": after_restart,
                         "isolated_archive_probe": probe},
        },
        {
            "criterion": 4,
            "name": "Failure logging",
            "target": "5/5 invalid requests have their own detailed logs",
            "value": f"{sum(each_failure.values())}/5 valid rejection traces",
            "met": pass4,
            "evidence": {"requests": invalid,
                         "telemetry": list(failures_telemetry.values()),
                         "audit_entries": failures_audit,
                         "per_request_pass": each_failure},
        },
        {
            "criterion": 5,
            "name": "Average warm response time",
            "target": "Mean of ten warm requests < 2 seconds",
            "value": f"{mean_ms / 1000:.3f} seconds" if mean_ms is not None else "not measurable",
            "met": pass5,
            "evidence": {"requests": samples, "mean_ms": mean_ms,
                         "warmup_excluded": warmup},
        },
    ]
    for c in checks:
        print(f"  {c['criterion']}: {c['value']} => {'MET' if c['met'] else 'MISSED'}",
              flush=True)
    return {"trial": trial, "criteria": checks, "rotation_probe": probe}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", choices=("before", "after"), required=True)
    args = parser.parse_args()
    if port_in_use():
        raise SystemExit("Port 5000 already has a server. Close app.py and rerun.")
    if config.LOG_ROTATION_BYTES != 1024 * 1024:
        raise SystemExit("Expected the agreed 1 MiB log limit.")
    RESULTS.mkdir(exist_ok=True)

    service = LocalService(args.label)
    trials = []
    try:
        service.start()
        for trial in range(1, 4):
            trials.append(test_trial(trial, args.label, service))
    finally:
        service.stop()

    verdicts = []
    for number in range(1, 6):
        items = [
            next(x for x in trial["criteria"] if x["criterion"] == number)
            for trial in trials
        ]
        verdicts.append({
            "criterion": number,
            "name": items[0]["name"],
            "target": items[0]["target"],
            "run_1": items[0]["value"],
            "run_2": items[1]["value"],
            "run_3": items[2]["value"],
            "verdict": "MET" if all(x["met"] for x in items) else "MISSED",
        })

    summary = {
        "label": args.label,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "criteria_commit": "25085d33",
        "method": "Three independent trials; ten real warm HTTP requests per "
                  "trial for criteria 1, 2, 3 and 5; five invalid requests per "
                  "trial for criterion 4; service restarted after each trial. "
                  "A separate temporary 1 MiB fixture validates archive rollover "
                  "without filling the committed service log with fake HTTP events.",
        "verdicts": verdicts,
        "trials": trials,
    }
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    path = RESULTS / f"capstone_eval_{args.label}_{stamp}.json"
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")
    md = [
        f"# Unit 9 {args.label.upper()} capstone evaluation",
        "",
        "Created by capstone_eval.py using real local HTTP responses and JSONL logs.",
        "",
        "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
        "|---|---|---|---|---|---|",
    ]
    for row in verdicts:
        md.append(
            f"| {row['criterion']}. {row['name']} | {row['target']} | "
            f"{row['run_1']} | {row['run_2']} | {row['run_3']} | "
            f"**{row['verdict']}** |"
        )
    md.extend(["", "Complete HTTP responses, timing values, archived-log fixture "
               "results, and per-criterion traces are in the JSON file.",
               "No after-run success is claimed until the actual AFTER script runs.",
               ""])
    md_path = path.with_suffix(".md")
    md_path.write_text("\n".join(md), encoding="utf-8")

    print(f"Saved {path.relative_to(ROOT)}")
    print(f"Saved {md_path.relative_to(ROOT)}")
    print("All five criteria tested three times. Do not change targets.")


if __name__ == "__main__":
    main()
