class AccessDenied(Exception):
    """Connection was denied."""
    pass


class ConnectionClosed(Exception):
    """Connection was closed."""
    pass


class UnhandledResponse(Exception):
    """Received unknown response."""
    pass


class UnknownMethod(Exception):
    """Unknown method."""
    pass
