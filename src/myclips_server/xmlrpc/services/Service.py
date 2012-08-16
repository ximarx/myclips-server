'''
Created on 15/lug/2012

@author: Francesco Capozzo
'''

class Service(object):
    '''
    Base class for myclips-xmlrpc-server services
    '''

    _TYPE = "Service"
    _NAME = "Service_Service"
    __API__ = ['ping', '__repr__', '__DOC__']

    def __init__(self, factory):
        '''
        Constructor
        '''
        self._factory = factory
        self._broker = None
        
    def __repr__(self):
        return "<Service: %s>"%self._NAME
        
    def _onInitCompleted(self):
        pass
    
    def onSessionDestroy(self, aSessionToken):
        '''
        Called by the Sessions service to notify other services
        about session's destroy() method call
        
        This hook should be used for any kind of
        resource cleanup
        '''
        pass
        
    def setBroker(self, theBroker):
        self._broker = theBroker
        
    def ping(self, aSessionToken=None):
        """
        Check if service is available for the session aSession
        If no Sessions service is installed, ping always return "PONG!"
        
        @param aSessionToken : an optional session Token from the Sessions service
        @type aSessionToken : string
        @return: "PONG!" if service is available, False otherwise
        @rtype: boolean|"PONG!"
        """
        
        try:
            return "PONG!" if self._broker.Sessions.isValid(aSessionToken) else False
        except:
            return "PONG!"