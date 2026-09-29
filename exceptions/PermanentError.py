class PermanentError(Exception):
    """A failure that will happen again no matter how many times we retry."""