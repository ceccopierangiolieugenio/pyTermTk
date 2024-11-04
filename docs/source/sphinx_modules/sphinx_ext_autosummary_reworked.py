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

def _get_decorators(cls):
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

def _get_attributes(obj,filter):
    return sorted([item for item in (set(dir(obj)) - set(filter)) if not item.startswith('_') and not inspect.isclass(getattr(obj,item))])

def _get_classes(obj,filter):
    return sorted([item for item in (set(dir(obj)) - set(filter)) if not item.startswith('_') and inspect.isclass(getattr(obj,item))])

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
            # print(line)
            ret.append(line)
            curlyBraket += _processLine(line)
        elif curlyBraket > 0:
            # print(line)
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
    ttkAllMethods={}
    ttkAllSlots={}
    ttkAllMembers={} # List all the member of a class
    ttkInherited={}  # List of the inherited classes for each class

    def _getMethodsAndSlots(_obj):
        retSlots = []
        retMethods = []
        def _hasmethod(obj, name):
            return hasattr(obj, name) and type(getattr(obj, name)) in (types.MethodType, types.FunctionType)

        for _name in (_dec:=_get_decorators(_obj)):
            if _name.startswith('_'): continue
            if _hasmethod(_obj,_name):
                retMethods.append(_name)
            for _decorator in _dec[_name]:
                if "pyTTkSlot"in _decorator:
                    retSlots.append(_name)
                    break
        return retMethods,retSlots

    def _getInherited(_obj):
        ret = []
        for cc in _obj.__mro__:
            if cc==_obj: continue
            # if hasattr(cc,'_ttkProperties'):
            if (
                issubclass(cc, ttk.TTkTemplates.dragevents.TDragEvents) or
                issubclass(cc, ttk.TTkTemplates.mouseevents.TMouseEvents) or
                issubclass(cc, ttk.TTkTemplates.keyevents.TKeyEvents) or
                issubclass(cc, ttk.TTkWidget) or
                issubclass(cc, ttk.TTkLayout) ) :
                ccName = cc.__name__
                ret.append(ccName)
                # print(ccName)
        # print(f"_getInherited {ret}")
        return ret

    def _getSignals(_obj):
        ret = []
        for _name in (_th:=get_type_hints(_obj)):
            # print(f"{_th=}")
            if _name.startswith('_'): continue
            if 'pyTTkSignal' in str(_th[_name]):
                ret.append(_name)
            else:
                print(ttk.TTkString(f"element not typed: {_name} - { _th[_name]}",ttk.TTkColor.BG_CYAN))
        return ret

    def _parseModules(_mod):
        if _file:=getattr(_mod,'__file__',None):
            if '__init__.py' in _file and '/TermTk/' in _file:
                # print(_file)
                for _name, _obj in inspect.getmembers(_mod):
                    if _mod.__name__ == 'TermTk.TTkCore.drivers': continue
                    if inspect.isclass(_obj):
                        _meth,_slots = _getMethodsAndSlots(_obj)
                        if _name not in ttkAllMethods:
                            ttkAllMethods[_name] = _meth
                        if _name not in ttkAllSlots:
                            ttkAllSlots[_name] = _slots
                        if _name not in ttkAllSignals:
                            ttkAllSignals[_name] = _getSignals(_obj)
                        if _name not in ttkInherited:
                            ttkInherited[_name] = _getInherited(_obj)
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

    for (x,y) in ttkInherited.items():
        print(f"Inherited {x} -> {y}")

    # print(modStyles)

    # raise Exception

    def generate_autosummary_content_hack(
        name, obj, parent, template, template_name, imported_members,
        app, recursive, context, modname, qualname,
        generate_autosummary_content_old = seautogenerate.generate_autosummary_content
    ) -> str:
        print(f"-----------------> OVERRIDEEEEE!!! {type(context)}")
        print(f"{name=}")
        # print(f"{obj=}")
        # print(f"{parent=}")
        # print(f"{template=}")
        # print(f"{template_name=}")
        # print(f"{imported_members=}")
        # print(f"{app=}")
        # print(f"{recursive=}")
        # print(f"{context=}")
        print(f"{modname=}")
        print(f"{qualname=}")

        ttkSignals = []
        ttkSignalsImported = {}
        ttkSlots = []
        ttkSlotsInherited = {}
        ttkMethods = []
        ttkMethodsInherited = {}
        ttkInheritedMethods = []
        ttkSubClasses = modSorted.get(name,[])
        ttkSubModules = modSubSorted.get(name,[])

        def _get_slots_in_obj(_name):
            _slotsInherited = {_sub : sorted(ttkAllSlots.get(_sub,[])) for _sub in ttkInherited.get(_name,[])}
            _slots = set(ttkAllSlots.get(_name,[])) - set([_sl for _subSl in _slotsInherited.values() for _sl in _subSl])
            return sorted(list(_slots)), _slotsInherited

        ttkSlots, ttkSlotsInherited = _get_slots_in_obj(qualname)

        def _get_methods_in_obj(_name):
            _methodsInherited = {_sub : sorted(ttkAllMethods.get(_sub,[])) for _sub in ttkInherited.get(_name,[])}
            _methods = set(ttkAllMethods.get(_name,[])) - set([_sl for _subSl in _methodsInherited.values() for _sl in _subSl])
            return sorted(list(_methods)), _methodsInherited

        ttkMethods, ttkInheritedMethods = _get_methods_in_obj(qualname)

        def _get_attributes_in_obj(_obj,_name):
            _allMethods = ttkAllMethods.get(_name,[])
            _slots = ttkAllSlots.get(_name,[])
            _signals = ttkAllSignals.get(_name,[])
            _classes = _get_classes(_obj,[])
            return _get_attributes(_obj,_allMethods+_slots+_signals+_classes)

        def _get_simple_attributes(_obj):
            return sorted(set(
                    [item for item in dir(obj)
                          if (
                              not (
                                item.startswith('_') or
                                inspect.isclass(   _attr:=getattr(obj,item)) or
                                inspect.ismethod(  _attr) or
                                inspect.isfunction(_attr)
                              ) ) ] ) )

        ttkAttributes = sorted(set(_get_simple_attributes(obj)) - set(ttkAllSignals.get(qualname,'')))

        context |= {
            'TTkAttributes':       sorted( ttkAttributes ),
            'TTkClasses':          sorted( _get_classes(obj,ttkMethods+ttkSlots+ttkAllSignals.get(qualname,[])) ),
            'TTkSignals':          sorted( ttkAllSignals.get(qualname,'') ),
            'TTkSubClasses':       sorted( ttkSubClasses ),
            'TTkSubModules':       sorted( ttkSubModules ),
            'TTkSlots':            sorted( ttkSlots ),
            'TTkMethods':          sorted( ttkMethods ),
            'TTkStyle':                    modStyles.get(qualname,'') ,
            'TTkSlotsInherited':           ttkSlotsInherited ,
            'TTkMethodsInherited':         ttkInheritedMethods ,
            }

        print('\n'.join([f" * {x}={context[x]}" for x in context]))

        return generate_autosummary_content_old(
            name, obj, parent, template, template_name, imported_members,
            app, recursive, context, modname, qualname)

    # def get_import_prefixes_from_env_hack(env, get_import_prefixes_from_env_old=seauto.get_import_prefixes_from_env) -> list[str | None]:
    #     pyClass = env.ref_context.get('py:class')
    #     # env.ref_context.set('py:class')
    #     prefixes = get_import_prefixes_from_env_old(env)
    #     retPrefixes = []
    #     for p in prefixes:
    #         if not p:
    #             retPrefixes.append(p)
    #             continue
    #         psplit = p.split('.')
    #         cur = ret = psplit[0]
    #         for pp in psplit[1:]:
    #             print(f"SPLIT: {pp} - {pyClass=} - {prefixes}")
    #             if cur != pp:
    #                 ret += f".{pp}"
    #         retPrefixes.append(ret)
    #     return retPrefixes

    seautogenerate.generate_autosummary_content = generate_autosummary_content_hack
    # seauto.get_import_prefixes_from_env = get_import_prefixes_from_env_hack
    return seauto.setup(app)