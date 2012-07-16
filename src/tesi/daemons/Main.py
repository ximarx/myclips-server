'''
Created on 08/lug/2012

@author: Francesco Capozzo
'''
from bottle import run, default_app, response
import bottle
from DocXMLRPCServer import DocXMLRPCServer, XMLRPCDocGenerator,\
    DocXMLRPCRequestHandler, ServerHTMLDoc
from tesi.daemons.MyClipsWrapper import MyClipsWrapper
import thread
import sys
from tesi.daemons.xmlrpc.API import API
import tesi.daemons.xmlrpc as xmlrpc
from SimpleXMLRPCServer import SimpleXMLRPCServer, resolve_dotted_attribute

class MyXMLRPCDocGenerator(XMLRPCDocGenerator):
    
    def recursive_find_methods(self, methodsDict, dotObject, method_prefix=""):
        
        for dotted in [x for x in dir(dotObject) if x[0] != '_']:
            objectAttr = getattr(dotObject, dotted)
            if callable(objectAttr):
                methodsDict[".".join([method_prefix, dotted]) if method_prefix != "" else dotted] = objectAttr
            else:
                self.recursive_find_methods(methodsDict, objectAttr, dotted)
    
    def generate_html_documentation(self):
        """generate_html_documentation() => html documentation for the server

        Generates HTML documentation for the server using introspection for
        installed functions and instances that do not implement the
        _dispatch method. Alternatively, instances can choose to implement
        the _get_method_argstring(method_name) method to provide the
        argument string used in the documentation and the
        _methodHelp(method_name) method to provide the help text used
        in the documentation."""

        methods = {}

        for method_name in self.system_listMethods():
            if method_name in self.funcs:
                method = self.funcs[method_name]
            elif self.instance is not None:
                method_info = [None, None] # argspec, documentation
                if hasattr(self.instance, '_get_method_argstring'):
                    method_info[0] = self.instance._get_method_argstring(method_name)
                if hasattr(self.instance, '_methodHelp'):
                    method_info[1] = self.instance._methodHelp(method_name)

                method_info = tuple(method_info)
                if method_info != (None, None):
                    method = method_info
                elif not hasattr(self.instance, '_dispatch'):
                    try:
                        method = resolve_dotted_attribute(
                                    self.instance,
                                    method_name
                                    )
                    except AttributeError:
                        method = method_info
                else:
                    method = method_info
            else:
                assert 0, "Could not find method in self.functions and no "\
                          "instance installed"

            methods[method_name] = method
        
        if self.instance is not None:
            self.recursive_find_methods(methods, self.instance)
        

        documenter = ServerHTMLDoc()
        documentation = documenter.docserver(
                                self.server_name,
                                self.server_documentation,
                                methods
                            )

        return documenter.page(self.server_title, documentation)    

class MyDocXMLRPCServer(  SimpleXMLRPCServer,
                        MyXMLRPCDocGenerator):
    """XML-RPC and HTML documentation server.

    Adds the ability to serve server documentation to the capabilities
    of SimpleXMLRPCServer.
    """

    def __init__(self, addr, requestHandler=DocXMLRPCRequestHandler,
                 logRequests=1, allow_none=False, encoding=None,
                 bind_and_activate=True):
        SimpleXMLRPCServer.__init__(self, addr, requestHandler, logRequests,
                                    allow_none, encoding, bind_and_activate)
        MyXMLRPCDocGenerator.__init__(self)


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
    
    
    server = MyDocXMLRPCServer(('localhost', 8081), allow_none=True)
    
    server.register_introspection_functions()
    
    api = API({
        "RULES"
            : xmlrpc.Rules(),
        "WM"
            : xmlrpc.WorkingMemory(),
        "TYPES"
            : xmlrpc.TypeFactory(),
        "AUTH"
            : xmlrpc.SessionsManager()
    })
    
    #api.apis("RULES")
    
    server.register_instance(api, True)
    #APIs = API()
    #server.register_instance(APIs.TYPES, allow_dotted_names=True)
    #server.register_instance(APIs.RETE, allow_dotted_names=True)
    
    server.serve_forever()
    