import time

from web3 import Web3

from artifacts.abi_py.lending_pool_abi import LENDING_POOL_ABI
from query_state_lib.base.mappers.eth_call_mapper import EthCall
from query_state_lib.base.utils.encoder import encode_eth_call_data
from query_state_lib.client.client_querier import ClientQuerier

url = "https://bsc-dataseed1.binance.org/"

web3 = Web3(Web3.HTTPProvider(url))

client_querier = ClientQuerier(provider_url=url)

contract_address = Web3.toChecksumAddress('0x75DE5f7c91a89C16714017c7443eca20C7a8c295')

block_number = "latest"

number_query = 100

call_infos = []

get_balances = []
start = time.time()
data = encode_eth_call_data(abi=LENDING_POOL_ABI, fn_name="getReservesList", args=[])
for i in range(number_query):
    call1 = EthCall(to=contract_address, data=data, block_number=block_number, abi=LENDING_POOL_ABI,
                    fn_name="getReservesList", id=i)
    call_infos.append(call1)

# list_json_rpc = []
list_json_rpc = call_infos + get_balances

data_result = client_querier.sent_batch_to_provider(list_json_rpc, batch_size=2000, max_workers=4,timeout=200)

result = data_result[1].decode_result()

print(result)
"""
data result is a dict with key is id of EthJsonRpc and value is object EthJsonRpc with result
"""
end = time.time()

print(f"finish after {end - start}s")
