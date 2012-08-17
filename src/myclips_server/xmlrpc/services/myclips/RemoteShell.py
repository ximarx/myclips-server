'''
Created on 14/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
from myclips.shell.Interpreter import Interpreter
from myclips_server.xmlrpc.services import sessions

class RemoteShell(Service):
    '''
    MyClips RemoteShell service:
        allow to execute "CLIPS commands" over a Network Instance
        
        For documentation about allowed commands, use the MyClips's Shell documentation.
        
        WARNING: output/input streams must be registered with
            ClientIO service before any method of this service is called,
            otherwise any input request will have EOF as return value
            and any output will be suppressed
    '''
    
    _NAME = 'RemoteShell_MyClipsShell'
    _TYPE = 'RemoteShell'
    __API__ = Service.__API__ + ['do']

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
        
    @sessions.renewer
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
        
    @sessions.renewer
    def destroy(self, aSessionToken):
        '''
        Destroy a shell (if any)
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        '''
        
        try:
            theSessionsService = self._broker.Sessions
            theSessionsService.delProperty(aSessionToken, 'RemoteShell_MyClipsShell.shell')
        finally:
            return True
