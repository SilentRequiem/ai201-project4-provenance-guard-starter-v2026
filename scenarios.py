"""
Unit 8 evaluation cases, matched to the unchanged criteria.md.

Human samples below come from the CodePath staff practice set used in Unit 6.
They are course examples, not claimed to be the student's original writing.
For the strongest false-positive test, replace them with 10 real paragraphs
written by you before running the final evaluation.

AI samples in this file were generated with AI assistance for testing.
No result is assumed or hardcoded. run_eval.py sends every input to the service.
"""

HUMAN_SAMPLES = [
    "Pulled the splits from the last five editions. The winning time has moved by 40 seconds total in ten years, but the 100th-place time is four minutes faster. The depth changed, the front didn't.",
    "I tracked sleep against session quality for eleven weeks. Under seven hours the next day's intervals were 6-8 seconds per mile slower, every time bar one. Small sample, one runner, but it's consistent enough that I've stopped scheduling hard days after late shifts.",
    "The club championship scoring changed in 2019 from top-6 to top-10. Since then our B team has finished above the A team twice. That's not depth improving, it's the scoring rewarding turnout.",
    "Everyone blames the hill at 18 miles. I split the field into people who ran the first half under 1:45 and over, and the slowdown after 18 was almost identical for both groups. If the hill were the problem the fast starters would fall apart harder.",
    "Carbon plates aren't the whole story. My times dropped 2% in the shoes and another 2% the following year in the same pair, when the only thing that changed was going from 35 to 50 miles a week.",
    "Checked the entry lists. 41% of this year's field have never run the distance before, against 26% five years ago. That's why the finish-line photos look different, not because standards dropped.",
    "Ran the same loop in 4C and in 24C within a fortnight, same effort by heart rate. 90 seconds slower in the heat over six miles. People keep saying heat costs you 'a bit' and it's more than that.",
    "Went back through the club results going back to 2012. Every single year the number of people who enter the spring marathon and don't start it sits between 18 and 23 percent. It's not a bad-luck year, it's the base rate.",
    "The 10K route was remeasured in 2021 and came out 60 metres long. Everyone comparing PBs from before and after that is comparing two different races, which is about 12 seconds at club pace.",
    "Three of us ran the same session on the same day, different shoes, within 10 seconds of each other over 5 miles. I'm not saying shoes do nothing, but whatever they do was smaller than the noise between three people.",
]

AI_SAMPLES = [
    "The implementation of the proposed framework requires careful consideration of several key factors. The system must handle different inputs consistently while providing reliable results. Additionally, overall performance depends on a number of important variables that should be evaluated carefully.",
    "In today's rapidly changing digital environment, organizations must prioritize effective communication and seamless collaboration. By adopting innovative approaches and leveraging advanced technologies, teams can drive meaningful outcomes and improve long-term operational efficiency.",
    "Healthy habits are essential for maintaining overall well-being. A balanced routine should include adequate sleep, regular physical activity, and thoughtful nutrition. These elements work together to promote physical health and support sustained personal growth.",
    "Education plays an important role in helping people achieve their potential. A supportive learning environment encourages curiosity, critical thinking, and consistent improvement. By connecting theory with practical application, students can build useful knowledge and strengthen their skills.",
    "Effective project management requires clear objectives, realistic timelines, and transparent communication. Teams should evaluate progress regularly, identify potential challenges, and adjust strategies when necessary. This proactive approach can help organizations deliver projects successfully.",
]

COVERAGE_SAMPLES = [
    AI_SAMPLES[0],
    AI_SAMPLES[1],
    HUMAN_SAMPLES[1],
    HUMAN_SAMPLES[3],
    "Wait. What? No. No. That wasn't the plan! I turned the corner and the dog was staring at me, soaked in rain, with one of my socks hanging from its mouth.",
    "Quixotic lanterns flickered beneath an unseasonably violet sky. Baffled, I traced the salt-crusted hieroglyphs along the brass hinge before the bell rang twice.",
]

APPEAL_SAMPLES = [
    AI_SAMPLES[0],
    AI_SAMPLES[1],
    HUMAN_SAMPLES[0],
    HUMAN_SAMPLES[1],
    HUMAN_SAMPLES[2],
]

BAD_BODIES = [
    {"creator_id": "eval_bad_missing"},
    {"text": "", "creator_id": "eval_bad_empty"},
    {"text": None, "creator_id": "eval_bad_null"},
    {"text": 12345, "creator_id": "eval_bad_type"},
    {"text": "longword " * 2501, "creator_id": "eval_bad_huge"},
]

SCENARIOS = [
    {
        "criterion": 1,
        "name": "false positives on 10 human samples",
        "kind": "human",
        "texts": HUMAN_SAMPLES,
        "target": "at most 1 of 10 high-confidence AI",
    },
    {
        "criterion": 2,
        "name": "average AI versus human score spread",
        "kind": "score_spread",
        "human": HUMAN_SAMPLES[:5],
        "ai": AI_SAMPLES,
        "target": "AI mean minus human mean at least 0.25",
    },
    {
        "criterion": 3,
        "name": "three label variants reachable in six samples",
        "kind": "coverage",
        "texts": COVERAGE_SAMPLES,
        "target": "all three guesses in at most 6 inputs",
    },
    {
        "criterion": 4,
        "name": "five valid appeals are logged",
        "kind": "appeal",
        "texts": APPEAL_SAMPLES,
        "target": "5 of 5 under_review and logged",
    },
    {
        "criterion": 5,
        "name": "five invalid requests rejected safely",
        "kind": "bad_input",
        "bodies": BAD_BODIES,
        "target": "5 of 5 rejected with 4xx, no 500",
    },
]


def validate() -> list[str]:
    problems = []
    if len(SCENARIOS) != 5:
        problems.append("Expected exactly five scenarios.")
    if [s["criterion"] for s in SCENARIOS] != [1, 2, 3, 4, 5]:
        problems.append("Scenario criterion numbers must be 1 through 5.")
    for scenario in SCENARIOS:
        kind = scenario["kind"]
        cases = scenario.get("texts") or scenario.get("bodies") or []
        if kind == "score_spread":
            cases = scenario.get("human", []) + scenario.get("ai", [])
        if not cases:
            problems.append(f"{scenario['name']}: no cases")
        if kind == "human" and len(cases) != 10:
            problems.append("Criterion 1 requires 10 samples.")
        if kind == "coverage" and len(cases) > 6:
            problems.append("Criterion 3 allows at most six samples.")
        if kind == "appeal" and len(cases) != 5:
            problems.append("Criterion 4 requires five appeal cases.")
        if kind == "bad_input" and len(cases) != 5:
            problems.append("Criterion 5 requires five bad inputs.")
    return problems


if __name__ == "__main__":
    issues = validate()
    print("Scenarios valid." if not issues else "\n".join(issues))
