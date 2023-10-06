from unireport import Plugin, ReportRenderer


def test_renderer_ctor():
    r = ReportRenderer()
    result = r.render_from_string("Hello, {{ name }}!", {"name": "world"})
    assert result == "Hello, world!"


def test_register_plugin_ok():
    r = ReportRenderer()
    r.register(Plugin())
