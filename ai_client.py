from dataclasses import dataclass
from typing import Callable


@dataclass
class AIResponse:
    text: str
    stop_reason: str
    input_tokens: int
    output_tokens: int


# A provider function takes a list of role-tagged messages and returns
# an AIResponse. Whatever real SDK we wire in later, GPT, Claude, Gemini,
# or any other, gets adapted to match this exact shape, once, in one place.
ProviderCall = Callable[[list[dict]], AIResponse]


def generate_text(messages: list[dict], provider: ProviderCall) -> str:
    """
    The one function the rest of the codebase is allowed to call.
    No other file should import an SDK directly.
    """
    response = provider(messages)

    if response.stop_reason != "complete":
        raise ValueError(
            f"Generation did not complete (stop_reason={response.stop_reason!r})"
        )

    return response.text