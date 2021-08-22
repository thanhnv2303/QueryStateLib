import logging

from query_state_lib.jobs.handler_batch_request_job import HandlerBatchRequestJob


def get_batch_request(json_request):
    return json_request.get("request")


def get_batch_response(json_response):
    return {"response": json_response}


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def is_batch_request(request):
    try:
        return request.get("batch_request")
    except Exception as e:
        return False


class StateQuerierServer:
    def __init__(self, batch_size=2000, max_workers=8, logger=logging.getLogger("StateQuerierServer")):
        """
        process_request is func with signature  same as : def process(request, batch=True)
        """
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.logger = logger

    def generate_batch_query_request(self, json_request):
        batch_request = get_batch_request(json_request)
        return list(divide_chunks(batch_request, self.batch_size))

    def handle_batch_request(self, request_json, process_func):
        try:
            request_data = get_batch_request(request_json)
            job = HandlerBatchRequestJob(request_data, process_func, self.batch_size, self.max_workers)
            job.run()
            response = job.get_response()
            return {"response": response}
        except Exception as e:
            self.logger.warning(f"err when handle batch request {e}")
            return None
