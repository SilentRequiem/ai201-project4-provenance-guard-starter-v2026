#!/usr/bin/env python3
"""
Supplemental Unit 9 comparison of bounded log lookup algorithms.

This runs after the one improvement. Both paths use the SAME local synthetic
archive fixture. The "original" function is the exact original lookup:
list(deque(log_rotation.iter_jsonl(path), maxlen=limit)). The optimized path
calls log_rotation.read_jsonl(path, limit). This does not claim to be a run
of the old checkout; the official BEFORE and AFTER live-service tests are
separate in capstone_eval.py.

    python capstone_tail_benchmark.py --label after
"""
import argparse
from collections import deque
from datetime import datetime, timezone
import json
from pathlib import Path
import statistics
import tempfile
import time

import config
import log_rotation


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def original_recent_records(path, limit):
    return list(deque(log_rotation.iter_jsonl(path), maxlen=limit))


def measured_call(fn, path, limit, rounds):
    durations = []
    output = None
    for _ in range(rounds):
        start = time.perf_counter()
        output = fn(path, limit)
        durations.append(round((time.perf_counter() - start) * 1000, 6))
    return output, durations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", choices=["after"], required=True)
    args = parser.parse_args()
    if config.LOG_ROTATION_BYTES != 1024 * 1024:
        raise SystemExit("This comparison expects the agreed 1 MiB log limit.")

    with tempfile.TemporaryDirectory(prefix="capstone_tail_") as folder:
        path = Path(folder) / "requests.jsonl"
        count = 1200
        for index in range(count):
            log_rotation.append_jsonl(path, {
                "timestamp": "2026-11-17T00:00:00+00:00",
                "request_id": f"synthetic-{index:05d}",
                "method": "POST",
                "route": "/submit",
                "input": {"creator_id": "benchmark", "text_chars": 8500},
                "output": {"http_status": 200},
                "duration_ms": 3.5,
                "cpu_seconds": 0.001,
                "padding": "x" * 8500,
            })

        paths = log_rotation.all_paths(path)
        sizes = [x.stat().st_size for x in paths]
        limit = 50
        reference, old_times = measured_call(original_recent_records, path, limit, 10)
        actual, new_times = measured_call(log_rotation.read_jsonl, path, limit, 10)
        if reference != actual or len(actual) != 50:
            raise SystemExit("Optimized latest-50 reader did not match the original reader.")
        if len(paths) < 2 or not all(x <= config.LOG_ROTATION_BYTES for x in sizes):
            raise SystemExit("The synthetic fixture did not rotate correctly.")

        med_old = statistics.median(old_times)
        med_new = statistics.median(new_times)
        report = {
            "label": args.label,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "fixture": "Synthetic 1200-record local JSONL history; not fabricated HTTP events",
            "old_implementation": "list(deque(log_rotation.iter_jsonl(path), maxlen=50))",
            "new_implementation": "log_rotation.read_jsonl(path, limit=50)",
            "limit": limit,
            "fixture_records": count,
            "archive_and_active_files": [x.name for x in paths],
            "file_sizes_bytes": sizes,
            "same_last_50_in_original_order": reference == actual,
            "rounds_each": 10,
            "original_elapsed_ms": old_times,
            "optimized_elapsed_ms": new_times,
            "original_median_ms": round(med_old, 6),
            "optimized_median_ms": round(med_new, 6),
            "median_speedup": round(med_old / med_new, 3) if med_new else None,
        }

    RESULTS.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    output = RESULTS / f"capstone_tail_benchmark_{args.label}_{stamp}.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Archived fixture: {count} synthetic entries across {len(paths)} log files")
    print(f"Both readers returned identical newest {len(reference)} entries.")
    print(f"Original reader median: {report['original_median_ms']} ms")
    print(f"Optimized reader median: {report['optimized_median_ms']} ms")
    print(f"Observed median speedup: {report['median_speedup']}x")
    print(f"Saved: {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
