'''
Created on 08/lug/2012

@author: Francesco Capozzo
'''
from myclips.rete.Network import Network

class MyClipsWrapper(object):
    '''
    classdocs
    '''

    __i = None

    def __init__(self):
        '''
        Constructor
        '''
        self.network = Network()

    @classmethod
    def i(cls):
        if cls.__i == None:
            cls.__i = cls()
        return cls.__i