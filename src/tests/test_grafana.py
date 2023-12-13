import requests

from unireport.plugins.external.grafana import GrafanaAPI


def test_grafana_api_ok():
    api = GrafanaAPI(auth=requests.auth.AuthBase()).from_url("https://grafana.com")
    assert api
