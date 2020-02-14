"Perform black magic of unearthly and ungodly sorts"

import inspect

from .dtdgenerator import *
from .metapickler import *

class import_with_metaclass_C(object):
    "This is a class factory, not a metaclass"
    def __init__(self, module, metaclass):
        class Meta(object, metaclass=metaclass): pass
        dct = {'__module__':module}
        mod = __import__(module)
        for key, val in list(mod.__dict__.items()):
            if not inspect.isclass(val):
                setattr(self, key, val)
            else:
                setattr(self, key, type(key,(val,Meta),dct))

def import_with_metaclass(modname, metaklass):
    "Module importer substituting custom metaclass"
    class Meta(object, metaclass=metaklass): pass
    dct = {'__module__':modname}
    mod = __import__(modname)
    for key, val in list(mod.__dict__.items()):
        if inspect.isclass(val):
            setattr(mod, key, type(key,(val,Meta),dct))
    return mod

def from_import(module, names="*"):
    if names == "*":
        names = [s for s in dir(module) if s[0]!="_"]
    elif names == "**":
        semisafe = lambda s: s not in ('__file__','__name__')
        names = list(filter(semisafe, dir(module)))
    for name in names:
        inspect.currentframe(1).f_globals[name] = getattr(module, name)

