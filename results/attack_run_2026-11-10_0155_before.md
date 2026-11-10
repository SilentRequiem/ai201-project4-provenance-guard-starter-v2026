# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 01:55
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `a0c6ca99da044562928088a5194c1dc9` | unsure | 0.306 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `4f39a45408d74044b46a7847063b6683` | unsure | 0.437 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `5aa38f6b9e734e7ba77371caf69b9aa6` | unsure | 0.490 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `20b19f27fe664dd78abf63b8468b8d0d` | unsure | 0.542 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `13c4c349bd6c486080eedeab515b3d4f` | human | 0.217 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `b2dd355f752741cda3e927fdfc130000` | unsure | 0.443 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `745328462c5d4574a9570a867896991c` | unsure | 0.557 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `335635debcc94cad9e64638699940760` | unsure | 0.330 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `641492fb0906467dbe05adad006123a4` | unsure | 0.497 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `7fa7144f363f4e74a8c75c4acfb20f5a` | ai | 0.852 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `024d8398437c4a2ab20f75a7366092f4` | unsure | 0.497 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `9bd2e958c37541268505002b9245ac87` | unsure | 0.641 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `47ca5f01a7cb40afaf2a5e2dacef1944` | unsure | 0.649 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `e1ab64a3556347a09861e7057b1b4617` | unsure | 0.558 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `84698f6b9b7145c0a54712b1b4d24e28` | unsure | 0.699 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `902d0f5ba758420da0e15ba038098699` | unsure | 0.557 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `2bf24cb41af04421950a381ca20d278c` | unsure | 0.579 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `b877208578b743878d52a6f58ac2a4e9` | unsure | 0.320 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `fe1d73920bfa40d2ae29a29b8d74f4a9` | unsure | 0.322 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `ecadf13c098a43eaad49a61c9954d4df` | human | 0.160 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `1ce00ca5b97141a0bc04c764fb2bb75e` | unsure | 0.476 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `7bf777431d9346b9904f82ee12ad3fc3` | unsure | 0.395 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `056f4b0b916f4ee5af20f93fae170d96` | unsure | 0.457 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `761bdea098c24008b7f02a2a693479d0` | unsure | 0.470 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `87012512992940abb4b5be9cf7a878c6` | unsure | 0.396 |  |
| MF04 | malformed | text is only punctuation | 200 | `41737d541bf84e5cace0e5923a55796f` | unsure | 0.478 |  |
| MF05 | malformed | text is a very long single word | 200 | `05b683a9c9fb4b69a290c43d511bfde1` | ai | 0.841 |  |
| MF06 | malformed | text is emoji only | 200 | `2036bbd5ea3546019d0307b615dd9c46` | ai | 0.998 |  |
| MF07 | malformed | text is right-to-left script | 200 | `c960fe83609c4e00a291e4f225d70790` | ai | 0.949 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7e333f5b3c2e4fa1a897a18e376d13c1` | unsure | 0.404 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `aa6c65a5ef3f41b68d567e7423744b84` | unsure | 0.404 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `27c5701aba634531aebe45e5a7c7b3a1` | unsure | 0.404 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `229fb30e3bac406da6509de41fb0b238` | unsure | 0.404 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8b70410bceb4497399d3d831037af57b` | unsure | 0.404 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `25525845ead2450d8d69d9d7affc21dd` | unsure | 0.404 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ea23b0b44015440b86d22f86274372ce` | unsure | 0.404 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9dc1bdd0be8146429296b6ac94785fd1` | unsure | 0.404 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9f1b4c32bdf04948b5e5b681febceb74` | unsure | 0.404 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `93c4a4d0cf5c438f950710d27578c143` | unsure | 0.404 |  |
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
  "content_id": "a0c6ca99da044562928088a5194c1dc9",
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
  "content_id": "4f39a45408d74044b46a7847063b6683",
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
  "content_id": "5aa38f6b9e734e7ba77371caf69b9aa6",
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
  "content_id": "20b19f27fe664dd78abf63b8468b8d0d",
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
  "content_id": "13c4c349bd6c486080eedeab515b3d4f",
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
  "content_id": "b2dd355f752741cda3e927fdfc130000",
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
  "content_id": "745328462c5d4574a9570a867896991c",
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
  "content_id": "335635debcc94cad9e64638699940760",
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
  "content_id": "641492fb0906467dbe05adad006123a4",
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
  "content_id": "7fa7144f363f4e74a8c75c4acfb20f5a",
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
  "content_id": "024d8398437c4a2ab20f75a7366092f4",
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
  "content_id": "9bd2e958c37541268505002b9245ac87",
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
  "content_id": "47ca5f01a7cb40afaf2a5e2dacef1944",
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
  "content_id": "e1ab64a3556347a09861e7057b1b4617",
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
  "content_id": "84698f6b9b7145c0a54712b1b4d24e28",
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
  "content_id": "902d0f5ba758420da0e15ba038098699",
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
  "content_id": "2bf24cb41af04421950a381ca20d278c",
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
  "content_id": "b877208578b743878d52a6f58ac2a4e9",
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
  "content_id": "fe1d73920bfa40d2ae29a29b8d74f4a9",
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
  "content_id": "ecadf13c098a43eaad49a61c9954d4df",
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
  "content_id": "1ce00ca5b97141a0bc04c764fb2bb75e",
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
  "content_id": "7bf777431d9346b9904f82ee12ad3fc3",
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
  "content_id": "056f4b0b916f4ee5af20f93fae170d96",
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
  "content_id": "761bdea098c24008b7f02a2a693479d0",
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
  "status": 400,
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
  "status": 200,
  "content_id": "87012512992940abb4b5be9cf7a878c6",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.3962,
  "model_score": 0.0,
  "style_score": 0.65,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "41737d541bf84e5cace0e5923a55796f",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.4781,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We cannot confidently tell whether this text was written by a person or generated by AI. No accusation should be made from this result.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "05b683a9c9fb4b69a290c43d511bfde1",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8412,
  "model_score": 0.9976,
  "style_score": 0.65,
  "label": "Our signals strongly suggest this text may be AI-generated. This is not proof, and the writer can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "2036bbd5ea3546019d0307b615dd9c46",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9983,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "Our signals strongly suggest this text may be AI-generated. This is not proof, and the writer can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c960fe83609c4e00a291e4f225d70790",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9485,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "Our signals strongly suggest this text may be AI-generated. This is not proof, and the writer can appeal this result.",
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
  "content_id": "7e333f5b3c2e4fa1a897a18e376d13c1",
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
  "content_id": "aa6c65a5ef3f41b68d567e7423744b84",
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
  "content_id": "27c5701aba634531aebe45e5a7c7b3a1",
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
  "content_id": "229fb30e3bac406da6509de41fb0b238",
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
  "content_id": "8b70410bceb4497399d3d831037af57b",
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
  "content_id": "25525845ead2450d8d69d9d7affc21dd",
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
  "content_id": "ea23b0b44015440b86d22f86274372ce",
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
  "content_id": "9dc1bdd0be8146429296b6ac94785fd1",
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
  "content_id": "9f1b4c32bdf04948b5e5b681febceb74",
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
  "content_id": "93c4a4d0cf5c438f950710d27578c143",
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
