import importlib.util
import platform

if importlib.util.find_spec('pyodideProxy'):
    pass
elif platform.system() == 'Linux':
    from .terminalhelper import *
elif platform.system() == 'Darwin':
    from .terminalhelper import *
elif platform.system() == 'Windows':
    pass

from .terminal import *
from .terminalview import *