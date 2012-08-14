'''
Created on 15/lug/2012

@author: Francesco Capozzo
'''

class Service(object):
    '''
    classdocs
    '''

    _TYPE = "Service"
    _NAME = "Service_Service"

    def __init__(self, factory):
        '''
        Constructor
        '''
        self._factory = factory
        self._broker = None
        
    def _onInitCompleted(self):
        pass
        
    def setBroker(self, theBroker):
        self._broker = theBroker
        
    def ping(self, aSession=None):
        """
        Check if service is available for the session aSession
        
        @param aSessions: an optional session Token from the Sessions service
        @type aSession: aSession skeleton
        @return: "PONG" if service is available
        @rtype: string
        """
        return "PONG"