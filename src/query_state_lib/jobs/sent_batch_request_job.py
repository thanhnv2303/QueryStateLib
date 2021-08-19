# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import json
import logging

from query_state_lib.base.executors.batch_work_executor import BatchWorkExecutor
from query_state_lib.base.jobs.base_job import BaseJob

logger = logging.getLogger(__name__)


class SentBatchRequestJob(BaseJob):
    def __init__(
            self,
            request,
            batch_provider,
            batch_size=2000,
            max_workers=5):
        self.request = request
        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.batch_provider = batch_provider
        self.response = []

    def _start(self):
        pass

    def _export(self):
        self.batch_work_executor.execute(
            self.request,
            self._export_batch,
            total_items=len(self.request)
        )

    def _export_batch(self, batched_request):
        self.response += self.batch_provider.make_batch_request(json.dumps(batched_request))

    def _end(self):
        self.batch_work_executor.shutdown()

    def get_response(self):
        return self.response

    def clean_cache(self):
        self.response = []
