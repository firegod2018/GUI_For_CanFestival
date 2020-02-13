import string
from os import sep
s = str
#d = s.join(s.split(__file__, sep)[:-1], sep)+sep
d = sep.join(s.split(__file__, sep)[:-1])+sep
_ = lambda f: s.rstrip(open(d+f).read())
l = lambda f: s.split(_(f),'\n')

try:
    __doc__ = _('README')
except:
    pass
