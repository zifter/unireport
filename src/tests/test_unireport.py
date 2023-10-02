from unireport.plugin import Plugin
from unireport.unireport import Unireport


def test_unireport_ctor():
    r = Unireport()
    result = r.render_from_string("Hello, {{ name }}!", {"name": "world"})
    assert result == "Hello, world!"


def test_register_plugin_ok():
    r = Unireport()
    r.register(Plugin())
