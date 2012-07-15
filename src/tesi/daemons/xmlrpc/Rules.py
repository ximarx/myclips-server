'''
Created on 15/lug/2012

@author: Francesco Capozzo
'''
from tesi.daemons.xmlrpc.Service import Service

class Rules(Service):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def ping(self):
        return "PONG"
    
    def addRule(self, ruleSkeleton):
        return False

    def removeRule(self, ruleName=None, ruleSkeleton=None):
        return False
    
    def getRules(self):
        return []
    
    def getRule(self, ruleName=None):
        return []