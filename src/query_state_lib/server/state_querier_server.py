def get_batch_request(json_request):
    return json_request.get("batch_request")


def get_batch_response(json_response):
    return {"response": json_response}


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


class StateQuerierServer:
    def __init__(self, batch_size=2000, max_workers=8):
        self.batch_size = batch_size
        self.max_workers = max_workers

    def generate_batch_query_request(self, json_request):
        batch_request = get_batch_request(json_request)
        return list(divide_chunks(batch_request, self.batch_size))
