import sys
import time
from abc import abstractmethod
from typing import Any, Callable, Optional, Sequence, Union

import jwt
from requests import Session
from requests_toolbelt import MultipartEncoder

from query_state_lib.client.moralis_client.exceptions import ServerConnectionError
from query_state_lib.client.moralis_client.moralis_http import HTTPClient
from query_state_lib.client.moralis_client.moralis_request import Request
from query_state_lib.client.moralis_client.resolver import HostResolver
from query_state_lib.client.moralis_client.moralis_response import Response
from query_state_lib.client.moralis_client.typings import Fields, Json


class BaseConnection:
    """Base connection to a specific ArangoDB database."""

    def __init__(
            self,
            host: str,
            _x_api_keys: Fields,
            host_resolver: HostResolver,
            sessions: Sequence[Session],
            http_client: HTTPClient,
            serializer: Callable[..., str],
            deserializer: Callable[[str], Any],
    ) -> None:
        self._url_prefix = host
        self._x_api_keys = _x_api_keys
        self._host_resolver = host_resolver
        self._sessions = sessions
        self._http = http_client
        self._serializer = serializer
        self._deserializer = deserializer

    def serialize(self, obj: Any) -> str:
        """Serialize the given object.

        :param obj: JSON object to serialize.
        :type obj: str | bool | int | float | list | dict | None
        :return: Serialized string.
        :rtype: str
        """
        return self._serializer(obj)

    def deserialize(self, string: str) -> Any:
        """De-serialize the string and return the object.

        :param string: String to de-serialize.
        :type string: str
        :return: De-serialized JSON object.
        :rtype: str | bool | int | float | list | dict | None
        """
        try:
            return self._deserializer(string)
        except (ValueError, TypeError):
            return string

    def prep_response(self, resp: Response, deserialize: bool = True) -> Response:
        """Populate the response with details and return it.

        :param deserialize: Deserialize the response body.
        :type deserialize: bool
        :param resp: HTTP response.
        :type resp: arango.response.Response
        :return: HTTP response.
        :rtype: arango.response.Response
        """
        if deserialize:
            resp.body = self.deserialize(resp.raw_body)
            if isinstance(resp.body, dict):
                resp.error_code = resp.body.get("errorNum")
                resp.error_message = resp.body.get("errorMessage")
        else:
            resp.body = resp.raw_body

        http_ok = 200 <= resp.status_code < 300
        resp.is_success = http_ok and resp.error_code is None
        return resp

    def prep_bulk_err_response(self, parent_response: Response, body: Json) -> Response:
        """Build and return a bulk error response.

        :param parent_response: Parent response.
        :type parent_response: arango.response.Response
        :param body: Error response body.
        :type body: dict
        :return: Child bulk error response.
        :rtype: arango.response.Response
        """
        resp = Response(
            method=parent_response.method,
            url=parent_response.url,
            headers=parent_response.headers,
            status_code=parent_response.status_code,
            status_text=parent_response.status_text,
            raw_body=self.serialize(body),
        )
        resp.body = body
        resp.error_code = body["errorNum"]
        resp.error_message = body["errorMessage"]
        resp.is_success = False
        return resp

    def normalize_data(self, data: Any) -> Union[str, MultipartEncoder, None]:
        """Normalize request data.

        :param data: Request data.
        :type data: str | MultipartEncoder | None
        :return: Normalized data.
        :rtype: str | MultipartEncoder | None
        """
        if data is None:
            return None
        elif isinstance(data, (str, MultipartEncoder)):
            return data
        else:
            return self.serialize(data)

    def ping(self) -> int:
        """Ping the next host to check if connection is established.

        :return: Response status code.
        :rtype: int
        """
        request = Request(method="get", endpoint="/dateToBlock")
        resp = self.send_request(request)
        if resp.status_code in {401, 403}:
            raise ServerConnectionError(f"bad api key ")
        if not resp.is_success:  # pragma: no cover
            raise ServerConnectionError(resp.error_message or "bad server response")
        return resp.status_code

    @abstractmethod
    def send_request(self, request: Request) -> Response:  # pragma: no cover
        """Send an HTTP request to ArangoDB server.

        :param request: HTTP request.
        :type request: arango.request.Request
        :return: HTTP response.
        :rtype: arango.response.Response
        """
        raise NotImplementedError


class BasicConnection(BaseConnection):
    """Connection to specific Moralis using basic authentication.
    :param host
    :type host: str
    :param x_api_keys: list Api key for moralis
    :type x_api_keys: [str]
    :param host_resolver: Host resolver (used for clusters).
    :type host_resolver: arango.resolver.HostResolver
    :param sessions: HTTP session objects per host.
    :type sessions: [requests.Session]\
    :param http_client: User-defined HTTP client.
    :type http_client: arango.http.HTTPClient
    """

    def __init__(
            self,
            host: str,
            x_api_keys: Fields,
            host_resolver: HostResolver,
            sessions: Sequence[Session],
            http_client: HTTPClient,
            serializer: Callable[..., str],
            deserializer: Callable[[str], Any],
    ) -> None:
        super().__init__(
            host,
            x_api_keys,
            host_resolver,
            sessions,
            http_client,
            serializer,
            deserializer,
        )

    def send_request(self, request: Request) -> Response:
        """Send an HTTP request to Moralis server.

        :param request: HTTP request.
        :type request: moralis_services.request.Request
        :return: HTTP response.
        :rtype: moralis_services.response.Response
        """
        host_index = self._host_resolver.get_host_index()
        x_api_key = self._x_api_keys[host_index]
        request.headers["X-API-Key"] = x_api_key

        resp = self._http.send_request(
            session=self._sessions[host_index],
            method=request.method,
            url=self._url_prefix + request.endpoint,
            params=request.params,
            data=self.normalize_data(request.data),
            headers=request.headers,
        )
        return self.prep_response(resp, request.deserialize)
