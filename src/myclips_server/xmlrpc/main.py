'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.Broker import Broker
import myclips_server.xmlrpc.services as services
from myclips_server.xmlrpc.server import MyClipsDocXMLRPCServer
import myclips_server


def main():
    
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
    