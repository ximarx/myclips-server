'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service

class Network(Service):
    '''
    Bridge to the myclips.rete.Network api
    '''

    _TYPE = "Network"
    _NAME = "Network_MyClips"
