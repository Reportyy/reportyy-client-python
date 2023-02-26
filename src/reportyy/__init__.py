from __future__ import absolute_import, division, print_function

# Configuration variables
api_base = "https://api.reportyy.com"
verify_ssl_certs = True
proxy = None
default_http_client = None

# Set to either 'debug' or 'info', controls console logging
log = None

# API client
from reportyy.client import *  # noqa E402
