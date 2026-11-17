"""
Size-limited, append-only JSONL logs for one local server process.

Active: requests.jsonl
Archives: requests.000001.jsonl, requests.000002.jsonl, ...

Every complete entry is written to exactly one file. Files are rotated before
the next entry would take them above LOG_ROTATION_BYTES. Old archives stay.
This is for one local process, not a multi-worker production deployment.
"""

from collections import deque
from hashlib import sha256
import json
from pathlib import Path
import threading

import config

_lock = threading.RLock()


def archived_paths(active: Path) -> list[Path]:
    """Find numbered archives in oldest-to-newest order."""
    active = Path(active)
    prefix, suffix = active.stem + ".", active.suffix
    numbered = []
    for path in active.parent.glob(f"{active.stem}.*{suffix}"):
        middle = path.name[len(prefix):-len(suffix)]
        if middle.isdigit():
            numbered.append((int(middle), path))
    return [path for _, path in sorted(numbered)]


def all_paths(active: Path) -> list[Path]:
    """Read archives first, then the current file."""
    active = Path(active)
    paths = archived_paths(active)
    if active.exists():
        paths.append(active)
    return paths


def _next_archive(active: Path) -> Path:
    paths = archived_paths(active)
    last = max((int(p.name[len(active.stem) + 1:-len(active.suffix)]) for p in paths),
               default=0)
    return active.with_name(f"{active.stem}.{last + 1:06d}{active.suffix}")


def _encode(entry: dict) -> bytes:
    """Store compact UTF-8 JSON. Avoid one huge value bypassing the 1 MiB cap."""
    data = (json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    if len(data) <= config.LOG_ROTATION_BYTES:
        return data

    # Preserve the event, status and identifiers. Note when very long user
    # supplied values had to be shortened; do not silently lose that fact.
    shortened = {}
    for key, value in entry.items():
        if isinstance(value, str) and len(value) > 4096:
            shortened[key] = value[:4096]
            shortened[f"{key}_original_chars"] = len(value)
            shortened[f"{key}_truncated"] = True
        else:
            shortened[key] = value

    shortened["oversize_entry"] = True
    shortened["original_bytes"] = len(data)
    shortened["original_sha256"] = sha256(data).hexdigest()
    data = (json.dumps(shortened, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    if len(data) > config.LOG_ROTATION_BYTES:
        raise ValueError("A single log entry exceeds the 1 MiB limit even after truncating long text fields")
    return data


def append_jsonl(active: Path, entry: dict) -> None:
    active = Path(active)
    data = _encode(entry)
    with _lock:
        active.parent.mkdir(parents=True, exist_ok=True)
        if active.exists() and active.stat().st_size + len(data) > config.LOG_ROTATION_BYTES:
            active.replace(_next_archive(active))
        with active.open("ab") as handle:
            handle.write(data)


def iter_jsonl(active: Path):
    """Stream every complete record from all archives and the active log."""
    # Hold the same lock as the writer while opening paths. Otherwise a
    # simultaneous rollover may rename requests.jsonl between listing and open.
    with _lock:
        for path in all_paths(active):
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    if not line.strip():
                        continue
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        # Keep older data available despite one damaged entry.
                        continue


def read_jsonl(active: Path, limit: int | None = None) -> list[dict]:
    if limit is not None:
        if limit <= 0:
            return []
        return list(deque(iter_jsonl(active), maxlen=limit))
    return list(iter_jsonl(active))


def count_jsonl(active: Path) -> int:
    return sum(1 for _ in iter_jsonl(active))

def clear_active(active: Path) -> int:
    """Explicitly clear only the current file, not any retained archives."""
    active = Path(active)
    with _lock:
        if not active.exists():
            return 0
        with active.open("r", encoding="utf-8") as handle:
            count = sum(1 for line in handle if line.strip())
        active.unlink()
        return count
