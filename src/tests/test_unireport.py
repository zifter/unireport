from unireport.plugin import Plugin
from unireport.unireport import Unireport


def test_unireport_ctor():
    r = Unireport()
    r.generate()


def test_register_plugin_ok():
    r = Unireport()
    r.register(Plugin())
