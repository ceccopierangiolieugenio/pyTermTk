import importlib.util
import platform

if importlib.util.find_spec('pyodideProxy'):
    pass
elif platform.system() == 'Linux':
    from .terminal import *
    from .terminalview import *
elif platform.system() == 'Darwin':
    from .terminal import *
    from .terminalview import *
elif platform.system() == 'Windows':
    pass
