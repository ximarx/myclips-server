'''
Created on 14/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
import xmlrpclib

class ClientIO(Service):
    '''
    classdocs
    '''
    
    _TYPE = "ClientIO"
    _NAME = "ClientIO_ClientIO"
    __API__= ['register', 'unregister', 'getStreamInfo', 'printTo']


    def register(self, aSessionToken, aStreamName, aStreamAddress, aReverseToken):
        
        theStreamName = "ClientIO_ClientIO.streams.%s"%aStreamName
        theSessionsService = self._factory.instance('Sessions')
        
        try:
            theSessionsService.getProperty(aSessionToken, theStreamName, None).close()
        except:
            # ignore any error
            pass

        theStream = xmlrpclib.Server(aStreamAddress, allow_none=True)
        theStream.ping(aReverseToken)
        
        theSessionsService.setProperty(aSessionToken, theStreamName, ClientIOStream( aReverseToken, theStream))
        
    def unregister(self, aSessionToken, aStreamName):
        theStreamName = "ClientIO_ClientIO.streams.%s"%aStreamName
        theSessionsService = self._factory.instance('Sessions')
        
        try:
            theSessionsService.getProperty(aSessionToken, theStreamName, None).close()
        except:
            # ignore any error
            pass
            
        theSessionsService.delProperty(aSessionToken, theStreamName)
        
    def getStreamInfo(self, aSessionToken, aStreamName):
        theStreamName = "ClientIO_ClientIO.streams.%s"%aStreamName
        theSessionsService = self._factory.instance('Sessions')
        
        return repr(theSessionsService.getProperty(aSessionToken, theStreamName))
            
        
    def getStream(self, aSessionToken, aStreamName):
        theStreamName = "ClientIO_ClientIO.streams.%s"%aStreamName
        theSessionsService = self._factory.instance('Sessions')
        
        return theSessionsService.getProperty(aSessionToken, theStreamName)
    
    def printTo(self, aSessionToken, aStreamName, aMessage):
        self.getStream(aSessionToken, aStreamName).write(aMessage + "\n")
        
    
class ClientIOStream(object):
    def __init__(self, theReverseToken, theServer):
        self._theReverseToken = theReverseToken
        self._theServer = theServer
        
    def __repr__(self):
        return "<ClientIOStream %s>"%repr(self._theServer)
    
    def __getattr__(self, name):
        return lambda *args, **kwargs: getattr(self._theServer, name)(self._theReverseToken, *args, **kwargs)

    def __hasattr__(self, name):
        return True
        
    