'''
Created on 14/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
from myclips.shell.Interpreter import Interpreter

class RemoteShell(Service):
    '''
    classdocs
    '''
    
    _NAME = 'RemoteShell_MyClipsShell'
    _TYPE = 'RemoteShell'
    __API__=['do']

    def __init__(self, factory):
        Service.__init__(self, factory)
        
    def getShell(self, aSessionToken):
        
        theSessionsService = self._broker.Sessions
        theShell = theSessionsService.getProperty(aSessionToken, 'RemoteShell_MyClipsShell.shell', None) 
        if theShell is None:
            
            theEngineService = self._broker.Engine
            theNetwork = theEngineService.getNetwork(aSessionToken)
            theShell = Interpreter(theNetwork, None)
            theSessionsService.setProperty(aSessionToken, 'RemoteShell_MyClipsShell.shell', theShell)
            
        return theShell
        
        
    def do(self, aSessionToken, aCommand):
        '''
        Execute a command and return the results
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aCommand: a command to be executed in the shell
        @type aCommand: string
        @return: the repr() of return value
        @rtype: string
        '''
        
        theShell = self.getShell(aSessionToken)
        
        assert isinstance(theShell, Interpreter)
        
        theRegistryService = self._broker.Registry
        
        return theRegistryService.toSkeleton(theShell.evaluate(aCommand))
        
        
    