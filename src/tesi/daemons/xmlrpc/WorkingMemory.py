'''
Created on 15/lug/2012

@author: Francesco Capozzo
'''
from tesi.daemons.xmlrpc.Service import Service

class WorkingMemory(Service):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def ping(self):
        '''
        Check if service is available from client
        @return PONG
        '''
        return "PONG"
    
    def assertFact(self, factSkeleton):
        return False
    
    def retractFact(self, factId=None, factSkeleton=None):
        return False
    
    def getFacts(self):
        return []
    
    def getFactSkeleton(self, factId):
        return []
    
    def getFactInfo(self, factId=None, factSkeleton=None):
        return ""