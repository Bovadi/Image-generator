import os
import re
from openai import OpenAI

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client


_PII_PATTERNS = [
    (r"(\+?1?\s?)?(\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4})", "555-000-0000"),       # phone
    (r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", "student@example.com"),  # email
    (r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b", "XXX-XX-XXXX"),                            # SSN
    (r"\b(0?[1-9]|1[0-2])[\/\-](0?[1-9]|[12]\d|3[01])[\/\-](\d{2}|\d{4})\b", "a date"), # date
    (r"\b\d{6,}\b", "XXXXXXXX"),                                                     # ID numbers
]

_SAFE_WORDS = {
    "monday","tuesday","wednesday","thursday","friday","saturday","sunday",
    "january","february","march","april","june","july","august","september",
    "october","november","december","south","north","east","west",
}


def scrub_pii(text: str) -> tuple[str, list[str]]:
    """
    Remove PII from text. Returns (scrubbed_text, list_of_detected_types).
    Called before moderation and before prompt building.
    """
    scrubbed = text
    detected = []

    for pattern, replacement in _PII_PATTERNS:
        if re.search(pattern, scrubbed):
            detected.append(pattern)
        scrubbed = re.sub(pattern, replacement, scrubbed)

    # Proper names: two+ capitalized words not at sentence start
    def replace_name(match: re.Match) -> str:
        words = match.group(0).lower().split()
        if any(w in _SAFE_WORDS for w in words):
            return match.group(0)
        detected.append("name")
        return "the student"

    scrubbed = re.sub(
        r"(?<![.!?\n])\b([A-Z][a-z]{1,15})(\s[A-Z][a-z]{1,15}){1,2}\b",
        replace_name,
        scrubbed,
    )

    return scrubbed, detected


class ModerationError(Exception):
    """Raised when a scenario is flagged by the moderation API."""
    def __init__(self, categories: list[str]):
        self.categories = categories
        super().__init__(f"Scenario flagged for: {', '.join(categories)}")


def check_scenario(scenario: str) -> None:
    """
    Run scenario text through OpenAI's moderation API.
    Raises ModerationError if the content is flagged.
    Does nothing if the content is safe.
    """
    response = _get_client().moderations.create(
        model="omni-moderation-latest",
        input=scenario,
    )
    result = response.results[0]
    if result.flagged:
        flagged_categories = [
            category
            for category, flagged in result.categories.model_dump().items()
            if flagged
        ]
        raise ModerationError(flagged_categories)
