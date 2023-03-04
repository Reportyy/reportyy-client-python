from __future__ import absolute_import, division, print_function
from abc import ABC

import json

import reportyy
from reportyy import error, http_client, version, six


class ReportyyApiClientBase(ABC):
    def __init__(self, api_key, client, api_base_url):
        self.api_base_url = api_base_url or reportyy.api_base_url
        self.api_key = api_key

        from reportyy import verify_ssl_certs as verify

        if client:
            self._client = client
        elif reportyy.default_http_client:
            self._client = reportyy.default_http_client
        else:
            reportyy.default_http_client = http_client.new_default_http_client(
                verify_ssl_certs=verify,
            )
            self._client = reportyy.default_http_client

    def request(self, method, url, params=None, headers=None):
        rbody, rcode, rheaders, my_api_key = self.request_raw(
            method.lower(), url, params, headers, is_streaming=False
        )

        resp = self._interpret_response(rbody, rcode, rheaders)

        return resp, my_api_key

    def request_stream(self, method, url, params=None, headers=None):
        stream, rcode, rheaders, my_api_key = self.request_raw(
            method.lower(), url, params, headers, is_streaming=True
        )

        resp = self._interpret_streaming_response(stream, rcode, rheaders)

        return resp, my_api_key

    def _request_raw(
        self,
        method,
        url,
        params=None,
        supplied_headers=None,
        is_streaming=False,
    ):
        if self.api_key:
            my_api_key = self.api_key
        else:
            from reportyy import api_key

            my_api_key = api_key

        if my_api_key is None:
            raise error.AuthenticationError(
                "No API key provided. (HINT: set your API key using "
                '"reportyy.api_key = <API-KEY>"). You can generate API keys '
                "from the Reportyy Dashboard."
            )

        abs_url = "%s%s" % (self.api_base_url, url)
        post_data = json.dump(params) if params and method == "post" else None
        headers = self.request_headers(my_api_key, method)

        if supplied_headers is not None:
            for key, value in six.iteritems(supplied_headers):
                headers[key] = value

        if is_streaming:
            (
                rcontent,
                rcode,
                rheaders,
            ) = self._client.request_stream(method, abs_url, headers, post_data)
        else:
            rcontent, rcode, rheaders = self._client.request(
                method, abs_url, headers, post_data
            )

        return rcontent, rcode, rheaders, my_api_key

    def _should_handle_code_as_error(self, rcode):
        return not 200 <= rcode < 300

    def _request_headers(self, api_key, method):
        user_agent = "Reportyy PythonBindings/%s" % (version.VERSION,)
        ua = {
            "bindings_version": version.VERSION,
            "lang": "python",
            "httplib": self._client.name,
        }

        headers = {
            "X-Reportyy-Client-User-Agent": json.dumps(ua),
            "User-Agent": user_agent,
            "Authorization": "API-Key %s" % (api_key,),
        }

        if method == "post":
            headers["Content-Type"] = "application/json"

        return headers

    def _specific_api_error(self, rbody, rcode, resp, rheaders, error_data):
        # Rate limits were previously coded as 400's with code 'rate_limit'
        if rcode == 429:
            return error.RateLimitError(
                error_data.get("message"), rbody, rcode, resp, rheaders
            )
        elif rcode == 400:
            return error.InvalidRequestError(
                error_data.get("message"), rbody, rcode, resp, rheaders
            )
        elif rcode == 401:
            return error.AuthenticationError(
                error_data.get("message"), rbody, rcode, resp, rheaders
            )
        else:
            return error.APIError(
                error_data.get("message"), rbody, rcode, resp, rheaders
            )

    def _handle_error_response(self, rbody, rcode, resp, rheaders):
        err = self._specific_api_error(rbody, rcode, resp, rheaders, rbody)

        raise err

    def _interpret_response(self, rbody, rcode, rheaders):
        try:
            if hasattr(rbody, "decode"):
                rbody = rbody.decode("utf-8")

            resp = reportyy.ReportyyResponse(rbody, rcode, rheaders)
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                rbody,
                rcode,
                rheaders,
            )

        if self._should_handle_code_as_error(rcode):
            self._handle_error_response(rbody, rcode, resp.data, rheaders)

        return resp

    def _interpret_streaming_response(self, stream, rcode, rheaders):
        if self._should_handle_code_as_error(rcode):
            if hasattr(stream, "getvalue"):
                json_content = stream.getvalue()
            elif hasattr(stream, "read"):
                json_content = stream.read()
            else:
                raise NotImplementedError(
                    "HTTP client %s does not return an IOBase object which "
                    "can be consumed when streaming a response."
                )

            return self.interpret_response(json_content, rcode, rheaders)
        else:
            return reportyy.ReportyyStreamResponse(stream, rcode, rheaders)


class ReportyyApi(ReportyyApiClientBase):
    def __init__(self, api_key, client=None, api_base_url=None):
        super.__init__(api_key, client, api_base_url)

    def generate_pdf_stream(self, template_id, data):
        url = "/api/v1/templates/%s/generate-pdf-sync" % (template_id,)
        return super.request_stream("post", url, data)
