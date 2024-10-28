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

# From
# https://stackoverflow.com/questions/3232024/introspection-to-get-decorator-names-on-a-method

def get_decorators(cls):
    target = cls
    decorators = {}

    def visit_FunctionDef(node):
        decorators[node.name] = []
        for n in node.decorator_list:
            name = ''
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id

            decorators[node.name].append(name)

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_FunctionDef
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return decorators


_styleMatch = re.compile('^ *classStyle')
_colorMatch = re.compile('^#[0-9a-fA-F]{6}')
def _get_classStyleCode(obj) -> list[str]:
    ret = []
    curlyBraket = 0
    def _processLine(line):
        cbRet = 0
        for i,ch in enumerate(line):
            if ch=='#':
                if not _colorMatch.match(line[i:]):
                    continue
            if   ch == '{':
                cbRet+=1
            elif ch == '}':
                cbRet-=1
                if  cbRet == 0:
                    return cbRet
        return cbRet

    for line in inspect.getsource(obj).split('\n'):
        # print(line)
        # print(f"{_styleMatch.match(line)=}")
        if curlyBraket == 0 and _styleMatch.match(line):
            print(line)
            ret.append(line)
            curlyBraket += _processLine(line)
        elif curlyBraket > 0:
            print(line)
            ret.append(line)
            curlyBraket += _processLine(line)
            if curlyBraket == 0:
                return ret
    return ret

def setup(app: Sphinx) -> ExtensionMetadata:
    '''Initialise the extension.'''

    modules = {}
    modSorted = {}
    modSub = {}
    modSubSorted = {}
    modStyles = {}
    ttkAllSignals={}
    ttkAllSlots={}

    def _getSignals(_obj):
        ret = []
        for _name in (_th:=get_type_hints(_obj)):
            print(f"{_th=}")
            if _name.startswith('_'): continue
            if 'pyTTkSignal' in str(_th[_name]):
                ret.append(_name)
            else:
                print(ttk.TTkString(f"element not typed: {_name} - { _th[_name]}",ttk.TTkColor.BG_CYAN))
        return ret

    def _parseModules(_mod):
        if _file:=getattr(_mod,'__file__',None):
            if '__init__.py' in _file and '/TermTk/' in _file:
                print(_file)
                for _name, _obj in inspect.getmembers(_mod):
                    if _mod.__name__ == 'TermTk.TTkCore.drivers': continue
                    if inspect.isclass(_obj):
                        if _name not in ttkAllSignals:
                            ttkAllSignals[_name] = _getSignals(_obj)
                        if _name not in modStyles:
                            modStyles[_name] = _get_classStyleCode(_obj)
                        if _name not in modules:
                            modules[_name] = _mod.__name__
                        modules[_name] = _mod.__name__ if len(_mod.__name__)>len(modules[_name]) else modules[_name]
                        print(f" * {_name=} = {_obj}")

    for _module in sys.modules:
        _parseModules(sys.modules[_module])

    for x in modules.items():
        print(x)
        a,b = x
        # if a == 'TermTk.TTkCore.drivers': continue
        if b not in modSorted:
            modSorted[b] = []
        modSorted[b].append(a)

    for (a,b) in modSorted.items():
        print(a)
        modSub[a] = '.'.join(a.split('.')[:-1])
        for x in b:
            print (f" - {x}")

    for x in modSub.items():
        print(x)

    for x in modSub.items():
        print(x)
        a,b = x
        if b not in modSubSorted:
            modSubSorted[b] = []
        modSubSorted[b].append(a)

    for (a,b) in modSubSorted.items():
        print(a)
        for x in b:
            print (f" - {x}")

    # print(modStyles)

    # raise Exception

    def generate_autosummary_content(
        name, obj, parent, template, template_name, imported_members,
        app, recursive, context, modname, qualname,
        generate_autosummary_content_old = seautogenerate.generate_autosummary_content
    ) -> str:
        print(f"-----------------> OVERRIDEEEEE!!! {type(context)}")
        print(f"{name=}")
        print(f"{obj=}")
        print(f"{parent=}")
        print(f"{template=}")
        print(f"{template_name=}")
        print(f"{imported_members=}")
        print(f"{app=}")
        print(f"{recursive=}")
        print(f"{context=}")
        print(f"{modname=}")
        print(f"{qualname=}")

        ttkSignals = []
        ttkSignalsImported = {}
        ttkSlots = []
        ttkSlotsImported = {}
        ttkMethods = []
        ttkInheritedMethods = []
        ttkSubClasses = modSorted.get(name,[])
        ttkSubModules = modSubSorted.get(name,[])

        # ns['members'] = dir(obj)
        # ns['inherited_members'] = set(dir(obj)) - set(obj.__dict__.keys())
        # ns['methods'], ns['all_methods'] = _get_members(
        #     doc, app, obj, {'method'}, include_public={'__init__'}
        # )
        # ns['attributes'], ns['all_attributes'] = _get_members(
        #     doc, app, obj, {'attribute', 'property'}
        # )

        print(f"{obj=}")
        # for member in inspect.getmembers(obj):
        #     _name = member[0]
        #     if _name.startswith('_'): continue
        #     _hint = get_type_hints(obj)[_name]

        # print(f"{obj=} - {get_type_hints(obj)=}")
        # for _name in (_th:=get_type_hints(obj)):
        #     print(f"{_th=}")
        #     if _name.startswith('_'): continue
        #     if 'pyTTkSignal' in str(_th[_name]):
        #         ttkSignals.append(_name)
        #     else:
        #         print(ttk.TTkString(f"element not typed: {_name} - { _th[_name]}",ttk.TTkColor.BG_CYAN))
        # print(ttkSignals)

        def _hasmethod(obj, name):
            return hasattr(obj, name) and type(getattr(obj, name)) in (types.MethodType, types.FunctionType)

        for _name in (_dec:=get_decorators(obj)):
            if _name.startswith('_'): continue
            if _hasmethod(obj,_name):
                ttkMethods.append(_name)
            for _decorator in _dec[_name]:
                if "pyTTkSlot"in _decorator:
                    ttkSlots.append(_name)
                    break

        context |= {
            'TTkStyle':modStyles.get(qualname,''),
            'TTkSignals':ttkAllSignals.get(qualname,''),
            'TTkSubClasses': ttkSubClasses,
            'TTkSubModules': ttkSubModules,
            'TTkMethods':ttkMethods,
            'TTkSlots':ttkSlots}

        print('\n'.join([f" * {x}={context[x]}" for x in context]))

        return generate_autosummary_content_old(
            name, obj, parent, template, template_name, imported_members,
            app, recursive, context, modname, qualname)

    seautogenerate.generate_autosummary_content = generate_autosummary_content

    return seauto.setup(app)
