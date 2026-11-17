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


# Unit 9 Capstone

## 1. Logging completeness

10/10 requests logged with detailed records and 1 MB rotation

**Why this target:** Comprehensive logging is essential for auditing and debugging purposes.

---

## 2. Timing accuracy

Client and server measurements differ by no more than 200 ms

**Why this target:** Accurate timing is crucial for performance analysis and ensuring the system behaves as expected under real-world conditions.

---

## 3. Log persistence

10/10 records survive a restart, including archived records

**Why this target:** Persistent logs are necessary for long-term auditing and compliance, ensuring that no critical information is lost during system restarts or failures.

---

## 4. Failure logging

5/5 failed requests have their own detailed log entries

**Why this target:** Detailed logging of failed requests is essential for diagnosing and resolving issues, as well as for compliance and auditing purposes.

---

## 5. Average response time

Under 2 seconds across 10 warm requests

**Why this target:** Maintaining a low average response time is critical for user satisfaction and system performance, ensuring that the service remains responsive under typical load conditions.
