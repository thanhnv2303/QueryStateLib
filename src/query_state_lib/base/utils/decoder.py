from web3 import Web3

w3 = Web3()


def hex_to_dec(hex_string):
    if hex_string is None:
        return None
    try:
        return int(hex_string, 16)
    except ValueError:
        print("Not a hex string %s" % hex_string)
        return hex_string


def decode_output_rpc(types, result):
    bytes_data = bytes.fromhex(result[2:])
    decode_data = w3.codec.decode_abi(types, bytes_data)
    return decode_data


def decode_eth_call_data(abi, fn_name, result):
    fn_abi = None
    for _fn_abi in abi:
        if _fn_abi.get("name") == fn_name:
            fn_abi = _fn_abi
            break
    if not fn_abi:
        raise Exception(f"function {fn_name} not found in abi")
    outputs = fn_abi.get("outputs")
    types = []
    for output in outputs:
        types.append(output.get("type"))

    return decode_output_rpc(types, result)


def decode_eth_call_balance_of(result):
    types = ["uint256"]
    return decode_output_rpc(types, result)[0]


def decode_eth_get_balance(result):
    return hex_to_dec(result)
