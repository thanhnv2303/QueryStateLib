from artifacts.abi_py.erc20_abi import ERC20_ABI
from query_state_lib.base.utils.decoder import decode_eth_call_data, decode_eth_call_balance_of, decode_eth_get_balance

abi = ERC20_ABI
fn_name = "balanceOf"
result = "0x000000000000000000000000000000000000000000d98a4d64cd3b63dbb5baec"

decode_result = decode_eth_call_data(abi, fn_name, result)
print(decode_result[0])

print(decode_eth_call_balance_of(result))

print(decode_eth_get_balance("0x0"))
