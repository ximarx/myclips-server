'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
import time

class Sessions(Service):
    '''
    Manage sessions
    '''
    _TYPE = "Sessions"
    _NAME = "Sessions_Sessions"
    
    def new(self):
        return time.asctime()
    
    def renew(self, aSession):
        return time.asctime()
    
    def destroy(self, aSession):
        return True
    
    def setParam(self, aSession, aParam, aValue):
        return True
    
    def getParam(self, aSession):
        return True
    
    def isValid(self, aSession):
        return True
    
        
        
    
