'''
Created on 15/lug/2012

@author: Francesco Capozzo
'''
from tesi.daemons.xmlrpc.Service import Service
import time

class SessionsManager(Service):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def ping(self):
        return "PONG"
    
    def newToken(self):
        return ("token", str(time.time()))