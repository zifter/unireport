import http
from typing import Tuple, Union
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

DEFAULT_TIMEOUT = 30.0


HTTP_STATUS_FOR_RETRY = [
    http.HTTPStatus.REQUEST_TIMEOUT,
    http.HTTPStatus.GATEWAY_TIMEOUT,
    http.HTTPStatus.TOO_EARLY,
    http.HTTPStatus.TOO_MANY_REQUESTS,
    http.HTTPStatus.INTERNAL_SERVER_ERROR,
    http.HTTPStatus.SERVICE_UNAVAILABLE,
    http.HTTPStatus.BAD_GATEWAY,
]


class TokenAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers.update({"Authorization": f"Bearer {self.token}"})
        return request


class GrafanaClient:
    @classmethod
    def from_url(
        cls,
        url: str = "http://admin:admin@localhost:3000",
        auth: Union[str, Tuple[str, str], requests.auth.AuthBase] = None,
        **kwargs,
    ):
        """
        Factory method to create a `GrafanaApi` instance from a URL.

        Accepts an optional credential, which is either an authentication
        token, or a tuple of (username, password).
        """

        if auth is not None and not isinstance(
            auth, (str, Tuple, requests.auth.AuthBase)
        ):
            raise TypeError(f"Argument 'credential' has wrong type: {type(auth)}")

        url = urlparse(url)

        # Use username and password from URL.
        if auth is None and url.username:
            auth = (url.username, url.password)

        return GrafanaClient(
            auth,
            host=url.hostname,
            port=url.port,
            url_path_prefix=url.path.lstrip("/"),
            protocol=url.scheme,
            **kwargs,
        )

    def __init__(
        self,
        auth,
        host="localhost",
        port=None,
        url_path_prefix="",
        protocol="http",
        timeout: float = DEFAULT_TIMEOUT,
        retries: Retry
        | None = Retry(
            total=3, backoff_factor=1, status_forcelist=HTTP_STATUS_FOR_RETRY
        ),
    ):
        self.auth = auth
        self.timeout = timeout
        self.url_host = host
        self.url_port = port
        self.url_path_prefix = url_path_prefix
        self.url_protocol = protocol

        def construct_api_url():
            params = {
                "protocol": self.url_protocol,
                "host": self.url_host,
                "url_path_prefix": self.url_path_prefix,
            }

            if self.url_port is None:
                url_pattern = "{protocol}://{host}{url_path_prefix}"
            else:
                params["port"] = self.url_port
                url_pattern = "{protocol}://{host}:{port}{url_path_prefix}"

            return url_pattern.format(**params)

        self.grafana_root = construct_api_url()

        self.session = requests.Session()
        if retries:
            self.session.mount(self.grafana_root, HTTPAdapter(max_retries=retries))

        if auth is not None:
            if isinstance(auth, requests.auth.AuthBase):
                pass
            elif isinstance(auth, tuple):
                self.auth = requests.auth.HTTPBasicAuth(*auth)
            else:
                self.auth = TokenAuth(auth)

    def __getattr__(self, method):
        def __http_method_override(url, **kwargs):
            __url = self.grafana_root + url
            method_call = getattr(self.session, method.lower())
            return method_call(
                __url,
                auth=self.auth,
                timeout=self.timeout,
                **kwargs,
            )

        return __http_method_override
