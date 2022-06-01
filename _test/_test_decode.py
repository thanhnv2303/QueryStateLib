from artifacts.abi_py.erc20_abi import ERC20_ABI
from artifacts.abi_py.lending_pool_abi import LENDING_POOL_ABI
from query_state_lib.base.utils.decoder import decode_eth_call_data, decode_eth_call_balance_of, decode_eth_get_balance

abi = ERC20_ABI
fn_name = "balanceOf"
result = "0x000000000000000000000000000000000000000000d98a4d64cd3b63dbb5baec"

decode_result = decode_eth_call_data(abi, fn_name, result)
print(decode_result[0])

print(decode_eth_call_balance_of(result))

print(decode_eth_get_balance("0x0"))

#### test decode for tuple
abi = LENDING_POOL_ABI
fn_name = "getReserveData"
result = "0x0000000000000000000000000000000000000000000003e8011229041f401d4c0000000000000000000000000000000000000000033b439631b5352dca7253c80000000000000000000000000000000000000000033b5773da738274fabce54d0000000000000000000000000000000000000000000b59a267c3177b2a9a864000000000000000000000000000000000000000000016d69d107f9d1003441c41000000000000000000000000000000000000000000000000000000006146a55800000000000000000000000017335ff98beba2e36d11421d4bd613c24b61acbe000000000000000000000000fa0be8c6dd8bc5d44c54ba538d360380f949d0df0000000000000000000000002262c0b9ed840532f7cd41dc09fd9fb6a69f91b90000000000000000000000000000000000000000000000000000000000000000"

decode_result = decode_eth_call_data(abi, fn_name, result)
print(decode_result)
print(decode_result[0][0])