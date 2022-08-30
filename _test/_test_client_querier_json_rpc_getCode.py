import time

from web3 import Web3

from query_state_lib.base.mappers.eth_json_rpc_mapper import EthJsonRpc
from query_state_lib.client.client_querier import ClientQuerier

url = "https://speedy-nodes-nyc.moralis.io/51ed809fc830640c534fe746/bsc/mainnet/archive"
url = "https://nd-384-319-366.p2pify.com/7e49b20f53222da5f0b4517cd1da43ef"
url = "https://nd-384-319-366.p2pify.com/7e49b20f53222da5f0b4517cd1da43ef"
url = "https://bsc-dataseed1.binance.org/"

web3 = Web3(Web3.HTTPProvider(url))

client_querier = ClientQuerier(provider_url=url)

contract_address = Web3.toChecksumAddress('0x75DE5f7c91a89C16714017c7443eca20C7a8c295')
param1 = ["0x75DE5f7c91a89C16714017c7443eca20C7a8c295", "latest"]
param2 = ["0x295e26495CEF6F69dFA69911d9D8e4F3bBadB89B", "latest"]

call1 = EthJsonRpc(method="eth_getCode", params=param1, id=1)
call2 = EthJsonRpc(method="eth_getCode", params=param2, id=3)

# list_json_rpc = []
list_json_rpc = [call1, call2]

data_result = client_querier.sent_batch_to_provider(list_json_rpc, batch_size=2000, max_workers=4, timeout=200)

result = data_result[1].decode_result()
print(result)
"""
data result is a dict with key is id of EthJsonRpc and value is object EthJsonRpc with result
"""

