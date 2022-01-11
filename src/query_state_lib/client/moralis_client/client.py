from json import dumps, loads
from typing import Optional, Sequence, Callable, Any

from query_state_lib.client.moralis_client.connection import BasicConnection
from query_state_lib.client.moralis_client.examples import LIQUIDATE_EVENT
from query_state_lib.client.moralis_client.moralis_http import HTTPClient, DefaultHTTPClient
from query_state_lib.client.moralis_client.moralis_request import Request
from query_state_lib.client.moralis_client.resolver import HostResolver, SingleHostResolver, RandomHostResolver, \
    RoundRobinHostResolver


class MoralisClient:
    def __init__(self, x_api_keys, base_url="https://deep-index.moralis.io/api/v2",
                 host_resolver: str = "roundrobin",
                 http_client: Optional[HTTPClient] = None,
                 serializer: Callable[..., str] = lambda x: dumps(x),
                 deserializer: Callable[[str], Any] = lambda x: loads(x)):
        self.base_url = base_url

        if isinstance(x_api_keys, str):
            self._x_api_keys = [host.strip("/") for host in x_api_keys.split(",")]
        else:
            self._x_api_keys = [host.strip("/") for host in x_api_keys]

        num_x_api_key = len(self._x_api_keys)
        self._host_resolver: HostResolver

        if num_x_api_key == 1:
            self._host_resolver = SingleHostResolver(x_api_key=num_x_api_key)
        elif host_resolver == "random":
            self._host_resolver = RandomHostResolver(num_x_api_key)
        else:
            self._host_resolver = RoundRobinHostResolver(num_x_api_key)
        self._http = http_client or DefaultHTTPClient()
        self._serializer = serializer
        self._deserializer = deserializer
        self._sessions = [self._http.create_session(h) for h in self._x_api_keys]

        self.connection = BasicConnection(
            host=self.base_url,
            x_api_keys=x_api_keys,
            host_resolver=self._host_resolver,
            sessions=self._sessions,
            http_client=self._http,
            serializer=self._serializer,
            deserializer=self._deserializer,
        )

    def __repr__(self) -> str:
        return f"<ArangoClient {','.join(self._x_api_keys)}>"

    def close(self) -> None:  # pragma: no cover
        """Close HTTP sessions."""
        for session in self._sessions:
            session.close()

    @property
    def x_api_keys(self) -> Sequence[str]:
        """Return the list of ArangoDB host URLs.

        :return: List of ArangoDB host URLs.
        :rtype: [str]
        """
        return self._x_api_keys

    def ping(self):
        return self.connection.ping()

    def date_to_block(self, chain="eth", date=None):
        endpoint = f"/dateToBlock"
        params = {
            "chain": chain
        }
        if date:
            params["date"] = date

        request = Request(method="get", endpoint=endpoint, params=params)
        res = self.connection.send_request(request)
        return res.body

    def get_token_price(self, address, chain="eth", to_block=None, exchange=None):
        endpoint = f"/erc20/{address}/price"
        params = {
            "chain": chain
        }
        if to_block:
            params["to_block"] = to_block
        if exchange:
            params["exchange"] = exchange

        request = Request(method="get", endpoint=endpoint, params=params)
        res = self.connection.send_request(request)
        return res.body

    def get_token_metadata(self, addresses, chain="eth"):
        endpoint = f"/erc20/metadata"
        params = {
            "chain": chain
        }
        if addresses:
            params["addresses"] = addresses

        request = Request(method="get", endpoint=endpoint, params=params)
        res = self.connection.send_request(request)
        return res.body

    def get_token_balance(self, address, chain="eth", to_block=None, token_addresses=[]):
        endpoint = f"/{address}/erc20"
        params = {
            "chain": chain
        }
        if to_block:
            params["to_block"] = to_block
        if token_addresses:
            params["token_addresses"] = token_addresses

        request = Request(method="get", endpoint=endpoint, params=params)
        res = self.connection.send_request(request)
        return res.body

    def get_address_transfers(self, address,
                              chain="eth",
                              from_block=None,
                              to_block=None,
                              from_date=None,
                              to_date=None,
                              offset=None,
                              limit=None,
                              ):
        endpoint = f"/{address}/erc20/transfers"
        params = {
            "chain": chain
        }
        if from_block:
            params["from_block"] = from_block
        if to_block:
            params["to_block"] = to_block
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit

        request = Request(method="get", endpoint=endpoint, params=params)
        res = self.connection.send_request(request)
        return res.body

    def get_address_logs(self, address, chain="eth",
                         block_number=None,
                         from_block=None,
                         to_block=None,
                         from_date=None,
                         to_date=None,
                         topic0=None,
                         topic1=None,
                         topic2=None,
                         topic3=None,
                         offset=None,
                         limit=None,
                         ):
        endpoint = f"/{address}/logs"
        params = {
            "chain": chain
        }
        if block_number:
            params["block_number"] = block_number
        if from_block:
            params["from_block"] = from_block
        if to_block:
            params["to_block"] = to_block
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        if topic0:
            params["topic0"] = topic0
        if topic1:
            params["topic1"] = topic1
        if topic2:
            params["topic2"] = topic2
        if topic3:
            params["topic3"] = topic3
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit

        request = Request(method="get", endpoint=endpoint, params=params)
        res = self.connection.send_request(request)
        return res.body

    def get_address_event_by_topic(self, address,
                                   topic,
                                   event_abi,
                                   chain="eth",
                                   block_number=None,
                                   from_block=None,
                                   to_block=None,
                                   from_date=None,
                                   to_date=None,
                                   offset=None,
                                   limit=None,
                                   ):
        endpoint = f"/{address}/events"
        params = {
            "chain": chain,
            "topic": topic
        }
        if block_number:
            params["block_number"] = block_number
        if from_block:
            params["from_block"] = from_block
        if to_block:
            params["to_block"] = to_block
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit

        request = Request(method="post", endpoint=endpoint, params=params, data=event_abi)
        res = self.connection.send_request(request)
        return res.body
