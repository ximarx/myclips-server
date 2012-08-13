'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips-server.xmlrpc.server import MyClipsDocXMLRPCServer
from myclips-server.xmlrpc.Broker import Broker
from myclips-server.xmlrpc.services import Services


server = MyClipsDocXMLRPCServer(('localhost', 8081), allow_none=True)

server.register_introspection_functions()

broker = Broker({
    "RULES"
        : Services.Rules(),
    "WM"
        : Services.WorkingMemory(),
    "TYPES"
        : Services.TypeFactory(),
    "AUTH"
        : Services.SessionsManager()
})

#api.apis("RULES")

server.register_instance(broker, True)
#APIs = API()
#server.register_instance(APIs.TYPES, allow_dotted_names=True)
#server.register_instance(APIs.RETE, allow_dotted_names=True)

server.serve_forever()