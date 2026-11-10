# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 02:04
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `b87da374c55a4ec49d74eb6f29ba465d` | unsure | 0.306 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `178e2854a3484e59b8cc4f7ef10847b9` | unsure | 0.437 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `76a948ad33074f61b7a55a25e2560be1` | unsure | 0.490 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `0cbaa3203ccb44e299f29a70143cfe4f` | unsure | 0.542 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `f68ddb25a62f474a9d1e189a307f2d0e` | human | 0.217 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `d2647da786194462a3e5dd2dd0c4bce1` | unsure | 0.443 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `671233d21c7544b69930cebf6d52a9cd` | unsure | 0.557 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `7590792c6353484bb80e96ac3b5ee430` | unsure | 0.330 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `60f3a19da475427bb4bcbf1b3a19ac65` | unsure | 0.497 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `f0abae2d101c4594960fc2a2b2750cac` | ai | 0.852 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `a4dbfa09116f4ee48541428e2501d4dc` | unsure | 0.497 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `7aa5b7590787414eb277fff20b0c645a` | unsure | 0.641 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `f18df59c142c4021ab33a47f26237a31` | unsure | 0.649 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `afa888a8375d400bbbf066dada6c5d53` | unsure | 0.558 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `6f7ddf9b912d450abb72c7be3a6693ba` | unsure | 0.699 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `313e518ff5e342128bc8f4b7b1c1fc21` | unsure | 0.557 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `757b1a9c08d54888abb8835debf3c7d2` | unsure | 0.579 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c8958bd328994f779f1394e59c5437e8` | unsure | 0.320 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `42fd1cb5b2104308ac56f8843a07270c` | unsure | 0.322 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `61500fc398644d60a2c09cf18ea8b89c` | human | 0.160 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `040cdd6c16e7427a832900a45ab8b774` | unsure | 0.476 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `fc161ca43a72450e9d4e4dc271e7ac37` | unsure | 0.395 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `ce16b1e0fd7d4d29ae14829987ff55cb` | unsure | 0.457 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `b8c0df07ba664c3792cab07aa0812377` | unsure | 0.470 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 422 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 422 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 422 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 422 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 422 | `—` | — | — |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `317d17e2317742e6bda6eddfd21bfac1` | unsure | 0.404 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dc0330e8f72348c68d9c515007806f8b` | unsure | 0.404 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `79ba6dc2188646f499250463d71c5e62` | unsure | 0.404 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4a6b0f95be844b28b4a135e135b554a8` | unsure | 0.404 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `aec8e33abb824928bfda5ab12c8ac0f6` | unsure | 0.404 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `28c00cd6d63643b486c1f7fa6611ddce` | unsure | 0.404 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0cd420c855d143879b28b4fd9e4225e5` | unsure | 0.404 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a2f3b15fae7b432199a40b211ea83fca` | unsure | 0.404 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6f2b90bf26a7496e9755dc2b06ad7624` | unsure | 0.404 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `facfb0a0c6374081887ee79a7f3da3b0` | unsure | 0.404 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "b87da374c55a4ec49d74eb6f29ba465d",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.3056,
  "model_score": 0.1635,
  "style_score": 0.4793,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "178e2854a3484e59b8cc4f7ef10847b9",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4373,
  "model_score": 0.5943,
  "style_score": 0.106,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "76a948ad33074f61b7a55a25e2560be1",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.49,
  "model_score": 0.6662,
  "style_score": 0.2523,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "0cbaa3203ccb44e299f29a70143cfe4f",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5424,
  "model_score": 0.6114,
  "style_score": 0.4581,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "f68ddb25a62f474a9d1e189a307f2d0e",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2168,
  "model_score": 0.3212,
  "style_score": 0.0893,
  "label": "Our signals suggest this text was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "d2647da786194462a3e5dd2dd0c4bce1",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4427,
  "model_score": 0.5727,
  "style_score": 0.1563,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "671233d21c7544b69930cebf6d52a9cd",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5568,
  "model_score": 0.5862,
  "style_score": 0.5208,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "7590792c6353484bb80e96ac3b5ee430",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3295,
  "model_score": 0.2452,
  "style_score": 0.4325,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "60f3a19da475427bb4bcbf1b3a19ac65",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.4968,
  "model_score": 0.7042,
  "style_score": 0.2363,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "f0abae2d101c4594960fc2a2b2750cac",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8522,
  "model_score": 0.9792,
  "style_score": 0.697,
  "label": "Our signals strongly suggest this text may be AI-generated. This is not proof, and the writer can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "a4dbfa09116f4ee48541428e2501d4dc",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.497,
  "model_score": 0.6175,
  "style_score": 0.3497,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "7aa5b7590787414eb277fff20b0c645a",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.641,
  "model_score": 0.7387,
  "style_score": 0.5216,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "f18df59c142c4021ab33a47f26237a31",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6487,
  "model_score": 0.8051,
  "style_score": 0.4575,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "afa888a8375d400bbbf066dada6c5d53",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.5585,
  "model_score": 0.8329,
  "style_score": 0.3532,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "6f7ddf9b912d450abb72c7be3a6693ba",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6991,
  "model_score": 0.8005,
  "style_score": 0.5751,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "313e518ff5e342128bc8f4b7b1c1fc21",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5567,
  "model_score": 0.8814,
  "style_score": 0.286,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "757b1a9c08d54888abb8835debf3c7d2",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5785,
  "model_score": 0.8816,
  "style_score": 0.3824,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c8958bd328994f779f1394e59c5437e8",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.3199,
  "model_score": 0.3223,
  "style_score": 0.3169,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "42fd1cb5b2104308ac56f8843a07270c",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.3219,
  "model_score": 0.4625,
  "style_score": 0.15,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "61500fc398644d60a2c09cf18ea8b89c",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1599,
  "model_score": 0.2044,
  "style_score": 0.1056,
  "label": "Our signals suggest this text was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "040cdd6c16e7427a832900a45ab8b774",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4761,
  "model_score": 0.5943,
  "style_score": 0.3316,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "fc161ca43a72450e9d4e4dc271e7ac37",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.3948,
  "model_score": 0.4998,
  "style_score": 0.2664,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "ce16b1e0fd7d4d29ae14829987ff55cb",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4569,
  "model_score": 0.6401,
  "style_score": 0.1374,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "b8c0df07ba664c3792cab07aa0812377",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4696,
  "model_score": 0.5583,
  "style_score": 0.3612,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "317d17e2317742e6bda6eddfd21bfac1",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4041,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "dc0330e8f72348c68d9c515007806f8b",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4041,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "79ba6dc2188646f499250463d71c5e62",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4041,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "4a6b0f95be844b28b4a135e135b554a8",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4041,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "aec8e33abb824928bfda5ab12c8ac0f6",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4041,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "28c00cd6d63643b486c1f7fa6611ddce",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4041,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "0cd420c855d143879b28b4fd9e4225e5",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4041,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "a2f3b15fae7b432199a40b211ea83fca",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4041,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "6f2b90bf26a7496e9755dc2b06ad7624",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4041,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "facfb0a0c6374081887ee79a7f3da3b0",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.4041,
  "model_score": 0.0287,
  "style_score": 0.65,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
