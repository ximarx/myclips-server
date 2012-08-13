'''
Created on 10/lug/2012

@author: Francesco Capozzo
'''
import inspect
from myclips_server.xmlrpc.services.Service import Service
from myclips_server.xmlrpc.Broker import Broker

class TypeFactory(Service):
    '''
    Types Factory and Types operator proxy
    '''
    _TYPE = "TypeFactory"
    _NAME = "TypeFactory_TypeFactory"

    def __init__(self, factory, typeRegistry=None):
        '''
        Constructor
        '''
        Service.__init__(self, factory)
        self._typeRegistry = typeRegistry if isinstance(typeRegistry, TypeRegistry) else TypeRegistry.default
    
    def getTypes(self):
        return self._typeRegistry.getTypes()
    
    def newInstance(self, typeName):
        return self._typeRegistry.getSkeleton(typeName)
    
    def getOperators(self, typeName):
        return self._typeRegistry.getTypeOperators(typeName)
    
    def do(self, typeSkeleton, operator, *args):
        return self._typeRegistry.getOperatorImpl(typeSkeleton, operator)(typeSkeleton, *args)
    
    def isInstance(self, typeSkeleton, typeName):
        return (typeSkeleton[0] == typeName)
    
    def getType(self, typeSkeleton):
        return (typeSkeleton[0])
    
class TypeRegistry(object):
    
    default = None
    
    def __init__(self, types=None):
        self._types = {}
        # TYPENAME: {
        #    instance: [],
        #    operators: {},
        #    skeleton_converter: lambda
        #    class_converter: lambda
        #    }
        self._classes_to_types = {}
    
    def addType(self, typeName, typeClass, description=None, skeleton=None, operators=None, skeleton_converter=None, class_converter=None):
        self._types[typeName] = {
                                 'class':       typeClass,
                                 'description': str(description),
                                 "skeleton":    ( typeName, None) if not isinstance(skeleton, tuple) else skeleton,
                                 "operators":   {} if not isinstance(operators, dict) else operators,
                                 "to_skeleton": (lambda t:t) if not callable(skeleton_converter) else skeleton_converter,
                                 "to_class":    (lambda t:t) if not callable(class_converter) else class_converter
                                 }
        self._classes_to_types[".".join([typeClass.__module__, typeClass.__name__])] = typeName

    def setSkeleton(self, typeName, skeleton):
        if isinstance(skeleton, tuple):
            self._types[typeName]['skeleton'] = skeleton
            return True
        return False
    
    def getSkeleton(self, typeName):
        return self._types[typeName]["skeleton"]
        
    def addOperator(self, typeName, operatorName, operatorFunc):
        if callable(operatorFunc):
            self._types[typeName]["operators"][operatorName] = operatorFunc
            return True
        return False
    
    def removeOperator(self, typeName, operatorName):
        del self._types[typeName]["operators"][operatorName]
        
    def setSkeletonConverter(self, typeName, converter):
        if callable(converter):
            self._types[typeName]["to_skeleton"] = converter
            return True
        return False        
    
    def setClassConverter(self, typeName, converter):
        if callable(converter):
            self._types[typeName]["to_class"] = converter
            return True
        return False
    
    def getTypes(self):
        return [(typeName, typeDef['description']) for (typeName, typeDef) in self._types.items()]
    
    def getTypeOperators(self, typeName):
        return [(opName, Broker._vectorizeArgs(opCall), inspect.getdoc(opCall)) for (opName, opCall) in self._types[typeName]["operators"].items()]
    
    def getOperatorImpl(self, typeSkeleton, operator):
        return self._types[typeSkeleton[0]]["operators"][operator]
    
TypeRegistry.default = TypeRegistry()