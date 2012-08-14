'''
Created on 14/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
import importlib

class Services(Service):
    '''
    Allow to manage published services in the broker
    '''

    _NAME = "AdminServices_Services"
    _TYPE = "AdminServices"
    __API__ = ["ping", "restart", "install", "replace", "remove", "refresh"]
    
    def start(self, aServiceType):
        theService = self._factory.instance(aServiceType)
        theService.setBroker(self._broker)
        if self._broker._services.has_key(theService._TYPE):
            serviceKey = theService._NAME
        else:
            serviceKey = theService._TYPE
        self._broker._services[serviceKey] = theService
        
        return serviceKey
    
    def restart(self, aServiceName):
        theService = self._broker._services[aServiceName]
        theModule = theService.__class__.__module__
        theServiceClass = theService.__class__.__name__
        self.replace(aServiceName, theModule, theServiceClass)
        return True
        
    
    def install(self, aServiceName, moduleName, className):
        theModule = importlib.import_module(moduleName)
        reload(theModule)
        theService = getattr(theModule, className)(self._factory)
        theService._onInitCompleted()
        theService.setBroker(self._broker)
        if self._broker._services.has_key(theService._TYPE):
            serviceKey = theService._NAME
        else:
            serviceKey = theService._TYPE
        self._broker._services[serviceKey] = theService
        
        return serviceKey
    
    def replace(self, aServiceName, moduleName, className):
        theModule = importlib.import_module(moduleName)
        theServiceClass = className
        reload(theModule)
        theService = getattr(theModule, theServiceClass)(self._factory)
        theService._onInitCompleted()
        theService.setBroker(self._broker)
        self._broker._services[aServiceName] = theService
        return True
    
    def remove(self, aServiceName):
        del self._broker._services[aServiceName]
        
    def refresh(self, aModule):
        aModule = importlib.import_module(aModule)
        reload(aModule)
