#!/usr/bin/env python3
"""
Measure the cost of ten real local Provenance Guard submissions.

Run only after your five Unit 9 criteria have been written and committed:
    python capstone_measure.py --label before
    python capstone_measure.py --label after

This is a measurement tool, not a substitute for the five-criterion tests.
It never assumes that a submission should be classified AI or human.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import statistics
import time
import uuid

import requests


ROOT = Path(__file__).resolve().parent
LOG_PATH = ROOT / "logs" / "requests.jsonl"
RESULTS_DIR = ROOT / "results"
TEXT = (
    "This is synthetic writing made only to check the local service. "
    "It includes ordinary sentences so the detector can evaluate its text. "
    "The timing, response, and log entry should all be visible after the request."
)


def read_telemetry(ids):
    if not LOG_PATH.exists():
        return []
    matches = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        try:
            entry = json.loads(line)
            if entry.get("input", {}).get("creator_id") in ids:
                matches.append(entry)
        except (ValueError, TypeError):
            continue
    return matches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", required=True, choices=["before", "after"])
    parser.add_argument("--url", default="http://127.0.0.1:5000")
    args = parser.parse_args()

    session = requests.Session()
    base_url = args.url.rstrip("/")
    health = session.get(base_url + "/health", timeout=10)
    health.raise_for_status()
    if not health.json().get("ok"):
        raise RuntimeError("Service health check failed.")

    # The first submission might load GPT-2. Keep it separate from warm runs.
    prefix = uuid.uuid4().hex[:10]
    warmup = session.post(
        base_url + "/submit",
        json={"text": TEXT, "creator_id": f"capstone_warmup_{prefix}"},
        timeout=120,
    )
    warmup.raise_for_status()

    requests_out = []
    creators = set()
    for i in range(1, 11):
        creator_id = f"capstone_{args.label}_{prefix}_{i:02d}"
        creators.add(creator_id)
        started = time.perf_counter()
        try:
            response = session.post(
                base_url + "/submit",
                json={"text": TEXT, "creator_id": creator_id},
                timeout=120,
            )
            body = response.json()
            record = {
                "trial": i,
                "creator_id": creator_id,
                "http_status": response.status_code,
                "client_elapsed_seconds": round(time.perf_counter() - started, 6),
                "response": body,
            }
        except Exception as exc:
            record = {
                "trial": i,
                "creator_id": creator_id,
                "client_elapsed_seconds": round(time.perf_counter() - started, 6),
                "error": f"{type(exc).__name__}: {exc}",
            }
        requests_out.append(record)

    # Verify that a bad request leaves a structured failure record too.
    bad_id = f"capstone_bad_{prefix}"
    creators.add(bad_id)
    invalid = session.post(
        base_url + "/submit",
        json={"creator_id": bad_id},
        timeout=20,
    )
    bad_record = {
        "creator_id": bad_id,
        "http_status": invalid.status_code,
        "response": invalid.json(),
    }

    server_entries = read_telemetry(creators)
    good = [x for x in requests_out if x.get("http_status") == 200]
    wall_seconds = [x["client_elapsed_seconds"] for x in good]
    server_seconds = [
        x["duration_ms"] / 1000
        for x in server_entries
        if x.get("input", {}).get("creator_id") in creators - {bad_id}
        and x.get("output", {}).get("http_status") == 200
        and isinstance(x.get("duration_ms"), (int, float))
    ]
    cpu_seconds = [
        x["cpu_seconds"]
        for x in server_entries
        if x.get("input", {}).get("creator_id") in creators - {bad_id}
        and x.get("output", {}).get("http_status") == 200
        and isinstance(x.get("cpu_seconds"), (int, float))
    ]

    report = {
        "label": args.label,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "description": "Ten warm local synthetic submissions; first model-load warmup excluded",
        "successes": len(good),
        "attempted": len(requests_out),
        "telemetry_entries_found": len(server_entries),
        "mean_client_elapsed_seconds": round(statistics.mean(wall_seconds), 6) if wall_seconds else None,
        "mean_server_elapsed_seconds": round(statistics.mean(server_seconds), 6) if server_seconds else None,
        "mean_process_cpu_seconds": round(statistics.mean(cpu_seconds), 6) if cpu_seconds else None,
        "hundred_requests_wall_seconds": round(100 * statistics.mean(wall_seconds), 3) if wall_seconds else None,
        "requests": requests_out,
        "invalid_request": bad_record,
        "telemetry_extract": server_entries,
    }

    RESULTS_DIR.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    dest = RESULTS_DIR / f"capstone_cost_{args.label}_{stamp}.json"
    dest.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(good)}/10 successful submissions")
    print(f"{len(server_entries)}/11 structured log entries found, including invalid input")
    print(f"Mean client time per successful request: {report['mean_client_elapsed_seconds']} seconds")
    print(f"Mean server time per successful request: {report['mean_server_elapsed_seconds']} seconds")
    print(f"Mean process CPU time per successful request: {report['mean_process_cpu_seconds']} seconds")
    print(f"At 100 requests/day: {report['hundred_requests_wall_seconds']} seconds total client waiting time")
    print(f"Bad request returned: HTTP {invalid.status_code}")
    print(f"Saved: {dest.relative_to(ROOT)}")
    if len(good) != 10 or len(server_entries) < 11 or invalid.status_code != 400:
        raise SystemExit("Measurement completed but at least one service or telemetry check failed.")


if __name__ == "__main__":
    main()
