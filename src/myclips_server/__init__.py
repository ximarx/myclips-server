
import logging as _logging
import sys
import os



FORMAT = '[%(levelname).3s %(module)s::%(funcName)s:%(lineno)d] %(message)s'
_logging.basicConfig(format=FORMAT)

logger = _logging.getLogger('myclips_server')
logger.setLevel(_logging.ERROR)


MYCLIPS_LIB_SRC_PATH = ['../../myclips', '../../../myclips', '../myclips', '../lib/myclips',
                        '../../myclips/src/', '../../../myclips/src/', '../myclips/src', '../lib/myclips/src']

pathIndex = -1
while True:
    try:
        import myclips
        print "Using: ", repr(myclips)
        break
    except ImportError:
        if pathIndex > -1:
            sys.path.pop()
        pathIndex += 1
        try:
            sys.path.append(os.path.abspath( MYCLIPS_LIB_SRC_PATH[pathIndex] ))
        except:
            print >> sys.stderr, "MyCLIPS not found in:"
            print >> sys.stderr, "    ", os.path.abspath( "." )
            for p in MYCLIPS_LIB_SRC_PATH:
                print >> sys.stderr, "    ", os.path.abspath(p)
            raise ImportError("No package named myclips")

    
from myclips.MyClipsException import MyClipsException

class MyClipsServerException(MyClipsException):
    pass
