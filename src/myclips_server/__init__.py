import traceback


MYCLIPS_LIB_SRC_PATH = ['../../myclips', '../../../myclips', '../myclips', '../lib/myclips',
                        '../../myclips/src/', '../../../myclips/src/', '../myclips/src', '../lib/myclips/src']

MYCLIPS_FUNCTIONS_REPLACEMENTS = [{
        "module": 'myclips_server.server_functions.DrawCircuit',
        "class": 'DrawCircuit',
    }]


import logging as _logging
import sys
import os



FORMAT = '[%(levelname).3s %(module)s::%(funcName)s:%(lineno)d] %(message)s'
_logging.basicConfig(format=FORMAT)

logger = _logging.getLogger('myclips_server')
logger.setLevel(_logging.ERROR)


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

def __replaceFuncs(_F_REPLACEMENTS):

    # replace some system function definition with a server-proof version:
    
    if len(_F_REPLACEMENTS):
    
        import myclips.functions as _mycfuncs
        
        # manually bootstrap system functions
        _mycfuncs.SystemFunctionBroker.bootstrap()
        
        for _funcInfo in _F_REPLACEMENTS:
    
            print "Replacing: ", _funcInfo    
    
            try:
                # prepare the replacement
                
                _moduleName = _funcInfo['module']
                _className = _funcInfo['class']
                _funcInstance = myclips.newInstance(_className, None, _moduleName)
            except:
                print "\t... Error"
                traceback.print_exc()
            else:
                # then replace the definition
                _mycfuncs.SystemFunctionBroker.register(_funcInstance, True)
                print "\t... Done"


__replaceFuncs(MYCLIPS_FUNCTIONS_REPLACEMENTS) 





