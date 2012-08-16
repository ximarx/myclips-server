'''
Created on 14/ago/2012

@author: Francesco Capozzo
'''
from copy import deepcopy

class Skeleton(object):
    
    __CLASS__ = ""
    __PROPERTIES__ = {}
    
    def __init__(self):
        pass
    
    @classmethod
    def sign(cls):
        return "<Skeleton: %s>"%cls.__CLASS__
    
    @property
    def theClass(self):
        return self.__class__.__CLASS__
    
    def new(self, *args, **kwargs):
        theSkeleton = {"class"
                            : self.theClass,
                       "properties"
                            : deepcopy(self.__class__.__PROPERTIES__)}
        
        for (propName, propValue) in kwargs.items():
            if theSkeleton['properties'].has_key(propName):
                theSkeleton['properties'][propName] = propValue

        return theSkeleton
    
            
        
        
    
