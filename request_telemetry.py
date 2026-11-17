"""
Capstone request telemetry.

Records the shape of each HTTP request and its result in structured JSONL.
Only a short input preview, character count, and digest are retained.
The original decision audit log remains untouched.
"""

from datetime import datetime, timezone
from hashlib import sha256
import time
import uuid

import config
import log_rotation


def new_request_id() -> str:
    return uuid.uuid4().hex


def _input_summary(request) -> dict:
    payload = request.get_json(silent=True)
    info = {
        "content_type": request.mimetype or "",
        "body_kind": type(payload).__name__,
        "creator_id": None,
        "text_chars": None,
        "text_sha256": None,
        "text_preview": None,
    }

    if isinstance(payload, dict):
        creator = payload.get("creator_id")
        if isinstance(creator, str):
            info["creator_id"] = creator[:100]
        value = payload.get("text")
        if isinstance(value, str):
            info["text_chars"] = len(value)
            info["text_sha256"] = sha256(value.encode("utf-8")).hexdigest()
            info["text_preview"] = value[:80].replace("\n", " ")
        else:
            info["text_kind"] = type(value).__name__

    return info


def _output_summary(response) -> dict:
    data = response.get_json(silent=True)
    info = {"http_status": response.status_code}
    if isinstance(data, dict):
        for key in ("content_id", "guess", "status", "error", "model_score",
                    "style_score", "confidence"):
            if key in data:
                info[key] = data[key]
    return info


def record_request(request, response, request_id: str,
                   started_ns: int, cpu_started_ns: int) -> dict:
    """Persist one request with a timestamp, input, output and measured cost."""
    duration_ms = (time.perf_counter_ns() - started_ns) / 1_000_000
    cpu_seconds = max(0.0, (time.process_time_ns() - cpu_started_ns) / 1_000_000_000)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "request_id": request_id,
        "method": request.method,
        "route": request.path,
        "input": _input_summary(request),
        "output": _output_summary(response),
        "duration_ms": round(duration_ms, 3),
        "cpu_seconds": round(cpu_seconds, 6),
    }

    log_rotation.append_jsonl(config.REQUEST_TELEMETRY_LOG, entry)
    return entry


def read_requests(limit: int | None = None) -> list[dict]:
    """Include both archived request logs and the current file."""
    return log_rotation.read_jsonl(config.REQUEST_TELEMETRY_LOG, limit=limit)
