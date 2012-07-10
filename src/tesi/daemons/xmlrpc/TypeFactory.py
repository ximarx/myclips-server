'''
Created on 10/lug/2012

@author: Francesco Capozzo
'''

class TypeFactory(object):
    '''
    Factory of MyClips types
    '''


    def __init__(self, typesDict=None, typesIter=None):
        '''
        Constructor
        '''
        self._types = {}
        if typesDict != None:
            self._types.update(typesDict)
        if typesIter != None:
            for clsIns in typesIter:
                self.addType(clsIns)
        
        
    def getNew(self, ClassName, *args, **kargs):
        try:
            print "New instance {0} with: {1}, {2}".format(ClassName, args, kargs)
            return self._types[ClassName](*args, **kargs)
        except KeyError:
            raise TypeNotFoundError("Type not found: "+repr(ClassName))
    
    def getType(self, ClassName):
        try:
            print "Getting Type {0}".format(ClassName)
            return self._types[ClassName]
        except KeyError:
            raise TypeNotFoundError("Type not found: "+repr(ClassName))
    
    def addType(self, ClassInstance):
        print "Adding type: {0} => {1}".format(ClassInstance.__name__, repr(ClassInstance))
        self._types[ClassInstance.__name__] = ClassInstance
        
        
class TypeNotFoundError(Exception):
    pass