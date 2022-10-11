import time

from web3 import Web3

from _test.CREAM_LENS_ABI import CREAM_LENS_ABI
from query_state_lib.base.mappers.eth_call_mapper import EthCall
from query_state_lib.base.utils.encoder import encode_eth_call_data
from query_state_lib.client.client_querier import ClientQuerier

url = "https://bsc-dataseed1.binance.org/"

client_querier = ClientQuerier(provider_url=url)

contract_address = Web3.toChecksumAddress('0x1a014ffe0cd187a298a7e79ba5ab05538686ea4a')

tokens = ['0x4cB7F1f4aD7a6b53802589Af3B90612C1674Fec4']

w3 = Web3(Web3.HTTPProvider(url))

block_number = "latest"

number_query = 100

call_infos = []

get_balances = []
start = time.time()
data = encode_eth_call_data(abi=CREAM_LENS_ABI, fn_name="cTokenMetadataAll", args=[tokens])

call1 = EthCall(to=contract_address, data=data, block_number=block_number, abi=CREAM_LENS_ABI,
                fn_name="cTokenMetadataAll", id=1)
call_infos.append(call1)
data_result = client_querier.sent_batch_to_provider(call_infos, batch_size=2000, max_workers=4, timeout=200)

result = data_result[1].decode_result()

print(result)
