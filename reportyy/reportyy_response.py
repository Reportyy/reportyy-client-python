from __future__ import absolute_import, division, print_function

import json
from collections import OrderedDict


class ReportyyResponseBase(object):
    def __init__(self, code, headers):
        self.code = code
        self.headers = headers


class ReportyyResponse(ReportyyResponseBase):
    def __init__(self, body, code, headers):
        ReportyyResponseBase.__init__(self, code, headers)
        self.body = body
        self.data = json.loads(body, object_pairs_hook=OrderedDict)


class ReportyyStreamResponse(ReportyyResponseBase):
    def __init__(self, io, code, headers):
        ReportyyResponseBase.__init__(self, code, headers)
        self.io = io
