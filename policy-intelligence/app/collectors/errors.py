class CollectorError(Exception):
    """
    Base exception for collector failures.
    """

    def __init__(
        self,
        message: str,
        source_id: str | None = None,
        retryable: bool = False,
    ):
        super().__init__(message)

        self.message = message
        self.source_id = source_id
        self.retryable = retryable


class CollectorNetworkError(CollectorError):
    """
    Network/connection failure.
    """

    def __init__(
        self,
        message: str,
        source_id: str | None = None,
    ):
        super().__init__(
            message=message,
            source_id=source_id,
            retryable=True,
        )


class CollectorHTTPError(CollectorError):
    """
    HTTP-level failure.
    """

    def __init__(
        self,
        message: str,
        source_id: str | None = None,
        retryable: bool = False,
    ):
        super().__init__(
            message=message,
            source_id=source_id,
            retryable=retryable,
        )


class CollectorValidationError(CollectorError):
    """
    Invalid or unsupported response.
    """

    def __init__(
        self,
        message: str,
        source_id: str | None = None,
    ):
        super().__init__(
            message=message,
            source_id=source_id,
            retryable=False,
        )