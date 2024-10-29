"""Sphinx extension to handle the signal directive in the method."""

__version__ = '2024.10'

import inspect
import ast
import sys
import types
import re
from typing import get_type_hints
from typing import get_overloads
from typing import TYPE_CHECKING, Any, ClassVar, NamedTuple, cast

from sphinx.util.inspect import signature, stringify_signature

from sphinx import addnodes
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.domains.python import PyMethod, PyObject
import sphinx.domains.python as sphinxPythonDomain

if True or TYPE_CHECKING:
    from collections.abc import Sequence

    from docutils.nodes import Node, system_message

    from sphinx.application import Sphinx
    from sphinx.extension import Extension
    from sphinx.util.typing import ExtensionMetadata, OptionSpec
    from sphinx.writers.html5 import HTML5Translator

import sphinx.ext.autosummary as seauto
import sphinx.ext.autosummary.generate as seautogenerate

import TermTk as ttk

import ast
import inspect


def setup(app: Sphinx) -> ExtensionMetadata:
    '''Initialise the extension.'''

    # Collect all pyTermTk roles and domains
    modules = {}
    def _parseModules(_mod):
        if _file:=getattr(_mod,'__file__',None):
            if '__init__.py' in _file and '/TermTk/' in _file:
                print(_file)
                for _name, _obj in inspect.getmembers(_mod):
                    if inspect.isclass(_obj):
                        if _name not in modules:
                            modules[_name] = _mod.__name__
                        modules[_name] = _mod.__name__ if len(_mod.__name__)>len(modules[_name]) else modules[_name]
                        print(f" * {_name=} = {_obj}")

    for _module in sys.modules:
        _parseModules(sys.modules[_module])

    for x in modules.items():
        print(x)

    def _resolve(txt) -> str:
        oldTxt = txt
        if txt in modules:
            txt = f"~{modules[txt]}.{txt}"
            print(f"-----------> {oldTxt=} -> {txt=}")
        else:
            txts = txt.split('.')
            if txts[0] in modules:
                txts[0] = f"~{modules[txts[0]]}.{txts[0]}"
                txt = '.'.join(txts)
                print(f"-----------> {oldTxt=} -> {txt=}")
        return txt

    _process_link_bk = sphinxPythonDomain.PyXRefRole.process_link
    def _hacked_process_link(self, env, refnode,
                     has_explicit_title, title: str, target, _process_link_bk=_process_link_bk) -> tuple[str, str]:
        print(f"-----------> HACKED !!! {title=} {target=}")
        # title = _resolve(title)
        target = _resolve(target)
        return _process_link_bk(self, env, refnode,
                     has_explicit_title, title, target)

    sphinxPythonDomain.PyXRefRole.process_link = _hacked_process_link

