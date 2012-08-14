'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
import time
import uuid
import threading

class Sessions(Service):
    '''
    Manage sessions
    '''
    _TYPE = "Sessions"
    _NAME = "Sessions_Sessions"
    __API__ = ["ping", "new", "renew", "destroy",
                'setProperty', "getProperty", "isValid"]
    
    def __init__(self, factory):
        Service.__init__(self, factory)
        
        self._lock = threading.RLock()
        
        self._sessions = {}
    
    def new(self):
        """
        Create a new Session and return the session token
        
        @return: aSessionToken for the new session
        @rtype: string
        """
        with self._lock:
            aSession = Session(self._generateToken())
            self._sessions[aSession.token] = aSession
            return aSession.token
    
    def renew(self, aSessionToken):
        """
        Set a new session expiration time.
        The session will last after another 5 minutes
        Return True on success
        
        @param aSessionToken: a valid session token
        @type aSessionToken: string
        @return: True if session renewed, False otherwise
        @rtype: boolean
        """
        try:
            self.get(aSessionToken).setParam('expiration', int(time.time()) + 5 * 60 )
            return True
        except:
            return False
    
    def destroy(self, aSessionToken):
        """
        Destroy a session before the expiration
        
        @param aSessionToken: a valid session token
        @type aSessionToken: string
        @return: True if session destroyed, False if aSessionToken is invalid
        @rtype: boolean
        """
        with self._lock:
            try:
                del self._sessions[aSessionToken]
                return True
            except:
                return False
    
    def setProperty(self, aSessionToken, aProperty, aValue):
        """
        Set a value aValue for the property aProperty
        in the session with token aSessionToken
        
        @param aSessionToken: a valid session token
        @type aSessionToken: string
        @param aProperty: a property name
        @type aProperty: string
        @param aValue: a property value
        @type aValue: mixed 
        """
        self.get(aSessionToken).setProperty(aProperty, aValue)
    
    def getProperty(self, aSessionToken, aProperty):
        """
        Get a property value for the property aProperty
        in the session with token aSessionToken
        
        @param aSessionToken: a valid session token
        @type aSessionToken: string
        @param aProperty: a property name
        @type aProperty: string
        @return: the property value or None if property is not set
        @rtype: mixed|None
        @raise KeyError: if aSessionToken is invalid
        """
        return self.get(aSessionToken).getProperty(aProperty, None)
    
    def isValid(self, aSessionToken):
        """
        Return True if aSessionToken is a valid token for
        a registered session
        
        @param aSessionToken: a token to check
        @type aSessionToken: string
        @return: True if valid, False otherwise
        @rtype: boolean
        """
        with self._lock:
            return self._sessions.has_key(aSessionToken)
    
    def get(self, aSessionToken):
        """
        Get the Session object for the token aSessionToken
        (thread-safe)
        
        @param aSessionToken: a valid token
        @type aSessionToken: string
        @return: the session with token aSessionToken
        @rtype: Session
        @raise KeyError: if aSessionToken is invalid
        """
        with self._lock:
            return self._sessions[aSessionToken]
    
    def _generateToken(self):
        """
        Generate and return a unique guid
        that can be used as session token
        """
        aToken = None
        while aToken is None or self._sessions.has_key(aToken):
            aToken = str(uuid.uuid4())
        return aToken
        
    
        
class Session(object):
    def __init__(self, aSessionToken):
        self._token = aSessionToken
        self._epoch = int(time.time())
        self._params = {"expiration" 
                            : self._epoch + 5 * 60 # default expiration is epoch + 5 minutes
                        }
        self._properties = {}
        
    @property
    def token(self):
        return self._token

    @property
    def epoch(self):
        return self._epoch
    
    def renew(self):
        self._epoch = int(time.time())
        
    def setProperty(self, propName, propValue):
        self._properties[propName] = propValue
        
    def getProperty(self, propName, defaultValue=None):
        return self._properties.get(propName, defaultValue)
    
    def setParam(self, paramName, paramValue):
        self._params[paramName] = paramValue
        
    def getParam(self, paramName, defaultValue=None):
        return self._params.get(paramName, defaultValue)
    
    def __hash__(self):
        return hash(self._token)
    
    def __eq__(self, other):
        return isinstance(other, self.__class__)\
                and other.token == self.token
                
    def __neq__(self, other):
        return not self.__eq__(other)
