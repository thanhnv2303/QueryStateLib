from query_state_lib.client.moralis_client.client import MoralisClient
from query_state_lib.client.moralis_client.examples import LIQUIDATE_EVENT

if __name__ == '__main__':
    x_api_keys = ["vCW7IgiEDAWfftnUxea8OcF6EWGiRdzFb1e7XyuQoecMUKOVEMGNB8LfAdoCS9dC",
                  "lBJVBjSy5AyLi9tLjs1ysz6OIFlnOdmd1cvH6Q3ROSkRMJI8sxoJXtE9BbliKao4"]
    moralis_client = MoralisClient(x_api_keys)
    res = moralis_client.ping()
    print(res)
    print("Date to block")
    date = "2022-1-1"
    chain = "bsc"
    res = moralis_client.date_to_block(chain=chain, date=date)
    print(res)

    print("Get price")
    chain = "bsc"
    address = "0x0391bE54E72F7e001f6BBc331777710b4f2999Ef"
    res = moralis_client.get_token_price(address=address, chain=chain)
    print(res)

    address = "0xACd7869C648CCB1b3478615e194aeb045A2e905f"
    to_block = 13936545
    token_balance = moralis_client.get_token_balance(address, to_block=to_block)

    print(f"Token balances of address {address}")
    print(token_balance)

    chain = "bsc"
    topic0 = "0xe413a321e8681d831f4dbccbca790d2952b56f977908e45be37335533e005286"
    address = "0x75de5f7c91a89c16714017c7443eca20c7a8c295"

    res = moralis_client.get_address_logs(address, topic0=topic0, chain=chain)
    print(f"Logs of address {address}")
    print(res)

    print(f"Event by topic")
    chain = "bsc"
    topic = "0xe413a321e8681d831f4dbccbca790d2952b56f977908e45be37335533e005286"
    address = "0x75de5f7c91a89c16714017c7443eca20c7a8c295"
    event_abi = LIQUIDATE_EVENT
    res = moralis_client.get_address_event_by_topic(chain=chain, address=address, topic=topic, event_abi=event_abi)
    print(res)
