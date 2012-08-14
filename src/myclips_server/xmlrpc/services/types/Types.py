'''
Created on 10/lug/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service


class Types(Service):
    '''
    Types Factory and Types operator proxy
    '''
    _TYPE = "Types"
    _NAME = "Types_Types"
    __API__ = ['newDict', "newDict2"]
    
    def __init__(self, factory):
        '''
        Constructor
        '''
        Service.__init__(self, factory)
        self._registry = None
        #self._typeRegistry = typeRegistry if isinstance(typeRegistry, Registry) else Registry.default
        
    def getRegistry(self):
        if self._registry is None:
            self._registry = self._factory.instance("Registry")
        return self._registry
    
    def getTypes(self):
        return self._registry.getTypes()
    
    def newInstance(self, typeName):
        return self._registry.getSkeleton(typeName)
    
    def getOperators(self, typeName):
        return self._registry.getTypeOperators(typeName)
    
    def do(self, typeSkeleton, operator, *args):
        return self._registry.getOperatorImpl(typeSkeleton, operator)(typeSkeleton, *args)
    
    def isInstance(self, typeSkeleton, typeName):
        return (typeSkeleton[0] == typeName)
    
    def getType(self, typeSkeleton):
        return (typeSkeleton[0])
    
    def newDict2(self):
        theRegistryService = self._factory.instance("Registry")
        return theRegistryService.new("myclips.parser.Types.Symbol", "CIAO") 
    
    def newDict(self):
        return {"class" 
                    : "myclips.parser.Types.DefRuleConstruct",
                "properties"
                    : {"lhs" 
                            : [{"class"
                                    : "myclips.parser.Types.PatternCE",
                                "properties"
                                    : {}}]}}
        
        
