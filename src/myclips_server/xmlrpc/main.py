'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.Broker import Broker
import myclips_server.xmlrpc.services as services
from myclips_server.xmlrpc.server import MyClipsDocXMLRPCServer


def main():
    
    
    
    server = MyClipsDocXMLRPCServer(('localhost', 8081), allow_none=True)
    
    server.register_introspection_functions()
    
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

    broker = Broker(services=[
            services.factory.instance('Sessions'),
            services.factory.instance('Network'),
            services.factory.instance('TypeFactory'),
    ])
    
    server.register_instance(broker, True)
    
    server.serve_forever()
    
if __name__ == '__main__':
    
    main()
    