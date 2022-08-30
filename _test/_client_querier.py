import time

from web3 import Web3

from query_state_lib.base.executors.batch_work_executor import RETRY_EXCEPTIONS
from query_state_lib.base.mappers.eth_call_balance_of_mapper import EthCallBalanceOf
from query_state_lib.client.client_querier import ClientQuerier

url = "https://bsc-dataseed1.binance.org/"

client_querier = ClientQuerier(provider_url=url)

contract_address = Web3.toChecksumAddress('0x2170Ed0880ac9A755fd29B2688956BD959F933F8')


w3 = Web3(Web3.HTTPProvider(url))
block_number = "latest"

address = "0x35a934af4e722f5282ec2b12c0956f3c1ed25c93"

number_query = 20

call_infos = []

get_balances = []
start = time.time()
for i in range(number_query):
    call1 = EthCallBalanceOf(contract_address, address, block_number , id=f"{address}_{i}")
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
