'''
Created on 14/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
import xmlrpclib
import myclips_server
from myclips_server import FunctionCallTimeout
from myclips_server.xmlrpc.services import sessions

class ClientIO(Service):
    '''
    ClientIO service:
        Allows a client to register one or more input/output streams.
        Allows other services to use registered stream with any interface
        
        
    The client must implement a xmlrpc end-point with at-least the following
    methods:
    
        - Stream.ping(string aReverseToken) : True
            Used by the server to check if stream is valid
            
        - Stream.write(string aReverseToken, string theString) : None
            Used by the server to send data (in string format)
            
        - Stream.writelines(string aReverseToken, list someStrings) : None
            Used by the server to send a list of string
            
        - Stream.close(string aReverseToken) : None
            Used by the server to notify the client about stream unregistering
            
        - Stream.seek(string aReverseToken, int aPosition, int aMode) : Boolean
            Used by the server to move the stream cursor position in the stream
            
        - Stream.readline(string aReverseToken) : String
            Used by the server to read a line from the client stream
            
        - Stream.__call(string aReverseToken, string aMissingMethodName, *args, **kwargs) : mixed
            This method will be called if a required method is missing. 
            If this method is missing too, an XMLRPC Fault will be raised.
            
        A client end-point is still valid if it implements only the .__call method as
        router for others
            
    '''
    
    _TYPE = "ClientIO"
    _NAME = "ClientIO_ClientIO"
    __API__= Service.__API__ + ['register', 'unregister', 'getStreamInfo', 'printTo', 'getStreamNames', '__DOC__']


    def onSessionDestroy(self, aSessionToken):
        '''
        Destory all registered stream for a session
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        '''
        theSessionsService = self._broker.Sessions
        try:
            for theStreamName in self.getStreamNames(aSessionToken):
                try:
                    self.unregister(aSessionToken, theStreamName)
                except:
                    pass
        except:
            pass
        theSessionsService.delProperty(aSessionToken, "ClientIO_ClientIO.streams")
        
    @sessions.renewer
    def getStreamNames(self, aSessionToken):
        '''
        Get a list of all registered stream names for a session
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @return: a list of stream names
        @rtype: list
        '''
        theSessionsService = self._broker.Sessions
        return theSessionsService.getProperty(aSessionToken, "ClientIO_ClientIO.streams", {}).keys()

    @sessions.renewer
    def register(self, aSessionToken, aStreamName, aStreamAddress, aReverseToken):
        '''
        Register a xmlrpc end-point of the client as a stream
        If a stream with the same identifier is already registered,
        it will be unregister and then replaced
        
        The registration protocol requires the client end-point to
        reply to a <client-end-point>.ping(aReverseToken) method call
        before the registration is completed
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aStreamName: the identifier of the stream after the registration
        @type aStreamName: string
        @param aStreamAddress: the url of the xmlrpc server of the client where streams methods will be redirected
        @type aStreamAddress: string
        @param aReverseToken: a <secret-code> the server will send with data to identify a valid transmission 
        @type aReverseToken: mixed
        '''
        
        #theStreamName = "ClientIO_ClientIO.streams.%s"%aStreamName
        theSessionsService = self._broker.Sessions
        
        try:
            self.unregister(aSessionToken, aStreamName)
        except:
            # ignore any error
            pass

        try:
            theStreamsDict = theSessionsService.getProperty(aSessionToken, "ClientIO_ClientIO.streams")
        except:
            theStreamsDict = {}
            theSessionsService.setProperty(aSessionToken, "ClientIO_ClientIO.streams", theStreamsDict)

        theStream = xmlrpclib.Server(aStreamAddress, allow_none=True)

        try:
            myclips_server.timeout_call(theStream.ping, 2, args=(aReverseToken))
        except myclips_server.FunctionCallTimeout:
            myclips_server.logger.info("...a ClientIOStream ping check took more than 2 seconds. Ignored!")
        else:
            theStreamsDict[aStreamName] = ClientIOStream( aReverseToken, theStream)
        
    @sessions.renewer
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
        
        theSessionsService = self._broker.Sessions
        theStreamsDict = theSessionsService.getProperty(aSessionToken, "ClientIO_ClientIO.streams", {})
        
        try:
            theStreamsDict.pop(aStreamName, None).close()
        except:
            # ignore any error
            pass

    @sessions.renewer            
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
        
        theSessionsService = self._broker.Sessions
        
        return repr(theSessionsService.getProperty(aSessionToken, "ClientIO_ClientIO.streams")[aStreamName])
            
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
        
        theSessionsService = self._broker.Sessions
        
        return theSessionsService.getProperty(aSessionToken, "ClientIO_ClientIO.streams")[aStreamName]
    
    @sessions.renewer
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
                #return getattr(self._theServer, name)(self._theReverseToken, *args, **kwargs)
                return myclips_server.timeout_call( getattr(self._theServer.Stream, name), timeout=60, args=[self._theReverseToken] + list(args), kwargs=kwargs) 
            except xmlrpclib.Fault:
                return self._theServer.Stream.__call(self._theReverseToken, name, *args, **kwargs)
            except FunctionCallTimeout:
                myclips_server.logger.warning("...a ClientIOStream request took more than 60 seconds. Aborted")
                raise IOError()
        
        return __forward_call


    def __hasattr__(self, name):
        return True
        
    