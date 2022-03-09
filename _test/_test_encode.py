from query_state_lib.base.utils.encoder import encode_eth_call_balance_of

print(encode_eth_call_balance_of("0x58f876857a02d6762e0101bb5c46a8c1ed44dc16"))
value = 0x58f876857a02d6762e0101bb5c46a8c1ed44dc16

type_of = type(encode_eth_call_balance_of)

print(type_of)
