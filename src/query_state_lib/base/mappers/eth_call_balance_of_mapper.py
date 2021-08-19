from typing import List

from query_state_lib.base.mappers.eth_call_mapper import EthCall, generate_eth_call_json_rpc
from query_state_lib.base.utils.decoder import decode_eth_call_balance_of
from query_state_lib.base.utils.encoder import encode_eth_call_balance_of


class EthCallBalanceOf(EthCall):
    def __init__(self, contract_address="", address="", block_number="", id=0):
        data = encode_eth_call_balance_of(address)
        super().__init__(to=contract_address, data=data, block_number=block_number, id=id)
        self.type = "eth_call_balance_of"

    def set_result(self, result):
        self.result = decode_eth_call_balance_of(result)
        return self.result


def generate_eth_call_balance_of_json_rpc(call_infos: List[EthCallBalanceOf]):
    return generate_eth_call_json_rpc(call_infos)
