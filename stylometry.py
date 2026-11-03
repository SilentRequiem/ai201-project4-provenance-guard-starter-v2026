"""
Signal two: a simple stylometry signal.

It measures the shape of the writing instead of its meaning. Higher scores
mean "more AI-like" so it points in the same direction as detector.model_signal.
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into rough sentences."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words with punctuation removed."""
    return re.findall(r"[a-z0-9']+", text.lower())


def _clamp(value: float) -> float:
    return min(max(value, 0.0), 1.0)


def sentence_length_spread(text: str) -> float:
    """
    Coefficient of variation for sentence lengths.

    Higher means sentence lengths vary more. Human writing often varies more,
    while generated prose often stays closer to a regular sentence length.
    """
    lengths = [len(words(sentence)) for sentence in sentences(text)]
    lengths = [length for length in lengths if length > 0]

    if len(lengths) < 2:
        return 0.0

    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.0

    return round(statistics.stdev(lengths) / mean, 4)


def type_token_ratio(text: str) -> float:
    """Unique words divided by total words."""
    tokens = words(text)
    if not tokens:
        return 0.0
    return round(len(set(tokens)) / len(tokens), 4)


def punctuation_density(text: str) -> float:
    """
    Expressive punctuation marks per word.

    This counts punctuation that tends to vary by writer rather than ordinary
    full stops: commas, semicolons, colons, question marks, exclamation marks,
    dashes, and parentheses.
    """
    tokens = words(text)
    if not tokens:
        return 0.0

    marks = re.findall(r"[,;:!?()\-—]", text)
    return round(len(marks) / len(tokens), 4)


def style_signal(text: str) -> float:
    """
    Return a 0-1 score where higher means more AI-like.

    The three raw measures use different scales, so each is normalized first.
    Lower sentence-length spread, lower vocabulary variety, and lower expressive
    punctuation all push the score upward.
    """
    spread = sentence_length_spread(text)
    ttr = type_token_ratio(text)
    punct = punctuation_density(text)

    spread_human = _clamp(spread / 0.65)
    vocabulary_human = _clamp((ttr - 0.35) / 0.45)
    punctuation_human = _clamp(punct / 0.15)

    ai_spread = 1.0 - spread_human
    ai_vocabulary = 1.0 - vocabulary_human
    ai_punctuation = 1.0 - punctuation_human

    score = (
        0.50 * ai_spread
        + 0.35 * ai_vocabulary
        + 0.15 * ai_punctuation
    )
    return round(_clamp(score), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
