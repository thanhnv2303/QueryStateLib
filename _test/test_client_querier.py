import time

from web3 import Web3

from base.mappers.eth_call_balance_of_mapper import EthCallBalanceOf
from client.client_querier import ClientQuerier

url = "https://speedy-nodes-nyc.moralis.io/51ed809fc830640c534fe746/bsc/mainnet/archive"
client_querier = ClientQuerier(provider_url=url)

contract_address = Web3.toChecksumAddress('0x334b3ecb4dca3593bccc3c7ebd1a1c1d1780fbf1')

block_number = 9941237

address = "0x0e6ddcf8f1bf0879bdd50fb314757fea7b71fa9e"

number_query = 10000

call_infos = []

get_balances = []
start = time.time()
for i in range(number_query):
    call1 = EthCallBalanceOf(contract_address, address, block_number + i, id=i)
    call_infos.append(call1)

    # get_balance = GetBalance(address, block_number + i, id=number_query + i)
    # get_balances.append(get_balance)

# list_json_rpc = []
list_json_rpc = call_infos + get_balances

data_result = client_querier.sent_batch_to_provider(list_json_rpc)
end = time.time()

print(f"finish after {end - start}s")
