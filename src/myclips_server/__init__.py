import traceback
import logging as _logging
import sys
import os
import json
from xmlrpclib import Fault
import threading

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

class FunctionCallTimeout(Exception):
    pass

def timeout_call(func, timeout=10, args=(), kwargs={}, forward_exc=False):
    """This function will spawn a thread and run the given function
    using the args, kwargs and return the given default value if the
    timeout_duration is exceeded.
    """ 
    class InterruptableThread(threading.Thread):
        def __init__(self):
            self.result = None
            threading.Thread.__init__(self)
            
            
        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except:
                if forward_exc:
                    raise
                else:
                    pass
            
    it = InterruptableThread()
    it.daemon = True
    it.start()
    it.join(timeout)
    if it.isAlive():
        raise FunctionCallTimeout()
    else:
        return it.result







