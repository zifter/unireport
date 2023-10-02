import jinja2

from tests.utils import TEST_TEMPLATES_DIR
from unireport.plugins.external.grafana import GrafanaAPI, GrafanaPlugin
from unireport.unireport import Unireport


def test_render_report(tmp_path):
    loader = jinja2.FileSystemLoader(searchpath=TEST_TEMPLATES_DIR)
    r = Unireport(loader=loader)
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
