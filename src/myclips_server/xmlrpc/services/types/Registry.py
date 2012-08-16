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
import myclips_server


class Registry(Service):
    
    _TYPE = "Registry"
    _NAME = "Registry_Registry"
    __API__ = ['ping', 'new', 'getSkeletons', 'isSkeleton']
    
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
            
        try:
            return self._skeletons[theType].new(*args, **kwargs)
        except KeyError:
            # the exact theType can't be found,
            # i try to resolve using last part only
            theType = theType.split('.')
            alternatives = []
            for aKey in self.getSkeletons():
                if aKey.split('.')[-len(theType):None] == theType:
                    alternatives.append(aKey)
            if len(alternatives) == 1:
                return self._skeletons[alternatives[0]].new(*args, **kwargs)
            else:
                raise
    
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
                    aPropValue[index] = self._tryReplace(aSessionToken, item)
                    needReturn = True
                except NothingToReplaceException:
                    continue
                
        elif isinstance(aPropValue, dict):
            # check if it's a skeleton
            if self.isSkeleton(aPropValue):
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
                        
    #def concretize(self, aSessionToken, aSkeleton):
    #    return repr(self.toConcrete(aSessionToken, aSkeleton))
    
    def isSkeleton(self, aDict):
        
        return isinstance(aDict, dict) \
                and aDict.has_key('class') \
                and aDict.has_key('properties') \
                and self._skeletons.has_key(aDict['class'])
                
                
    def isA(self, aSkeleton, aSkeletonType):
        
        return self.isSkeleton(aSkeleton) \
                and set(aSkeleton['properties'].keys()).issuperset( set(self._skeletons[aSkeletonType].__PROPERTIES__.keys()))
        
                
    def toSkeleton(self, aSkeletonable):
        
        if isinstance(aSkeletonable, list):
            
            return [self.toSkeleton(x) for x in aSkeletonable]
        
        elif isinstance(aSkeletonable, dict):
            
            if self.isSkeleton(aSkeletonable):
                return aSkeletonable
            else:
                return dict([ (aKey, self.toSkeleton(aValue)) for (aKey,aValue) in aSkeletonable.items()]) 
            
        else:
            try:
                theType = "%s.%s"%(aSkeletonable.__module__,aSkeletonable.__class__.__name__)
                
                if self._skeletons.has_key(theType):
                    theSkeleton = self.new(theType)
                    
                    for aProp in theSkeleton['properties'].keys():
                        if hasattr(aSkeletonable, aProp):
                            anAttr = getattr(aSkeletonable, aProp)
                            if callable(anAttr):
                                continue
                            theSkeleton['properties'][aProp] = self.toSkeleton(anAttr)
                    
                    return theSkeleton
                            
                else:
                    myclips_server.logger.warning("Not convertible: %s\n\t%s", theType, repr(aSkeletonable))
                    # unconvertible
                    return aSkeletonable
            except:
                
                myclips_server.logger.debug("Used as base-type: %s", repr(aSkeletonable))
                
                # for base types an exception is raised by .__module__
                return aSkeletonable

        

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
            theNetwork = theEngineService.getNetwork(aSessionToken)
                
            assert isinstance(theNetwork, Network)
            aSkeleton['properties']['modulesManager'] = theNetwork.modulesManager
            

        return theClass(**aSkeleton['properties'])
            
        
class NothingToReplaceException(Exception):
    pass