'''
Created on 08/lug/2012

@author: Francesco Capozzo
'''
from bottle import run, default_app, response
import bottle
from DocXMLRPCServer import DocXMLRPCServer
from tesi.daemons.MyClipsWrapper import MyClipsWrapper
import thread
import sys
from tesi.daemons.xmlrpc.API import API


if __name__ == '__main__':
    
    #default_app.push()
    
    def allow_origin(callback):
        def wrapper(*args, **kwargs):
            body = callback(*args, **kwargs)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return body
        return wrapper
    
    bottle.install(allow_origin)    
    
    import tesi.daemons.restful.routes
    
    #app = default_app.pop()
    
    #run(app, host='localhost', port=8080, debug=True)
    #run(host='localhost', port=8080, debug=True)
    try:
        thread.start_new_thread(run, (), {'port': 8080, 'debug': True})
    except Exception, e:
        print >> sys.stderr, "Impossibile avviare bottle: ", e 
    
    
    server = DocXMLRPCServer(('localhost', 8081), allow_none=True)
    
    server.register_introspection_functions()
    
    server.register_instance(API())
    #APIs = API()
    #server.register_instance(APIs.TYPES, allow_dotted_names=True)
    #server.register_instance(APIs.RETE, allow_dotted_names=True)
    
    server.serve_forever()
    