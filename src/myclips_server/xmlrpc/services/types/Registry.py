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
    """
    Type Registry service:
        provides api to create skeleton dict from
        skeleton declaration and check if a dict is a Skeleton
    """
    
    _TYPE = "Registry"
    _NAME = "Registry_Registry"
    __API__ = Service.__API__ + ['new', 'getSkeletons', 'isSkeleton', 'isA']
    
    def __init__(self, factory, theSkeletonModule=None):
        Service.__init__(self, factory)
        self._skeletons = {}
        self._setupSkeletons(theSkeletonModule)
    
    def _setupSkeletons(self, theSkeletonsModule = None):
        theSkeletonsModule = theSkeletonsModule or skeletons
        
        for theSkeleton in (getattr(theSkeletonsModule, aSkeleton) for aSkeleton in dir(theSkeletonsModule) 
                                if isinstance(getattr(theSkeletonsModule, aSkeleton), type)
                                    and getattr(theSkeletonsModule, aSkeleton) != Skeleton
                                    and issubclass(getattr(theSkeletonsModule, aSkeleton), Skeleton)):
            self.addSkeleton(theSkeleton) 
    
    def new(self, theType, *args, **kwargs):
        '''
        Create a new Skeleton of type theType.
        If an dict is used as second argument, in the dict are used in the
        Skeleton instance initialization. Dict's values with a key that is
        a valid skeleton properties are used as property value
          
        @param theType: a skeleton type name
            If theType is not a registered skeleton, a skeleton name
            that ends with theType will be used if a single similar
            match is found
        @type theType: string
        @return: a Skeleton of type theType
        @rtype: dict
        '''
        
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
        '''
        Add a new skeleton in the list of registered skeletons
        
        @param aSkeleton: a new skeleton class
        @type aSkeleton: Skeleton.__class__
        '''
        
        assert issubclass(aSkeleton, Skeleton)
        self._skeletons[aSkeleton.__CLASS__] = aSkeleton()

    def getSkeletons(self):
        '''
        Return the list of skeleton registered
        '''
        
        return self._skeletons.keys()

    def _tryReplace(self, aSessionToken, aPropValue ):
        '''
        Try to replace a value with a skeleton for the same type
        '''
        
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
        '''
        Check if a dict is a skeleton instance
        
        @param aDict: a dict to check
        @type aDict: dict
        '''
        
        return isinstance(aDict, dict) \
                and aDict.has_key('class') \
                and aDict.has_key('properties') \
                and self._skeletons.has_key(aDict['class'])
                
                
    def isA(self, aSkeleton, aSkeletonType):
        '''
        Check if a skeleton is of type aSkeletonType
        
        @param aSkeleton: a skeleton dict
        @type aSkeleton: dict
        @param aSkeletonType: a skeleton type name
        @type aSkeletonType: string
        '''
        
        return self.isSkeleton(aSkeleton) \
                and set(aSkeleton['properties'].keys()).issuperset( set(self._skeletons[aSkeletonType].__PROPERTIES__.keys()))
        
                
    def toSkeleton(self, aSkeletonable):
        '''
        Convert a value to its skeleton form (if possible)
        lists and non-skeleton dicts values are converted too
        
        @param aSkeletonable: an object to convert
        @type aSkeletonable: object
        @return: a Skeleton for the object if possible
            or the same object if can't be replaced
        @rtype: object|dict
        '''
        
        if isinstance(aSkeletonable, (list, tuple)):
            
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
        '''
        Convert a skeleton to its real object. the session token
        is used to retrive parameters from the session if necessary
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aSkeleton: a skeleton instance to convert
        @type aSkeleton: dict
        @return: the converted object
        @rtype: object
        '''
        
        
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
            theEngineService = self._broker.Engine
            theNetwork = theEngineService.getNetwork(aSessionToken)
                
            assert isinstance(theNetwork, Network)
            aSkeleton['properties']['modulesManager'] = theNetwork.modulesManager
            

        return theClass(**aSkeleton['properties'])
            
        
class NothingToReplaceException(Exception):
    '''
    Registry internal exception raised to notify
    no value replacement while converting
    concrete -> skeleton
    '''
    pass