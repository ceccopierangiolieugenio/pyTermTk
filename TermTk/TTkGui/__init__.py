import importlib.util

from .drag         import *
from .textwrap1    import *
from .textcursor   import *
from .textdocument import *
from .clipboard    import *
from .tooltip      import *

if importlib.util.find_spec('pygments'):
    from .textdocument_highlight_pygments import *
else:
    from .textdocument_highlight import *
