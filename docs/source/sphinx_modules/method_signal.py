"""Sphinx extension to handle the signal directive in the method."""

__version__ = '2024.10'

from typing import get_overloads
from typing import TYPE_CHECKING, Any, ClassVar, NamedTuple, cast

from sphinx.util.inspect import signature, stringify_signature

from sphinx import addnodes
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.domains.python import PyMethod, PyObject

if True or TYPE_CHECKING:
    from collections.abc import Sequence

    from docutils.nodes import Node, system_message

    from sphinx.application import Sphinx
    from sphinx.extension import Extension
    from sphinx.util.typing import ExtensionMetadata, OptionSpec
    from sphinx.writers.html5 import HTML5Translator



class TermTkMethod(PyMethod):
    option_spec: ClassVar[OptionSpec] = PyMethod.option_spec.copy()
    option_spec.update({
        'signal': directives.flag,
    })

    def get_signature_prefix(self, sig: str) -> list[nodes.Node]:
        prefix: list[nodes.Node] = super().get_signature_prefix(sig)
        if 'signal' in self.options:
            prefix.append(nodes.Text('signal'))
            prefix.append(addnodes.desc_sig_space())
        return prefix

def setup(app: Sphinx) -> ExtensionMetadata:
    '''Initialise the extension.'''

    app.add_directive_to_domain("py", "method", TermTkMethod, override=True)
