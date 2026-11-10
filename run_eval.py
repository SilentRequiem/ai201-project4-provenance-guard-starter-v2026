#!/usr/bin/env python3
"""
Run all five unchanged Unit 7 acceptance criteria across three trials.

Usage:
    python run_eval.py --label before
    python run_eval.py --label after

The actual HTTP responses, signal scores, appeal states and verdicts are
saved to results/ as JSON and Markdown. No detector results are fabricated.
"""

import argparse
from datetime import datetime
import json
import sys

import config
import scenarios


def request_result(session, url, body, timeout, label=""):
    """Send one JSON submission and retain the actual response and scores."""
    result = {"sent": str(body.get("text", "(missing)"))[:150], "case": label}
    try:
        response = session.post(url + "/submit", json=body, timeout=timeout)
        result["status"] = response.status_code
        try:
            payload = response.json()
        except ValueError:
            payload = {"error": "response_not_json", "body": response.text[:250]}
        result["response"] = payload
        for key in ("guess", "confidence", "model_score", "style_score", "content_id"):
            result[key] = payload.get(key)
    except Exception as exc:
        result["status"] = None
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def text_result(session, url, text, creator, timeout, label=""):
    return request_result(
        session, url, {"text": text, "creator_id": creator}, timeout, label
    )


def success_score(row):
    return row.get("status") == 200 and isinstance(row.get("confidence"), (int, float))


def run_trial(session, url, scenario, trial, timeout):
    kind = scenario["kind"]
    number = scenario["criterion"]
    rows = []
    outcome = None

    if kind in ("human", "coverage"):
        for i, text in enumerate(scenario["texts"], 1):
            rows.append(text_result(session, url, text,
                                    f"eval_c{number}_{trial}_{i}", timeout))
        if kind == "human":
            flagged = sum(row.get("guess") == "ai" for row in rows)
            valid = sum(success_score(row) for row in rows)
            passed = valid == 10 and flagged <= 1
            outcome = f"{flagged}/10 flagged AI ({valid}/10 scored)"
        else:
            guesses = {row.get("guess") for row in rows if success_score(row)}
            passed = len(rows) <= 6 and len(guesses) == 3
            outcome = f"{len(guesses)}/3 labels ({len(rows)} inputs)"

    elif kind == "score_spread":
        ai_scores, human_scores = [], []
        for origin in ("human", "ai"):
            for i, text in enumerate(scenario[origin], 1):
                row = text_result(session, url, text,
                                  f"eval_spread_{origin}_{trial}_{i}",
                                  timeout, origin)
                rows.append(row)
                if success_score(row):
                    (ai_scores if origin == "ai" else human_scores).append(
                        row["confidence"]
                    )
        if len(ai_scores) == len(scenario["ai"]) and len(human_scores) == len(scenario["human"]):
            ai_mean = sum(ai_scores) / len(ai_scores)
            human_mean = sum(human_scores) / len(human_scores)
            gap = ai_mean - human_mean
            passed = gap >= 0.25
            outcome = f"gap {gap:+.3f} (AI {ai_mean:.3f}, human {human_mean:.3f})"
        else:
            passed = False
            outcome = f"incomplete: {len(ai_scores)} AI, {len(human_scores)} human"

    elif kind == "appeal":
        passed_count = 0
        for i, text in enumerate(scenario["texts"], 1):
            row = text_result(session, url, text,
                              f"eval_appeal_{trial}_{i}", timeout)
            if row.get("status") == 200 and row.get("content_id"):
                content_id = row["content_id"]
                try:
                    response = session.post(
                        url + "/appeal",
                        json={"content_id": content_id,
                              "reasoning": f"Trial {trial}, item {i}: please review."},
                        timeout=timeout,
                    )
                    appeal_body = response.json()
                    log_response = session.get(url + "/log", timeout=timeout)
                    entries = log_response.json().get("entries", [])
                    logged = any(
                        e.get("content_id") == content_id
                        and e.get("event") == "appeal"
                        and e.get("status") == "under_review"
                        for e in entries
                    )
                    row["appeal_status"] = response.status_code
                    row["appeal_response"] = appeal_body
                    row["logged_under_review"] = logged
                    if (response.status_code == 200
                        and appeal_body.get("status") == "under_review"
                        and logged):
                        passed_count += 1
                except Exception as exc:
                    row["appeal_error"] = f"{type(exc).__name__}: {exc}"
            rows.append(row)
        passed = passed_count == 5
        outcome = f"{passed_count}/5 appeals under_review and logged"

    elif kind == "bad_input":
        passed_count = 0
        for i, body in enumerate(scenario["bodies"], 1):
            row = request_result(session, url, body, timeout, f"bad_{i}")
            if row.get("status") in (400, 413, 422):
                passed_count += 1
            rows.append(row)
        passed = passed_count == 5
        outcome = f"{passed_count}/5 rejected cleanly"

    else:
        raise ValueError(f"Unsupported scenario kind: {kind}")

    return {"trial": trial, "passed": passed, "outcome": outcome, "responses": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", default="before")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--url", default=f"http://{config.HOST}:{config.PORT}")
    parser.add_argument("--timeout", type=float, default=90)
    args = parser.parse_args()

    if args.trials < 3:
        raise SystemExit("At least three trials are required.")
    issues = scenarios.validate()
    if issues:
        raise SystemExit("\n".join(issues))

    import requests
    session = requests.Session()
    try:
        health = session.get(args.url + "/health", timeout=5)
        health.raise_for_status()
    except Exception as exc:
        raise SystemExit(f"Service unavailable at {args.url}: {exc}")

    report = {
        "label": args.label,
        "created_at": datetime.now().astimezone().isoformat(),
        "trials_per_criterion": args.trials,
        "service": args.url,
        "scenarios": [],
    }

    for scenario in scenarios.SCENARIOS:
        print(f"\n{scenario['criterion']}. {scenario['name']}")
        trials = []
        for i in range(1, args.trials + 1):
            result = run_trial(session, args.url, scenario, i, args.timeout)
            trials.append(result)
            print(f"  Trial {i}: {result['outcome']} - {'MET' if result['passed'] else 'MISSED'}")
        report["scenarios"].append({
            "criterion": scenario["criterion"],
            "name": scenario["name"],
            "target": scenario["target"],
            "trials": trials,
            "verdict": "MET" if all(t["passed"] for t in trials) else "MISSED",
        })

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    stem = f"eval_{args.label}_{stamp}"
    json_path = config.RESULTS_DIR / (stem + ".json")
    md_path = config.RESULTS_DIR / (stem + ".md")
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    rows = [
        f"# Run Log - {args.label}",
        "",
        "- Produced by: run_eval.py::main",
        f"- Three-trial test on {report['created_at']}",
        "",
        "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
        "|---|---|---|---|---|---|",
    ]
    for scenario in report["scenarios"]:
        values = [t["outcome"] for t in scenario["trials"]]
        rows.append(
            f"| {scenario['criterion']}. {scenario['name']} | {scenario['target']} | "
            + " | ".join(values[:3]) + f" | {scenario['verdict']} |"
        )
    rows.extend(["", "## Actual responses", ""])
    fence = chr(96) * 3
    for scenario in report["scenarios"]:
        rows.append(f"### {scenario['criterion']}. {scenario['name']}")
        for trial in scenario["trials"]:
            rows.extend([
                "",
                f"**Trial {trial['trial']}**: {trial['outcome']}",
                "",
                fence + "json",
                json.dumps(trial["responses"], indent=2),
                fence,
            ])
    md_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"\nWrote {json_path.relative_to(config.ROOT)}")
    print(f"Wrote {md_path.relative_to(config.ROOT)}")
    print("Keep all original criteria and compare all three trials honestly.")


if __name__ == "__main__":
    main()
