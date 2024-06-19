import requests

from unireport.plugins.external.grafana import GrafanaAPI


def test_grafana_api_ok():
    api = GrafanaAPI.from_url("https://grafana.com", auth=requests.auth.AuthBase())
    assert api
