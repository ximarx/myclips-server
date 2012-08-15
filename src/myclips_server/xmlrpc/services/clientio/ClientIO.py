'''
Created on 14/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
import xmlrpclib

class ClientIO(Service):
    '''
    ClientIO service:
        Allows a client to register one or more input/output streams.
        Allows other services to use registered stream with any interface
        
        
    The client must implement a xmlrpc end-point with at-least the following
    methods:
    
        - .ping(string aReverseToken) : True
            Used by the server to check if stream is valid
            
        - .write(string aReverseToken, string theString) : None
            Used by the server to send data (in string format)
            
        - .writelines(string aReverseToken, list someStrings) : None
            Used by the server to send a list of string
            
        - .close(string aReverseToken) : None
            Used by the server to notify the client about stream unregistering
            
        - .seek(string aReverseToken, int aPosition, int aMode) : Boolean
            Used by the server to move the stream cursor position in the stream
            
        - .readline(string aReverseToken) : String
            Used by the server to read a line from the client stream
            
        - .__call(string aReverseToken, string aMissingMethodName, *args, **kwargs) : mixed
            This method will be called if a required method is missing. 
            If this method is missing too, an XMLRPC Fault will be raised.
            
        A client end-point is still valid if it implements only the .__call method as
        router for others
            
    '''
    
    _TYPE = "ClientIO"
    _NAME = "ClientIO_ClientIO"
    __API__= ['register', 'unregister', 'getStreamInfo', 'printTo']


    def register(self, aSessionToken, aStreamName, aStreamAddress, aReverseToken):
        '''
        Register a xmlrpc end-point of the client as a stream
        If a stream with the same identifier is already registered,
        it will be unregister and then replaced
        
        The registration protocol requires the client end-point to
        reply to a <client-end-point>.ping(aReverseToken) method call
        before the registration will be completed
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aStreamName: the identifier of the stream after the registration
        @type aStreamName: string
        @param aStreamAddress: the url of the xmlrpc server of the client where streams methods will be redirected
        @type aStreamAddress: string
        @param aReverseToken: a <secret-code> the server will send with data to identify a valid transmission 
        @type aReverseToken: mixed
        '''
        
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
        '''
        Remove a registered stream.
        
        The method <client-end-point>.close(aReverseToken) will be call
        before stream removal (as notification). The removal will
        take place even in case of close-call failure 
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aStreamName: the identifier of the stream to remove
        @type aStreamName: string
        @raise KeyError: if aStreamName is not a valid stream identifier
        '''
        
        theStreamName = "ClientIO_ClientIO.streams.%s"%aStreamName
        theSessionsService = self._factory.instance('Sessions')
        
        try:
            theSessionsService.getProperty(aSessionToken, theStreamName, None).close()
        except:
            # ignore any error
            pass
            
        theSessionsService.delProperty(aSessionToken, theStreamName)
        
    def getStreamInfo(self, aSessionToken, aStreamName):
        '''
        Return the repr() string for the stream idenfitied by aStreamName
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aStreamName: a valid stream identifier
        @type aStreamName: string
        @return: representation of the stream object
        @rtype: string 
        @raise KeyError: if aStreamName or aSessionToken are invalid
        '''
        
        theStreamName = "ClientIO_ClientIO.streams.%s"%aStreamName
        theSessionsService = self._factory.instance('Sessions')
        
        return repr(theSessionsService.getProperty(aSessionToken, theStreamName))
            
        
    def getStream(self, aSessionToken, aStreamName):
        '''
        Return a ClientIOStream instance for the aStreamName identifier
        @param aSessionToken: a valid session token
        @type aSessionToken: string
        @param aStreamName: a valid stream identifier
        @type aStreamName: string
        @return: the ClientIOStream instance for the stream identifier
        @rtype: ClientIOStream
        '''
        
        theStreamName = "ClientIO_ClientIO.streams.%s"%aStreamName
        theSessionsService = self._factory.instance('Sessions')
        
        return theSessionsService.getProperty(aSessionToken, theStreamName)
    
    def printTo(self, aSessionToken, aStreamName, aMessage):
        '''
        Helper method to send a message to a stream
        
        @deprecated
        '''
        
        self.getStream(aSessionToken, aStreamName).write(aMessage + "\n")
        
    
class ClientIOStream(object):
    """
    Wrapper for a remove client stream
    """
    def __init__(self, theReverseToken, theServer):
        self._theReverseToken = theReverseToken
        self._theServer = theServer
        
    def __repr__(self):
        return "<ClientIOStream %s>"%repr(self._theServer)
    
    def __getattr__(self, name):
        def __forward_call(*args, **kwargs):
            try:
                return getattr(self._theServer, name)(self._theReverseToken, *args, **kwargs)
            except xmlrpclib.Fault:
                return self._theServer.__call(self._theReverseToken, name, *args, **kwargs)
        
        return __forward_call


    def __hasattr__(self, name):
        return True
        
    