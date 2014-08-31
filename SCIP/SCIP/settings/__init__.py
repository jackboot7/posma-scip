import sys

try:
    from local import *
except sys.exc_info()[0], e:
    print e