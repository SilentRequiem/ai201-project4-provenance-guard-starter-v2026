"""Focused standard-library tests for Unit 9 log rotation.

    python -m unittest -v test_capstone_rotation.py

They use temporary folders, so the real audit files and model are untouched.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

import audit
import config
import log_rotation
import request_telemetry


class LogRotationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.directory = Path(self.tmp.name)
        self.old_limit = config.LOG_ROTATION_BYTES
        self.old_audit = config.AUDIT_LOG
        self.old_requests = config.REQUEST_TELEMETRY_LOG
        config.LOG_ROTATION_BYTES = 600
        config.AUDIT_LOG = self.directory / "audit.jsonl"
        config.REQUEST_TELEMETRY_LOG = self.directory / "requests.jsonl"

    def tearDown(self):
        config.LOG_ROTATION_BYTES = self.old_limit
        config.AUDIT_LOG = self.old_audit
        config.REQUEST_TELEMETRY_LOG = self.old_requests
        self.tmp.cleanup()

    def test_rotation_preserves_all_request_records(self):
        for i in range(10):
            log_rotation.append_jsonl(config.REQUEST_TELEMETRY_LOG, {
                "timestamp": "2026-11-16T00:00:00Z",
                "request_id": f"capstone-{i:02d}",
                "input": {"creator_id": f"user-{i}"},
                "output": {"http_status": 200},
                "duration_ms": 15.2,
                "cpu_seconds": 0.008,
            })
        paths = log_rotation.all_paths(config.REQUEST_TELEMETRY_LOG)
        self.assertGreater(len(paths), 1)
        self.assertEqual([r["request_id"] for r in request_telemetry.read_requests()],
                         [f"capstone-{i:02d}" for i in range(10)])
        self.assertTrue(all(p.stat().st_size <= config.LOG_ROTATION_BYTES for p in paths))
        self.assertEqual(len(request_telemetry.read_requests(limit=3)), 3)

    def test_audit_decision_and_appeal_work_across_archives(self):
        audit.log_decision(content_id="first", creator_id="author",
                           guess="unsure", model_score=.5, style_score=.5,
                           combined_score=.5, label="unsure")
        for i in range(25):
            audit.log_rejection(creator_id=f"bad-{i}", reason="invalid_text")
        audit.log_appeal(content_id="first", creator_id="author",
                         reasoning="I want this reviewed.")
        self.assertGreater(len(log_rotation.archived_paths(config.AUDIT_LOG)), 0)
        history = audit.entries_for("first")
        self.assertEqual([x["status"] for x in history], ["decided", "under_review"])
        self.assertEqual(audit.count_entries(), 27)
        self.assertEqual(len(audit.read_entries(limit=5)), 5)

        # Independent second read stands in for a new process reopening files.
        self.assertEqual(log_rotation.count_jsonl(config.AUDIT_LOG), 27)

    def test_each_failure_gets_its_own_entry(self):
        for i in range(5):
            audit.log_rejection(creator_id=f"invalid-{i}", reason="invalid_text",
                                http_status=400, duration_ms=2.5)
        entries = audit.read_entries()
        self.assertEqual(len(entries), 5)
        self.assertEqual({e["creator_id"] for e in entries},
                         {f"invalid-{i}" for i in range(5)})
        self.assertTrue(all(e["reason"] == "invalid_text" for e in entries))

    def test_byte_limit_for_unicode_text(self):
        for i in range(12):
            log_rotation.append_jsonl(config.REQUEST_TELEMETRY_LOG,
                                      {"index": i, "text": "é" * 40})
        self.assertEqual(len(log_rotation.read_jsonl(config.REQUEST_TELEMETRY_LOG)), 12)
        self.assertTrue(all(p.stat().st_size <= 600 for p in
                            log_rotation.all_paths(config.REQUEST_TELEMETRY_LOG)))

    def test_oversized_user_reasoning_is_marked(self):
        config.LOG_ROTATION_BYTES = 1024 * 1024
        audit.log_appeal("first", "author", "long " * 300000)
        record = audit.read_entries()[0]
        self.assertTrue(record["oversize_entry"])
        self.assertTrue(record["reasoning_truncated"])
        self.assertGreater(record["reasoning_original_chars"], 1024 * 1024)
        self.assertLessEqual(config.AUDIT_LOG.stat().st_size, config.LOG_ROTATION_BYTES)

    def test_recent_log_lookup_matches_full_history_across_archives(self):
        for i in range(80):
            log_rotation.append_jsonl(config.REQUEST_TELEMETRY_LOG, {
                "request_id": f"tail-{i:03d}",
                "input": {"creator_id": "synthetic"},
                "padding": "a" * 90,
            })
        all_rows = log_rotation.read_jsonl(config.REQUEST_TELEMETRY_LOG)
        self.assertGreater(len(log_rotation.archived_paths(config.REQUEST_TELEMETRY_LOG)), 1)
        for limit in (1, 5, 20, 50, 200):
            self.assertEqual(
                log_rotation.read_jsonl(config.REQUEST_TELEMETRY_LOG, limit=limit),
                all_rows[-limit:],
            )

        # Include an invalid final JSON line. Recent reads should ignore it
        # and preserve the order of the most recent complete valid entries.
        with config.REQUEST_TELEMETRY_LOG.open("a", encoding="utf-8") as handle:
            handle.write("{broken json\\n")
        self.assertEqual(
            log_rotation.read_jsonl(config.REQUEST_TELEMETRY_LOG, limit=5),
            all_rows[-5:],
        )

    def test_empty_log_reads_are_clean(self):
        self.assertEqual(audit.read_entries(), [])
        self.assertEqual(audit.count_entries(), 0)
        self.assertEqual(request_telemetry.read_requests(), [])


if __name__ == "__main__":
    unittest.main()
