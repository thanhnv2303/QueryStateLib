from typing import List

from query_state_lib.base.mappers.eth_json_rpc_mapper import generate_json_rpc, EthJsonRpc
from query_state_lib.base.utils.decoder import decode_eth_call_data


class EthCall(EthJsonRpc):
    def __init__(self, to="", data="", block_number=0, abi=None, fn_name=None, id=0):
        super().__init__()
        self.type = "eth_call"
        self.to = to
        self.data = data
        self.block_number = block_number
        self.id = id
        self.abi = abi
        self.fn_name = fn_name

    def set_abi(self, abi):
        self.abi = abi

    def set_fn_name(self, fn_name):
        self.fn_name = fn_name

    def decode_result(self):
        if not self.abi:
            raise Exception("Have to set abi before decode eth call result")
        if not self.fn_name:
            raise Exception("Have to set function name (fn_name) before decode eth call result")
        self.result = decode_eth_call_data(self.abi, self.fn_name, self.result)

        return self.result


def generate_eth_call_json_rpc(call_infos: List[EthCall]):
    for call_info in call_infos:
        block = call_info.block_number
        yield generate_json_rpc(
            method="eth_call",
            params=[{
                "to": call_info.to,
                "data": call_info.data
            }, hex(block) if isinstance(block, int) else block],
            request_id=call_info.id
        )
