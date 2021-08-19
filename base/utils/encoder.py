from web3 import Web3

w3 = Web3()


def encode_eth_call_data(abi, fn_name, args):
    contract = w3.eth.contract(abi=abi)

    encode_fnc = contract.encodeABI(fn_name=fn_name, args=args)
    return encode_fnc


def encode_eth_call_balance_of(address):
    prefix = "0x70a08231000000000000000000000000"
    return prefix + str(address).lower()[2:]
