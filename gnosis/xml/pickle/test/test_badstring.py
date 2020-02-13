
# gnosis 1.1.1 can't correctly pickle & restore certain string & unicode
# values. gnosis 1.1.2 adds checks for those -- test that
# the checks are working.

# frankm@hiwaay.net

import gnosis.xml.pickle as xml_pickle
from gnosis.xml.pickle.util import setInBody
from types import *

class Foo:
    def __init__(self,s):
        self.s = s

class WeirdUni(str):
    def __init__(self,s):
        str.__init__(self,s)

# show that I didn't screw up normal strings
f = Foo('OK')
x = xml_pickle.dumps(f)
o = xml_pickle.loads(x)
print(o.s, type(o.s))

f = Foo('OK')
x = xml_pickle.dumps(f)
o = xml_pickle.loads(x)
print(o.s, type(o.s))

f = Foo(WeirdUni('OK'))
x = xml_pickle.dumps(f)
o = xml_pickle.loads(x)
print(o.s, type(o.s))

# pickler should catch all these unpickleable cases.
# (to be fixed in gnosis 1.2.x)

try:
    # Unicode string that contains our special string escape    
    f = Foo('\xbb\xbbABC\xab\xab')
    x = xml_pickle.dumps(f)
    print("************* ERROR *************")
except Exception as exc:
    print("OK  <%s>" % str(exc))
    
try:
    # Unicode string that contains our special string escape    
    f = Foo(WeirdUni('\xbb\xbbABC\xab\xab'))
    x = xml_pickle.dumps(f)
    print("************* ERROR *************")
except Exception as exc:
    print("OK  <%s>" % str(exc))
        
try:
    # Unicode string that contains our special string escape    
    f = Foo({'a':'\xbb\xbbABC\xab\xab'})
    x = xml_pickle.dumps(f)
    print("************* ERROR *************")
except Exception as exc:
    print("OK  <%s>" % str(exc))
        
try:
    # Unicode string that contains our special string escape
    f = Foo({'a':WeirdUni('\xbb\xbbABC\xab\xab')})
    x = xml_pickle.dumps(f)
    print("************* ERROR *************")
except Exception as exc:
    print("OK  <%s>" % str(exc))
    
try:
    # illegal Unicode value for an XML file 
    f = Foo('\ud800')
    x = xml_pickle.dumps(f)
    print("************* ERROR *************")
except Exception as exc:
    print("OK  <%s>" % str(exc))
    
try:
    # illegal Unicode value for an XML file
    f = Foo(WeirdUni('\ud800'))
    x = xml_pickle.dumps(f)
    print("************* ERROR *************")
except Exception as exc:
    print("OK  <%s>" % str(exc))
    
try:
    # safe_content assumes it can always convert the string
    # to unicode, which isn't true
    # ex: pickling a UTF-8 encoded value
    setInBody(StringType, 1)
    f = Foo('\xed\xa0\x80')
    x = xml_pickle.dumps(f)
    print("************* ERROR *************")
except Exception as exc:
    print("OK  <%s>" % str(exc))
    



