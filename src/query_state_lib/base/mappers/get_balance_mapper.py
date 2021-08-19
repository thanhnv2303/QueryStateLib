from typing import List

from query_state_lib.base.mappers.eth_json_rpc_mapper import generate_json_rpc, EthJsonRpc
from query_state_lib.base.utils.decoder import decode_eth_get_balance


class GetBalance(EthJsonRpc):
    def __init__(self, address="", block_number="latest", id=0):
        super().__init__()
        self.type = "eth_get_balance"
        self.address = address
        self.block_number = block_number
        self.id = id
        self.result = None

    def set_result(self, result):
        self.result = decode_eth_get_balance(result)
        return self.result


def generate_get_balance_json_rpc(get_balance_infos: List[GetBalance]):
    for get_balance in get_balance_infos:
        block = get_balance.block_number
        yield generate_json_rpc(
            method="eth_getBalance",
            params=[
                get_balance.address
                , hex(block) if isinstance(block, int) else block],
            request_id=get_balance.id
        )
