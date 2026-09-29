from time import time

from ai_client import AIResponse, ProviderCall, generate_text
from exceptions.PermanentError import PermanentError
from exceptions.RateLimitError import RateLimitError
from exceptions.TransientError import TransientError


def fake_provider_a(messages: list[dict]) -> AIResponse:
    """Stands in for one real provider's SDK, adapted to our AIResponse shape."""
    return AIResponse(
        text="billing",
        stop_reason="complete",
        input_tokens=40,
        output_tokens=2,
    )


def fake_provider_b(messages: list[dict]) -> AIResponse:
    """Stands in for a different real provider, with a different response shape internally."""
    return AIResponse(
        text="billing2",
        stop_reason="complete",
        input_tokens=35,
        output_tokens=2,
    )

def call_with_retries(operation, max_attempts: int = 3) -> str:
    """
    Calls `operation` (a zero-argument function that returns a string or
    raises TransientError / RateLimitError / PermanentError), retrying
    transient and rate-limit failures with exponential backoff.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except PermanentError:
            raise  # Retrying won't help; fail immediately.
        except (TransientError, RateLimitError) as error:
            if attempt == max_attempts:
                raise
            wait_seconds = 2 ** (attempt - 1) #Exponential backoff: 1s, 2s, 4s, ...
            print(
                f"Attempt {attempt} failed ({type(error).__name__}); "
                f"waiting {wait_seconds}s before retry."
            )
            time.sleep(wait_seconds)

    raise RuntimeError("Unreachable: loop always returns or raises above.")

def classify_ticket(ticket_text: str, provider: ProviderCall) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "Classify the ticket into exactly one category: billing, "
                "technical, account_access. Respond with only the category."
            ),
        },
        {"role": "user", "content": ticket_text},
    ]
    
    def attempt_classification() -> str:
        return call_with_retries(lambda: generate_text(messages, provider=provider))

    try:
        return attempt_classification()
    except (TransientError, RateLimitError):
        print("AI classification unavailable; falling back to default category.")
        return "unclassified"


category = classify_ticket(
    "The app crashes every time I open my documents.",
    provider=fake_provider_b,
)
print("Classified as:", category)
