import jinja2
import pytest
from jinja2 import Environment
from requests.exceptions import RetryError

from tests.utils import TEST_TEMPLATES_DIR
from unireport import ReportRenderer
from unireport.exceptions import RendererException
from unireport.plugins.external.grafana import GrafanaAPI, GrafanaPlugin

TEST_DATA = {
    "dashboards": [
        {
            "name": "test1",
            "url": "http://localhost:3000/d/iUfmr5kMk/prometheus-2-22?orgId=1",
        },
        {
            "name": "test2",
            "url": "http://localhost:3000/d/iUfmr5kMk/prometheus-2-22?orgId=1",
        },
    ],
}


def test_render_report_ok(tmp_test_dir):
    env = Environment(loader=jinja2.FileSystemLoader(searchpath=TEST_TEMPLATES_DIR))
    r = ReportRenderer(jinja2_env=env)
    api = GrafanaAPI.from_url(url="http://admin:admin@localhost:3000")
    r.register(GrafanaPlugin(api))

    result = r.render_from_file("grafana_report.md", TEST_DATA, output=tmp_test_dir)
    assert result


def test_render_report_render_params_ok(tmp_test_dir):
    env = Environment(loader=jinja2.FileSystemLoader(searchpath=TEST_TEMPLATES_DIR))
    r = ReportRenderer(jinja2_env=env)
    api = GrafanaAPI.from_url(url="http://admin:admin@localhost:3000")
    r.register(GrafanaPlugin(api))

    result = r.render_from_file("grafana_report.md", TEST_DATA, output=tmp_test_dir)
    assert result


def test_render_report_unauthorized():
    r = ReportRenderer()
    api = GrafanaAPI.from_url(url="http://localhost:3000")
    r.register(GrafanaPlugin(api))

    with pytest.raises(RendererException) as excinfo:
        r.render_from_string(
            "{{ render_grafana_dashboard('http://localhost:3000/d/iUfmr5kMk/prometheus-2-22?orgId=1') }}",
            {},
        )

    assert str(excinfo.value) == "Invalid content-type text/html; charset=UTF-8"


def test_render_report_for_wrong_host():
    r = ReportRenderer()
    api = GrafanaAPI.from_url(url="http://localhost:3000")
    r.register(GrafanaPlugin([api]))

    with pytest.raises(RendererException) as excinfo:
        r.render_from_string(
            "{{ render_grafana_dashboard('http://wronghost:3000/d/iUfmr5kMk/prometheus-2-22?orgId=1') }}",
            {},
        )

    assert str(excinfo.value) == "Can't find GrafanaAPI for wronghost"


def test_render_report_invalid_token():
    r = ReportRenderer()
    api = GrafanaAPI.from_url(url="http://localhost:3000", credential="invalid-token")
    r.register(GrafanaPlugin(api))

    with pytest.raises(RendererException) as excinfo:
        r.render_from_string(
            "{{ render_grafana_dashboard('http://localhost:3000/d/iUfmr5kMk/prometheus-2-22?orgId=1') }}",
            {},
        )

    assert str(excinfo.value) == "Invalid content-type text/html; charset=UTF-8"


def test_render_report_with_retry():
    r = ReportRenderer()
    api = GrafanaAPI.from_url(url="https://httpbin.org", credential="fake-token")
    r.register(GrafanaPlugin(api, render_path_template="{path}"))

    with pytest.raises(RetryError) as excinfo:
        r.render_from_string(
            "{{ render_grafana_dashboard('https://httpbin.org/status/500') }}",
            {},
        )

    assert "Max retries exceeded with url: /status/500" in str(excinfo.value)


def test_render_report_with_failed_request():
    r = ReportRenderer()
    api = GrafanaAPI.from_url(url="https://httpbin.org", credential="fake-token")
    r.register(GrafanaPlugin(api, render_path_template="{path}"))

    with pytest.raises(RetryError) as excinfo:
        r.render_from_string(
            "{{ render_grafana_dashboard('https://httpbin.org/status/500') }}",
            {},
        )

    assert "Max retries exceeded with url: /status/500" in str(excinfo.value)


def test_render_report_with_exception_and_stub_image():
    r = ReportRenderer()
    api = GrafanaAPI.from_url(url="https://httpbin.org", credential="fake-token")
    r.register(
        GrafanaPlugin(
            api, render_path_template="{path}", stub_dashboard_image_on_exception=True
        )
    )
    r.render_from_string(
        "{{ render_grafana_dashboard('https://httpbin.org/status/500') }}",
        {},
    )
