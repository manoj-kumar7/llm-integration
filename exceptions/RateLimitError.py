class RateLimitError(Exception):
    """We've sent too many requests; retrying immediately won't help."""