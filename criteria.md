# Acceptance criteria — Provenance Guard

## 1. False positives

Out of 10 pieces of clearly human writing, at most 1 may be labeled high-confidence AI.

**Why this target:** False accusations are the worst mistake for this kind of system, so I want the false-positive rate to stay very low.

---

## 2. Score spread

Clearly AI and clearly human samples should differ by at least 0.25 in average confidence score.

**Why this target:** I want AI and human writing to be noticeably separated instead of producing nearly identical scores.

---

## 3. Label coverage

All three label variants must be reachable using at most 6 deliberately chosen test inputs.

**Why this target:** If one of the three labels cannot be reached with a small set of targeted examples, the score ranges are not useful.

---

## 4. Appeal path

5 out of 5 valid appeals must change the content status to `under_review` and be recorded in the audit log.

**Why this target:** Every valid appeal should work because the appeal is the writer's way to push back against a potentially wrong decision.

---

## 5. Bad input

5 out of 5 missing, empty, or invalid text requests must be rejected cleanly without causing a 500 error.

**Why this target:** Bad input should never crash the service. The caller should get a clear error instead.
