import importlib.util
import platform

if importlib.util.find_spec('pyodideProxy'):
    from .pyodide import *
    from .term_pyodide import *
elif platform.system() == 'Linux':
    from .unix import *
    from .term_unix import *
elif platform.system() == 'Darwin':
    from .unix import *
    from .term_unix import *
elif platform.system() == 'Windows':
    from .windows import *
    from .term_windows import *
