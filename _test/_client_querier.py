import time

from query_state_lib.base.executors.batch_work_executor import RETRY_EXCEPTIONS
from web3 import Web3

from query_state_lib.base.mappers.eth_call_balance_of_mapper import EthCallBalanceOf
from query_state_lib.client.client_querier import ClientQuerier

url = "https://speedy-nodes-nyc.moralis.io/51ed809fc830640c534fe746/bsc/mainnet/archive"
url = "https://speedy-nodes-nyc.moralis.io/51ed809fc830640c534fe746/bsc/mainnet/archive"
url = "https://speedy-nodes-nyc.moralis.io/892851844778bc31eb9f6b6e/bsc/mainnet/archive"
url = "https://speedy-nodes-nyc.moralis.io/bf2c665d233974e6df7cb109/bsc/mainnet/archive"
url = "https://nd-384-319-366.p2pify.com/7e49b20f53222da5f0b4517cd1da43ef"
url = "https://nd-548-567-990.p2pify.com/cbbfddee2b688acec746b6d0b4fdac3c"
# url = "https://bold-withered-smoke.bsc.quiknode.pro/0c905a0c5d236a477e35c4727969ab3acda5a962/"
# url = "http://localhost:1337"
client_querier = ClientQuerier(provider_url=url)

contract_address = Web3.toChecksumAddress('0x334b3ecb4dca3593bccc3c7ebd1a1c1d1780fbf1')
block_number = 14297268
block_number = 14609572

# w3 = Web3(Web3.HTTPProvider(url))
# block_number = w3.eth.block_number-100

address = "0x0e6ddcf8f1bf0879bdd50fb314757fea7b71fa9e"

number_query = 20

call_infos = []

get_balances = []
start = time.time()
for i in range(number_query):
    call1 = EthCallBalanceOf(contract_address, address, block_number + i, id=f"{address}_{block_number + i}")
    call_infos.append(call1)

    # get_balance = GetBalance(address, block_number + i, id=number_query + i)
    # get_balances.append(get_balance)

# list_json_rpc = []
list_json_rpc = call_infos + get_balances

data_result = client_querier.sent_batch_to_provider(list_json_rpc, batch_size=2000, max_workers=4, timeout=200,
                                                    max_retries=1,
                                                    retry_exceptions=RETRY_EXCEPTIONS)
num_err = 0
for key, data in data_result.items():
    balance = data.decode_result()
    if data.error:
        num_err += 1

    print(f"{key} - balance :{balance}")

print(f"err ratio {num_err / number_query * 100}")
# data_result = client_querier.sent_batch_to_state_querier(list_json_rpc)
"""
data result is a dict with key is id of EthJsonRpc and value is object EthJsonRpc with result
"""
end = time.time()

print(f"finish after {end - start}s")
