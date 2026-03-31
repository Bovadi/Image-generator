import os
from openai import OpenAI

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client


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
