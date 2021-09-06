from typing import List

import requests

from query_state_lib.base.mappers.eth_call_balance_of_mapper import generate_eth_call_balance_of_json_rpc
from query_state_lib.base.mappers.eth_call_mapper import generate_eth_call_json_rpc
from query_state_lib.base.mappers.eth_json_rpc_mapper import EthJsonRpc, generate_eth_json_rpc
from query_state_lib.base.mappers.get_balance_mapper import generate_get_balance_json_rpc
from query_state_lib.base.providers.auto import get_provider_from_uri
from query_state_lib.jobs.sent_batch_request_job import SentBatchRequestJob


def _sent_batch(list_json_rpc: List[EthJsonRpc], func_sent_handler, err_list=[]):
    """

    :param list_json_rpc:
    :param func_sent_handler:   is a function with argument is a request
                                request is a list , each element is a dict with form of json rpc like :
                                    {
                                        'jsonrpc': '2.0',
                                        'method': method,
                                        'params': params,
                                        'id': request_id,
                                    }

    :return:
    """
    if not list_json_rpc:
        return dict()
    dict_eth_json_rpc = dict()
    type_dict_list = dict()
    for json_rpc in list_json_rpc:
        type_list = type_dict_list.get(json_rpc.type)
        if not type_list:
            type_dict_list[json_rpc.type] = []
            type_list = type_dict_list[json_rpc.type]
        type_list.append(json_rpc)
        dict_eth_json_rpc[json_rpc.id] = json_rpc
    request = []
    for type in type_dict_list:
        request += generate_json_rpc_from_type(type, type_dict_list[type])

    response = func_sent_handler(request)
    check_response(response)
    for response_item in response:
        id = response_item.get("id")
        result = response_item.get("result")
        dict_eth_json_rpc[id].set_result(result)
        if not result:
            err_list.append(dict_eth_json_rpc[id])
            dict_eth_json_rpc[id].error = response_item.get("error")
    return dict_eth_json_rpc


def check_response(response):
    res_start = response[0]
    id = res_start.get("id")
    err = res_start.get("error")
    res_end = response[-1]
    id2 = res_end.get("id")
    err2 = res_end.get("error")
    if res_start.get("error") and res_end.get("error"):
        raise Exception(f"""
        Response data err 
        Request {id} - err {err}
        ...
        Request {id2}- err {err2}
        """)


class ClientQuerier:
    def __init__(self, provider_url):
        self.provider_url = provider_url
        self.batch_provider = get_provider_from_uri(provider_url, batch=True)
        self.recent_err = []

    def sent_batch_to_state_querier(self, list_json_rpc: List[EthJsonRpc]):
        """

        :param list_json_rpc:
        :return:
        """

        url = self.provider_url + "/batch-query"

        def sent_batch_to_state_querier_server(request):
            data = {
                "request": request,
                "batch_request": True
            }
            res = requests.post(url, json=data)
            if res.status_code != 200:
                raise Exception(f"provider {self.provider_url} not support batch-query api")
            return res.json().get("response")

        sent_handler = sent_batch_to_state_querier_server
        self.recent_err = []
        dict_eth_json_rpc = _sent_batch(list_json_rpc, sent_handler, self.recent_err)

        return dict_eth_json_rpc

    def sent_batch_to_provider(self, list_json_rpc: List[EthJsonRpc], batch_size=2000, max_workers=8):
        """

        :param list_json_rpc:
        :return:
        """

        batch_provider = self.batch_provider

        def sent_batch_direct(request):
            job = SentBatchRequestJob(request, batch_provider, batch_size=batch_size, max_workers=max_workers)
            job.run()

            response = job.get_response()
            return response

        sent_handler = sent_batch_direct
        self.recent_err = []
        dict_eth_json_rpc = _sent_batch(list_json_rpc, sent_handler, self.recent_err)

        return dict_eth_json_rpc


MAP_TYPE_JSON_RPC_GENERATOR = {
    "eth_get_balance": generate_get_balance_json_rpc,
    "eth_call_balance_of": generate_eth_call_balance_of_json_rpc,
    "eth_call": generate_eth_call_json_rpc,
    "eth_json_rpc": generate_eth_json_rpc
}


def generate_json_rpc_from_type(type, eth_json_rpc_list: List[EthJsonRpc]):
    generator = MAP_TYPE_JSON_RPC_GENERATOR.get(type)
    if generator:
        return list(generator(eth_json_rpc_list))
    else:
        return []
