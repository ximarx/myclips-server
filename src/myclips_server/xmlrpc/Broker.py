'''
Created on 10/lug/2012

@author: Francesco Capozzo
'''
import inspect
import traceback
from myclips_server.xmlrpc.services.sessions.Sessions import InvalidSessionError
from xmlrpclib import Fault
from myclips_server import MyClipsServerException, MyClipsServerFault
from myclips.MyClipsException import MyClipsException
import myclips_server

class Broker(object):
    '''
    MyClips-Server Service Broker
    '''
    
    __API__ = ['services', 'apis']

    def __init__(self, services):
        
        if isinstance(services, dict):
            self._services = services
        elif isinstance(services, list):
            self._services = {}
            for service in services:
                if self._services.has_key(service._TYPE):
                    self._services[service._NAME] = service
                else:
                    self._services[service._TYPE] = service
        
        
        for (sKey, Service) in self._services.items():
            Service.setBroker(self)
            setattr(self, sKey, Service)
            
    def __getattr__(self, name):
        raise myclips_server.ServiceNotFoundFault('Invalid service "%s"' % name)
            
    def _dispatch(self, methodName, args):
        
        if methodName is Broker.__API__:
            return getattr(self, methodName)(*args)
        
        parts = methodName.split(".")
        
        theService = parts[0]
        parts = parts[1:None]
        
        theObj = self._services[theService]
        
        try:
            for part in parts:
                
                theAPIs = theObj.__API__ if hasattr(theObj, "__API__") else [x for x in dir() if x[0] != '_']
                
                if part in theAPIs:
                    theObj = getattr(theObj, part)
                else:
                    raise MyClipsServerFault('property "%s" is not supported' % methodName, code=1999)    
        
            # log a requests    
            returnValue = theObj(*args)
            myclips_server.logger.info("Request:\n\tMethod-Name: %s\n\tArgs: %s", methodName, args)
            myclips_server.logger.debug("Response:\n\t%s", repr(returnValue))
            return returnValue
        
        except MyClipsServerFault, e:
            myclips_server.logger.warning("Request:\n\tMethod-Name: %s\n\tArgs: %s\n\tException: %s\n\t\t%s", 
                                          methodName, 
                                          args, 
                                          e.__class__.__name__, 
                                          e.message)
            raise
        except Exception, e:
            myclips_server.logger.error("Request:\n\tMethod-Name: %s\n\tArgs: %s\n\n%s\n--------------",
                                          methodName, 
                                          args,
                                          traceback.format_exc())
            
            # convert the unexpected exception into a Fault
            # and hide trace informations 
            if isinstance(e, MyClipsServerException):
                raise MyClipsServerFault(e.message, 1003)
            elif isinstance(e, MyClipsException):
                raise MyClipsServerFault(e.message, 1004)
            else:
                raise MyClipsServerFault(str(e))
        

    def services(self):
        """
        Get the list of services available for this server
        Each service is returned as a list of
            [serviceId, serviceType, serviceName]
        
        @return: a list of service descriptor
        @rtype: list
        """
        return [(x, y._TYPE, y._NAME) for (x,y) in self._services.items()]
            
    @staticmethod
    def _vectorizeArgs(func):
        args, _, _, defaults = inspect.getargspec(func)
        return [(arg,) if defaults is None
                    else (arg, defaults[index]) if len(args) == len(defaults) 
                        else (arg, defaults[index - (len(args) - len(defaults))]) if (index - (len(args) - len(defaults))) >= 0
                            else (arg,) 
                for (index, arg) in enumerate(args) if (index > 0 or (index == 0 and args[0] != "self"))]

    def apis(self, aServiceId):
        """
        Show the list of apis available for a service
        
        The result is returned as a list of 
            [funcName, [funcArg1, funcArg2, .. , funcArgN]]
        for each function
        
        @param aServiceId: the name of a registered service
        @type aServiceId: string
        @return: a list of nested list (1 for each function)
        @rtype: list
        
        """
        theService = self._services[aServiceId]
        iterateOver = theService.__APIS__ if hasattr(theService, '__APIS__') else dir(theService)
        return [
                [
                 ".".join([aServiceId, func]), #SERVICENAME.func
                 Broker._vectorizeArgs(getattr(self._services[aServiceId], func))
                ] 
                for func in iterateOver if func[0] != '_'# and callable(getattr(theService, func))
            ]

#    def parseProduction(self, defrule):
#        parsedItems = clipsparser.parse(defrule)
#        
#        rule = parsedItems[0][1]
#        default_rule = {'name': '', 'lhs': [], 'rhs': [], 'declare': {'salience': 0}, 'description': ''}
#        default_rule.update(rule)
#        rule = default_rule
#        p = Production(rule['name'], rule['lhs'], rule['rhs'], rule['declare'], rule['description'])
#        MyClipsWrapper.i().rete.add_production(p)
#        
#
#    def assert_fact(self, *args, **kargs):
#        MyClipsWrapper.i().rete.assert_fact(*args, **kargs)

