from ai_client import AIResponse, ProviderCall, generate_text


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
    return generate_text(messages, provider=provider)


category = classify_ticket(
    "The app crashes every time I open my documents.",
    provider=fake_provider_b,
)
print("Classified as:", category)
