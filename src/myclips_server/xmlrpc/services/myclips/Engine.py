'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
from myclips.rete.Network import Network

class Engine(Service):
    '''
    Bridge to the myclips.rete.Network api
    '''

    _TYPE = "Engine"
    _NAME = "Engine_MyClips"
    __API__ = ['ping']
    
    def getNetwork(self, aSessionToken):
        
        theSessionsService = self._factory.instance('Sessions')
        theNetwork = theSessionsService.getProperty(aSessionToken, 'Engine_MyClips.network', None) 
        if theNetwork is None:
            theNetwork = Network()
            theSessionsService.setProperty(aSessionToken, 'Engine_MyClips.network', theNetwork)
            
        return theNetwork
    
    

    