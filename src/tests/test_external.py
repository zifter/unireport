import pytest

from unireport.plugins.external.grafana import GrafanaAPI


def test_grafana_incorrect_token():
    with pytest.raises(TypeError) as excinfo:
        GrafanaAPI.from_url(url="http://localhost:3000", credential=list())

    assert str(excinfo.value) == "Argument 'credential' has wrong type: <class 'list'>"
