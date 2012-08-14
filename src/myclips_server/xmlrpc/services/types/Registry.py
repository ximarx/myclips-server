'''
Created on 14/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
from myclips_server.xmlrpc.services.types.Skeleton import Skeleton
from myclips_server.xmlrpc.services.types import skeletons
import importlib
import myclips.parser.Types as types
from myclips.rete.Network import Network


class Registry(Service):
    
    _TYPE = "Registry"
    _NAME = "Registry_Registry"
    __API__ = ['ping', 'new', 'getSkeletons', 'concretize']
    
    default = None
    
    def __init__(self, factory, types=None):
        Service.__init__(self, factory)
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

    def _tryReplace(self, aSessionToken, aPropValue ):
        
        needReturn = False
        
        if isinstance(aPropValue, list):
            # iterate items
            for (index, item) in enumerate(aPropValue):
                try:
                    aPropValue[index] = self._tryReplace(item)
                    needReturn = True
                except NothingToReplaceException:
                    continue
                
        elif isinstance(aPropValue, dict):
            # check if it's a skeleton
            if aPropValue.has_key('class') and self._skeletons.has_key(aPropValue['class']):
                # it's a skeleton, convert it!
                return self.toConcrete(aSessionToken, aPropValue)
            
            else:
                # convert all items
                for (innerKey, innerValue) in aPropValue.items():
                    try:
                        aPropValue[innerKey] = self._tryReplace(aSessionToken, innerValue)
                        needReturn = True
                    except NothingToReplaceException:
                        continue
        
        if needReturn:
            return aPropValue
        else:
            raise NothingToReplaceException()
                        
    def concretize(self, aSessionToken, aSkeleton):
        return repr(self.toConcrete(aSessionToken, aSkeleton))

    def toConcrete(self, aSessionToken, aSkeleton):
        
        theClass = aSkeleton['class']
        theModule = ".".join(theClass.split('.')[0:-1])
        theClass = theClass.split('.')[-1]
        
        theModule = importlib.import_module(theModule)
        theClass = getattr(theModule, theClass)
        
        # try to resolve all parameters (inner skeleton -> types)
        for (propName, propValue) in aSkeleton['properties'].items():
            try:
                aSkeleton['properties'][propName] = self._tryReplace(aSessionToken, propValue)
            except NothingToReplaceException:
                continue
        
        
        # if the types requires the modulesManager, inject its in the parameters
        if issubclass(theClass, types.HasScope):
            # need to fetch the modulesManager linked to the network from the session
            theEngineService = self._factory.instance('Engine')
            print theEngineService 
            theNetwork = theEngineService.getNetwork(aSessionToken)
                
            assert isinstance(theNetwork, Network)
            aSkeleton['properties']['modulesManager'] = theNetwork.modulesManager
            
        print "TheClass: ", theClass
        print "__init__ params: ", aSkeleton['properties']

        return theClass(**aSkeleton['properties'])
            
        
class NothingToReplaceException(Exception):
    pass