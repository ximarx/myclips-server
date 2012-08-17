'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
import time
import uuid
import threading
from myclips_server import MyClipsServerFault, MyClipsServerException
import myclips_server

class Sessions(Service):
    '''
    Manage sessions
    '''
    _TYPE = "Sessions"
    _NAME = "Sessions_Sessions"
    __API__ = ["ping", "new", "renew", "destroy",
                'setProperty', "getProperty", "isValid"]
    
    try:
        _SESSION_LIFE = max([myclips_server.CONFIGURATIONS['services']['Sessions_Sessions']['session-life'], 10])
    except:
        _SESSION_LIFE = 5 * 60
    
    def __init__(self, factory):
        Service.__init__(self, factory)
        self._lock = threading.RLock()
        self._sessions = {}
        self._cleaner = None
    
    def _initCleaner(self):
        if self._cleaner is None:
            self._cleaner = SessionsCleaner(keysMaker=lambda *args: self._sessions.keys(),
                                            destroyer=self.destroy,
                                            lockObject=self._lock,
                                            timeLeft=lambda s: self.get(s).getParam('expiration') - time.time())
            self._cleaner.daemon = True
            self._cleaner.start()
            myclips_server.logger.info("Sessions cleanup thread started with %d expiration time...", Sessions._SESSION_LIFE)
    
    def new(self):
        """
        Create a new Session and return the session token
        
        @return: aSessionToken for the new session
        @rtype: string
        """
        
        self._initCleaner()
        
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
            self.get(aSessionToken).setParam('expiration', int(time.time()) + Sessions._SESSION_LIFE )
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
                for serviceName in self._factory.services():
                    try:
                        myclips_server.timeout_call(self._factory.instance(serviceName).onSessionDestroy, 2, args=(aSessionToken))
                    except MyClipsServerException:
                        pass
                    
            except myclips_server.FunctionCallTimeout:
                myclips_server.logger.warning("Session cleanup took more than 2 seconds...")
                pass
            
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
    
    def getProperty(self, aSessionToken, aProperty, *args):
        """
        Get a property value for the property aProperty
        in the session with token aSessionToken
        
        @param aSessionToken: a valid session token
        @type aSessionToken: string
        @param aProperty: a property name
        @type aProperty: string
        @return: the property value or None if property is not set
        @rtype: mixed|None
        @raise KeyError: if property name is missing
        @raise InvalidSessionError: if aSessionToken is not valid
        """
        if len(args):
            return self.get(aSessionToken).getProperty(aProperty, args[0])
        else:
            return self.get(aSessionToken).getProperty(aProperty)
    
    def delProperty(self, aSessionToken, aProperty):
        """
        remove a property from the session with token aSessionToken
        
        @param aSessionToken: a valid session token
        @type aSessionToken: string
        @param aProperty: a property name
        @type aProperty: string
        @raise KeyError: if aSessionToken is invalid
        """
        return self.get(aSessionToken).delProperty(aProperty)
    
    
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
        try:
            with self._lock:
                return self._sessions[aSessionToken]
        except KeyError:
            raise InvalidSessionError("Invalid token: %s"%aSessionToken)
    
    def _generateToken(self):
        """
        Generate and return a unique guid
        that can be used as session token
        """
        aToken = None
        while aToken is None or self._sessions.has_key(aToken):
            aToken = str(uuid.uuid4())
        return aToken
        
    
class InvalidSessionError(MyClipsServerFault):
    def __init__(self, message="", *args, **kwargs):
        MyClipsServerFault.__init__(self, message=message, code=1002, *args, **kwargs)
    
class SessionsCleaner(threading.Thread):
    
    def __init__(self, keysMaker=lambda *args:[], 
                        destroyer=lambda *args:None,
                        lockObject=None,
                        timeLeft=lambda s:0,
                        group=None, target=None, name=None, args=(), kwargs=None, verbose=None
                    ):
        
        self._keysMaker = keysMaker
        self._destroyer = destroyer
        self._lockObject = lockObject
        self._timeLeft = timeLeft
        self._nextLoop = Sessions._SESSION_LIFE + 10
        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
                
    def run(self):
        while True:
            time.sleep(self._nextLoop)
            
            myclips_server.logger.info("Session cleanup")
            
            removed = 0
            errors = 0
            
            with self._lockObject:
                self._nextLoop = Sessions._SESSION_LIFE
                
                myclips_server.logger.debug("\tKeys: %s", repr(self._keysMaker()))
                for aKey in self._keysMaker():
                    try:
                        timeLeft = self._timeLeft(aKey)
                        myclips_server.logger.debug("\tKey: %s", aKey)
                        myclips_server.logger.debug("\tTime-Left: %d", timeLeft)
                        if timeLeft <= 0:
                            # destroy the session
                            self._destroyer(aKey)
                            removed += 1
                        else:
                            if self._nextLoop > timeLeft:
                                self._nextLoop = timeLeft
                    except:
                        # if error found, try to destroy
                        errors += 1
                        try:
                            self._destroyer(aKey)
                            removed += 1
                        except:
                            # destroyer failed
                            # log this problem
                            errors += 1
                            myclips_server.logger.critical("A session can't be destroyed: %s", aKey)
                            # this count as double problem!
                            pass
                        
            # increment the next-loop-iteration delta by 10 seconds
            self._nextLoop += 10
            
            myclips_server.logger.info("\t ... cleanup finished. %d destroyed. %d errors. Next iteration in: %d seconds", removed, errors, self._nextLoop)
            
        
        
class Session(object):
    def __init__(self, aSessionToken):
        self._token = aSessionToken
        self._epoch = int(time.time())
        self._params = {"expiration" 
                            : self._epoch + Sessions._SESSION_LIFE # default expiration is epoch + 5 minutes
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
        
    def delProperty(self, propName):
        # pop + default value avoid the need of try/catch + del statement
        self._properties.pop(propName, True)
        
    def getProperty(self, propName, *args):
        if len(args):
            return self._properties.get(propName, args[0])
        else:
            return self._properties[propName]
    
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
