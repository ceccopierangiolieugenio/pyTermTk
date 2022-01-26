import platform

if platform.system() == 'Linux':
    from .input    import *
    from .term     import *
    from .colors   import *
    from .inputkey import *
elif platform.system() == 'Darwin':
    from .input    import *
    from .term     import *
    from .colors   import *
    from .inputkey import *
elif platform.system() == 'Windows':
    raise NotImplementedError('Windows OS not yet supported')
elif platform.system() == 'Emscripten':
    raise NotImplementedError('Pyodide not yet supported')

