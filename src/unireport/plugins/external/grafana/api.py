from unireport.plugins.external.grafana.client import GrafanaClient

DEFAULT_TIMEOUT = 30.0


class GrafanaAPI:
    @classmethod
    def from_url(cls, *args, **kwargs):
        client = GrafanaClient.from_url(*args, **kwargs)
        return cls(client=client)

    def __init__(self, client: GrafanaClient):
        self.client: GrafanaClient = client

    def query_raw(self, url, params=None):
        response = self.client.get(url, params=params)
        return response
