import importlib
import os
import json
import myclips_server
from myclips_server import MyClipsServerException

SERVICES_DIRS = [os.path.dirname(__file__)]
SERVICES_MANIFEST = "services.json"


class Factory(object):

    def __init__(self, paths, manifestName):    
        self._INSTANCES = {}
        self.__ready = False
        self._paths = paths
        self._manifestName = manifestName
    
    def register(self, serviceType, serviceInstance, replaceDefault=False):
        
        self._INSTANCES[serviceInstance._NAME] = serviceInstance
        
        if replaceDefault or not self._INSTANCES.has_key(serviceType):
            self._INSTANCES[serviceType] = serviceInstance
        
        
    def services(self):
        return self._INSTANCES.keys()
    
    def bootstrap(self):

        self.__ready = True
    
        for SERVICES_DIR in self._paths:
        
            manifestPath = "/".join([SERVICES_DIR.rstrip("/"), self._manifestName])
            
            try:
                funcList = json.load(open(manifestPath, "rU"))
            except Exception, e:
                myclips_server.logger.error("Services manifest file %s cannot be loaded: %s", manifestPath, repr(e))
            else:
                for serviceDict in funcList:
                    try:
                        serviceType = serviceDict['type']
                        serviceModule = serviceDict['module']
                        serviceClass = serviceDict['class']
                    except KeyError, e:
                        myclips_server.logger.error("Malformed service definition in manifest file %s:\n\tError: %s\n\tDefinition: %s", manifestPath, repr(e), str(serviceDict))
                    else:
                        try:
                            serviceInstance = myclips_server.myclips.newInstance(serviceClass, [self], serviceModule)
                        except (ImportError, TypeError), e:
                            myclips_server.logger.error("Error loading service definition class <%s>: %s", serviceClass, e)
                        else:
                            self.register(serviceType, serviceInstance)
        
        # send the _onInitCompleted signal
        for serviceInstance in self._INSTANCES.values():
            serviceInstance._onInitCompleted()
        
    
    def instance(self, service):
        if not self.__ready: self.bootstrap()
        try:
            return self._INSTANCES[service]
        except KeyError:
            raise ServiceNotFoundError("Unknown service <%s>"%service) 
            
            
    def isValid(self, service):
        return self._INSTANCES.has_key(service)
    
    
factory = Factory(SERVICES_DIRS, SERVICES_MANIFEST)

    
class ServiceNotFoundError(MyClipsServerException):
    pass