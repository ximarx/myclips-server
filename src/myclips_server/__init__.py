import traceback
import logging as _logging
import sys
import os
import json
from xmlrpclib import Fault

__author__  = "Francesco Capozzo <ximarx@gmail.com>"
__status__  = "development"
__version__ = "0.0-dev"

try:
    CONFIGURATIONS = json.load(open(os.path.dirname(__file__)+'/configs.json', "rU"))
except:
    print >> sys.stderr, "Error loading configurations"
    traceback.print_exc()
    CONFIGURATIONS = {
        "myclips_server": {
            "bind-address": "localhost",
            "bind-port": 8081,
            "log-requests": True,
            "log-level": _logging.WARNING,
            "services": [
                "Registry", "Sessions", "Engine"
            ]

        },
        "myclips": {
            "log-level": _logging.ERROR,
            "search-paths": [
                '../../myclips', '../../../myclips', '../myclips', '../lib/myclips',
                '../../myclips/src/', '../../../myclips/src/', '../myclips/src', '../lib/myclips/src'
            ],
            "system-functions": {
                "remove": [
                    'open', 'close'
                ],
                "replace": [],
                "register": []
            }
        }
    }
    

MYCLIPS_LIB_SRC_PATH = CONFIGURATIONS.get('myclips', {}).get('search-paths', [])
MYCLIPS_FUNCTIONS_REPLACEMENTS = CONFIGURATIONS.get('myclips', {}).get('system-functions', {}).get('replace', [])
MYCLIPS_FUNCTIONS_REMOVALS = CONFIGURATIONS.get('myclips', {}).get('system-functions', {}).get('remove', [])
MYCLIPS_FUNCTIONS_REGISTRATIONS = CONFIGURATIONS.get('myclips', {}).get('system-functions', {}).get('register', [])

FORMAT = '[%(levelname).3s %(module)s::%(funcName)s:%(lineno)d] %(message)s'
_logging.basicConfig(format=FORMAT)


logger = _logging.getLogger('myclips_server')
logger.setLevel(CONFIGURATIONS.get('myclips_server', {}).get('log-level', _logging.WARNING))


pathIndex = -1
while True:
    try:
        import myclips
        logger.info("Using: %s", repr(myclips))
        myclips.logger.setLevel(CONFIGURATIONS.get('myclips', {}).get('log-level', _logging.ERROR))
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

class MyClipsServerFault(MyClipsServerException, Fault):
    def __init__(self, message="", code=1000, *args, **kwargs):
        MyClipsServerException.__init__(self, message=message, *args, **kwargs)
        Fault.__init__(self, code, "[%s] %s"%(self.__class__.__name__, message), **kwargs)

class ServiceNotFoundFault(MyClipsServerFault):
    def __init__(self, message="", *args, **kwargs):
        MyClipsServerFault.__init__(self, message=message, code=1998, *args, **kwargs)

class InvalidArgTypeError(MyClipsServerFault):
    def __init__(self, funcName="", argNum=None, expectedSkeleton=None, foundClass=None, *args, **kwargs):
        
        message="Function %(funcName)s expects arguments #%(argNum)s to be a %(expected)s, but found %(found)s"%{
                    'funcName' :    funcName,
                    'argNum' :      str(argNum) if argNum is not None else "ALL",
                    'expected' :    str(expectedSkeleton),
                    'found':        str(foundClass)}
        
        MyClipsServerFault.__init__(self, message=message, code=1001, *args, **kwargs)

def __replaceFuncs(_F_REPLACEMENTS):

    # replace some system function definition with a server-proof version:
    
    if len(_F_REPLACEMENTS):
    
        import myclips.functions as _mycfuncs
        
        # manually bootstrap system functions
        _mycfuncs.SystemFunctionBroker.bootstrap()
        
        for _funcInfo in _F_REPLACEMENTS:
    
            logger.info("Replacing: %s", str(_funcInfo))    
    
            _moduleName = "<none>"
            _className = "<none>"    
    
            try:
                # prepare the replacement
                
                _moduleName = _funcInfo['module']
                _className = _funcInfo['class']
                _funcInstance = myclips.newInstance(_className, None, _moduleName)
                _mycfuncs.SystemFunctionBroker.register(_funcInstance, True)
            except:
                logger.critical("Error replacing %s.%s\n%s---------------\n", _moduleName, _className, traceback.format_exc() )
            else:
                # then replace the definition
                logger.info("\t\t...Done")


def __registerFuncs(_F_REGISTERS):

    # replace some system function definition with a server-proof version:
    
    if len(_F_REGISTERS):
    
        import myclips.functions as _mycfuncs
        
        # manually bootstrap system functions
        _mycfuncs.SystemFunctionBroker.bootstrap()
        
        for _funcInfo in _F_REGISTERS:
    
            logger.info("Registering: %s", str(_funcInfo))
            
            _moduleName = "<none>"
            _className = "<none>"    
    
            try:
                # prepare the replacement
                
                _moduleName = _funcInfo['module']
                _className = _funcInfo['class']
                _funcInstance = myclips.newInstance(_className, None, _moduleName)
                _mycfuncs.SystemFunctionBroker.register(_funcInstance, False)
            except:
                logger.critical("Error registering %s.%s\n%s---------------\n", _moduleName, _className, traceback.format_exc() )
            else:
                # then replace the definition
                logger.info("\t\t...Done")


def __removeFuncs(_F_REMOVES):

    # replace some system function definition with a server-proof version:
    
    if len(_F_REMOVES):
    
        import myclips.functions as _mycfuncs
        
        # manually bootstrap system functions
        _mycfuncs.SystemFunctionBroker.bootstrap()
        
        for _funcInfo in _F_REMOVES:
    
            logger.info("Removing: %s", str(_funcInfo))
            try:
                _mycfuncs.SystemFunctionBroker.unregister(_funcInfo)
            except:
                logger.critical("Error removing %s\n%s--------------\n", _funcInfo, traceback.format_exc() )
            else:
                logger.info("\t\t...Done")


__removeFuncs(MYCLIPS_FUNCTIONS_REMOVALS)
__registerFuncs(MYCLIPS_FUNCTIONS_REGISTRATIONS)
__replaceFuncs(MYCLIPS_FUNCTIONS_REPLACEMENTS) 





