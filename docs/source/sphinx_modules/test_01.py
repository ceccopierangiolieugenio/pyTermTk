"""Sphinx extension to render inherited overloads with autodoc."""

__version__ = '2023.4'

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


# def test_process_signature(app, what, name, obj, options, sig, ret_ann):
#     '''Callback function to provide new signatures.'''
#     print(f"{app=}\n{what=}\n{name=}\n{obj=}\n{options=}\n{sig=}\n{ret_ann=}")
#     return '\n'.join(["a","b","c"]), "Pipppo Pippero"

# def test_process_docstring(app, what, name, obj, options, lines:list[str]):
#     '''Callback function to provide overloaded signatures.'''
#     print(f"{app=}\n{what=}\n{name=}\n{obj=}\n{options=}\n{lines=}")
#     for i,line in enumerate(lines):
#         lines[i] = line.replace("Table","PIPPO")

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
    # from:
    #   https://smobsc.readthedocs.io/en/stable/usage/extensions/autodoc.html
    #   https://github.com/ntessore/autodoc_inherit_overload/blob/main/sphinxcontrib/autodoc_inherit_overload.py
    # app.connect('autodoc-process-signature', test_process_signature)
    # app.connect('autodoc-process-docstring', test_process_docstring)

    app.add_directive_to_domain("py", "method", TermTkMethod, override=True)
