import jinja2
from jinja2 import Environment

from tests.utils import TEST_TEMPLATES_DIR
from unireport import ReportRenderer
from unireport.plugins.external.grafana import GrafanaAPI, GrafanaPlugin


def test_render_report(tmp_path):
    env = Environment(loader=jinja2.FileSystemLoader(searchpath=TEST_TEMPLATES_DIR))
    r = ReportRenderer(jinja2_env=env)
    api = GrafanaAPI.from_url(url="http://admin:admin@localhost:3000")
    r.register(GrafanaPlugin(api))

    data = {
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
    result = r.render_from_file("grafana_report.md", data, output=tmp_path)
    print(result)
