from django.utils import six
from django.utils.functional import LazyObject
from django.utils.importlib import import_module

# support legacy parser module usage
from compressor.parser.base import ParserBase  # noqa
from compressor.parser.lxml import LxmlParser
from compressor.parser.default_htmlparser import DefaultHtmlParser as HtmlParser
from compressor.parser.html5lib import Html5LibParser  # noqa


class AutoSelectParser(LazyObject):
    options = (
        # TODO: make lxml.html parser first again
        (six.moves.html_parser.__name__, HtmlParser),  # fast and part of the Python stdlib
        ('lxml.html', LxmlParser),  # lxml, extremely fast
    )

    def __init__(self, content):
        self._wrapped = None
        self._setup(content)

    def __getattr__(self, name):
        return getattr(self._wrapped, name)

    def _setup(self, content):
        for dependency, parser in self.options:
            try:
                import_module(dependency)
                self._wrapped = parser(content)
                break
            except ImportError:
                continue
