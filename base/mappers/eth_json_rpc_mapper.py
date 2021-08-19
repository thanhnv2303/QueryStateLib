from typing import List


class EthJsonRpc:
    def __init__(self, method="", params=None, id=0):
        self.id = id
        self.type = "eth_json_rpc"
        self.method = method
        self.params = params
        self.result = None
        self.decoded = False

    def set_result(self, result):
        self.result = result

    def decode_result(self):
        return self.result


def generate_eth_json_rpc(call_infos: List[EthJsonRpc]):
    for call_info in call_infos:
        yield generate_json_rpc(
            method=call_info.method,
            params=call_info.params,
            request_id=call_info.id
        )


def generate_json_rpc(method, params, request_id=1):
    return {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': request_id,
    }
