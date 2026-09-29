class TransientError(Exception):
    """A temporary failure that's likely to succeed if retried."""