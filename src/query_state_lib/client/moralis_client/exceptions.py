from typing import Optional

from query_state_lib.client.moralis_client.moralis_request import Request
from query_state_lib.client.moralis_client.moralis_response import Response


class MoralisError(Exception):
    """Base class for all exceptions in python-arango."""


class MoralisClientError(MoralisError):
    """Base class for errors originating from python-arango client.

    :param msg: Error message.
    :type msg: str

    :cvar source: Source of the error (always set to "client").
    :vartype source: str
    :ivar message: Error message.
    :vartype message: str
    """

    source = "client"

    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.message = msg
        self.error_message = None
        self.error_code = None
        self.url = None
        self.response = None
        self.request = None
        self.http_method = None
        self.http_code = None
        self.http_headers = None


class MoralisServerError(MoralisError):
    """Base class for errors originating from ArangoDB server.

    :param resp: HTTP response.
    :type resp: arango.response.Response
    :param msg: Error message override.
    :type msg: str

    :cvar source: Source of the error (always set to "server").
    :vartype source: str
    :ivar message: Exception message.
    :vartype message: str
    :ivar url: API URL.
    :vartype url: str
    :ivar response: HTTP response object.
    :vartype response: arango.response.Response
    :ivar request: HTTP request object.
    :vartype request: arango.request.Request
    :ivar http_method: HTTP method in lowercase (e.g. "post").
    :vartype http_method: str
    :ivar http_code: HTTP status code.
    :vartype http_code: int
    :ivar http_headers: Response headers.
    :vartype http_headers: dict
    :ivar error_code: Error code from ArangoDB server.
    :vartype error_code: int
    :ivar error_message: Raw error message from ArangoDB server.
    :vartype error_message: str
    """

    source = "server"

    def __init__(
            self, resp: Response, request: Request, msg: Optional[str] = None
    ) -> None:
        msg = msg or resp.error_message or resp.status_text
        self.error_message = resp.error_message
        self.error_code = resp.error_code
        if self.error_code is not None:
            msg = f"[HTTP {resp.status_code}][ERR {self.error_code}] {msg}"
        else:
            msg = f"[HTTP {resp.status_code}] {msg}"
            self.error_code = resp.status_code
        super().__init__(msg)
        self.message = msg
        self.url = resp.url
        self.response = resp
        self.request = request
        self.http_method = resp.method
        self.http_code = resp.status_code
        self.http_headers = resp.headers


#####################
# Server Exceptions #
#####################


class ServerConnectionError(MoralisClientError):
    """Failed to connect to ArangoDB server."""


class ServerEngineError(MoralisServerError):
    """Failed to retrieve database engine."""


class ServerVersionError(MoralisServerError):
    """Failed to retrieve server version."""


class ServerDetailsError(MoralisServerError):
    """Failed to retrieve server details."""


class ServerStatusError(MoralisServerError):
    """Failed to retrieve server status."""


class ServerTimeError(MoralisServerError):
    """Failed to retrieve server system time."""


class ServerEchoError(MoralisServerError):
    """Failed to retrieve details on last request."""


class ServerShutdownError(MoralisServerError):
    """Failed to initiate shutdown sequence."""


class ServerRunTestsError(MoralisServerError):
    """Failed to execute server tests."""


class ServerRequiredDBVersionError(MoralisServerError):
    """Failed to retrieve server target version."""


class ServerReadLogError(MoralisServerError):
    """Failed to retrieve global log."""


class ServerLogLevelError(MoralisServerError):
    """Failed to retrieve server log levels."""


class ServerLogLevelSetError(MoralisServerError):
    """Failed to set server log levels."""


class ServerReloadRoutingError(MoralisServerError):
    """Failed to reload routing details."""


class ServerStatisticsError(MoralisServerError):
    """Failed to retrieve server statistics."""


class ServerMetricsError(MoralisServerError):
    """Failed to retrieve server metrics."""


class ServerRoleError(MoralisServerError):
    """Failed to retrieve server role in a cluster."""


class ServerTLSError(MoralisServerError):
    """Failed to retrieve TLS data."""


class ServerTLSReloadError(MoralisServerError):
    """Failed to reload TLS."""


class ServerEncryptionError(MoralisServerError):
    """Failed to reload user-defined encryption keys."""
