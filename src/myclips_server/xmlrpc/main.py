'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.Broker import Broker
import myclips_server.xmlrpc.services as services
from myclips_server.xmlrpc.server import MyClipsDocXMLRPCServer
import myclips_server
import myclips
import traceback

def _setup():
    
    MYCLIPS_FUNCTIONS_REPLACEMENTS = myclips_server.CONFIGURATIONS.get('myclips', {}).get('system-functions', {}).get('replace', [])
    MYCLIPS_FUNCTIONS_REMOVALS = myclips_server.CONFIGURATIONS.get('myclips', {}).get('system-functions', {}).get('remove', [])
    MYCLIPS_FUNCTIONS_REGISTRATIONS = myclips_server.CONFIGURATIONS.get('myclips', {}).get('system-functions', {}).get('register', [])
    
    
    def __replaceFuncs(_F_REPLACEMENTS):
    
        # replace some system function definition with a server-proof version:
        
        if len(_F_REPLACEMENTS):
        
            import myclips.functions as _mycfuncs
            
            # manually bootstrap system functions
            _mycfuncs.SystemFunctionBroker.bootstrap()
            
            for _funcInfo in _F_REPLACEMENTS:
        
                myclips_server.logger.info("Replacing: %s", str(_funcInfo))    
        
                _moduleName = "<none>"
                _className = "<none>"    
        
                try:
                    # prepare the replacement
                    
                    _moduleName = _funcInfo['module']
                    _className = _funcInfo['class']
                    _funcInstance = myclips.newInstance(_className, None, _moduleName)
                    _mycfuncs.SystemFunctionBroker.register(_funcInstance, True)
                except:
                    myclips_server.logger.critical("Error replacing %s.%s\n%s---------------\n", _moduleName, _className, traceback.format_exc() )
                else:
                    # then replace the definition
                    myclips_server.logger.info("\t\t...Done")
    
    
    def __registerFuncs(_F_REGISTERS):
    
        # replace some system function definition with a server-proof version:
        
        if len(_F_REGISTERS):
        
            import myclips.functions as _mycfuncs
            
            # manually bootstrap system functions
            _mycfuncs.SystemFunctionBroker.bootstrap()
            
            for _funcInfo in _F_REGISTERS:
        
                myclips_server.logger.info("Registering: %s", str(_funcInfo))
                
                _moduleName = "<none>"
                _className = "<none>"    
        
                try:
                    # prepare the replacement
                    
                    _moduleName = _funcInfo['module']
                    _className = _funcInfo['class']
                    _funcInstance = myclips.newInstance(_className, None, _moduleName)
                    _mycfuncs.SystemFunctionBroker.register(_funcInstance, False)
                except:
                    myclips_server.logger.critical("Error registering %s.%s\n%s---------------\n", _moduleName, _className, traceback.format_exc() )
                else:
                    # then replace the definition
                    myclips_server.logger.info("\t\t...Done")
    
    
    def __removeFuncs(_F_REMOVES):
    
        # replace some system function definition with a server-proof version:
        
        if len(_F_REMOVES):
        
            import myclips.functions as _mycfuncs
            
            # manually bootstrap system functions
            _mycfuncs.SystemFunctionBroker.bootstrap()
            
            for _funcInfo in _F_REMOVES:
        
                myclips_server.logger.info("Removing: %s", str(_funcInfo))
                try:
                    _mycfuncs.SystemFunctionBroker.unregister(_funcInfo)
                except:
                    myclips_server.logger.critical("Error removing %s\n%s--------------\n", _funcInfo, traceback.format_exc() )
                else:
                    myclips_server.logger.info("\t\t...Done")
    
    
    __removeFuncs(MYCLIPS_FUNCTIONS_REMOVALS)
    __registerFuncs(MYCLIPS_FUNCTIONS_REGISTRATIONS)
    __replaceFuncs(MYCLIPS_FUNCTIONS_REPLACEMENTS) 
    

def main():
    
    _setup();
    
    bindAddress = myclips_server.CONFIGURATIONS.get('myclips_server', {}).get('bind-address', 'localhost')
    bindPort = myclips_server.CONFIGURATIONS.get('myclips_server', {}).get('bind-port', 'localhost')
    logRequests = myclips_server.CONFIGURATIONS.get('myclips_server', {}).get('log-requests', True)
    
    server = MyClipsDocXMLRPCServer((bindAddress, bindPort), allow_none=True, logRequests=logRequests)
    
    servicesConf = myclips_server.CONFIGURATIONS.get('myclips_server', {}).get('services', [])
    
    if isinstance(servicesConf, list):
        for index, serviceName in enumerate(services):
            servicesConf[index] = services.factory.instance(serviceName)
    elif isinstance(servicesConf, dict):
        for (serviceKey, serviceName) in servicesConf.items():
            servicesConf[serviceKey] = services.factory.instance(serviceName)
    
    #server.register_introspection_functions()
    
#    broker = Broker({
#        "RULES"
#            : Services.Rules(),
#        "WM"
#            : Services.WorkingMemory(),
#        "TYPES"
#            : Services.TypeFactory(),
#        "AUTH"
#            : Services.SessionsManager()
#    })

    broker = Broker(services=servicesConf)
    
    server.register_instance(broker)
    
    server.serve_forever()
    
if __name__ == '__main__':
    
    main()
    