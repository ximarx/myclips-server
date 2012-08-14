'''
Created on 14/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.Broker import Broker
from myclips_server.xmlrpc.services.Service import Service
from myclips_server.xmlrpc.services.types.Skeleton import Skeleton
from myclips_server.xmlrpc.services.types import skeletons

class Registry(Service):
    
    _TYPE = "Registry"
    _NAME = "Registry_Registry"
    __API__ = ['ping', 'new', 'getSkeletons']
    
    default = None
    
    def __init__(self, types=None):
        self._skeletons = {}
        self._setupSkeletons()
    
    def _setupSkeletons(self, theSkeletonsModule = None):
        theSkeletonsModule = theSkeletonsModule or skeletons
        
        for theSkeleton in (getattr(theSkeletonsModule, aSkeleton) for aSkeleton in dir(theSkeletonsModule) 
                                if isinstance(getattr(theSkeletonsModule, aSkeleton), type)
                                    and getattr(theSkeletonsModule, aSkeleton) != Skeleton
                                    and issubclass(getattr(theSkeletonsModule, aSkeleton), Skeleton)):
            self.addSkeleton(theSkeleton) 
    
    def new(self, theType, *args, **kwargs):
        
        if len(args) > 0 and isinstance(args[0], dict) and len(kwargs) == 0:
            kwargs = args[0]
            args = args[1:]
        
        return self._skeletons[theType].new(*args, **kwargs)
    
    def addSkeleton(self, aSkeleton):
        assert issubclass(aSkeleton, Skeleton)
        self._skeletons[aSkeleton.__CLASS__] = aSkeleton()

    def getSkeletons(self):
        return self._skeletons.keys()

    
