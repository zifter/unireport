from typing import List

from unireport.plugin import Plugin


class Unireport:
    def __init__(self):
        self.plugins: List[Plugin] = []

    def register(self, plugin):
        self.plugins.append(plugin)

    def generate(self):
        pass
