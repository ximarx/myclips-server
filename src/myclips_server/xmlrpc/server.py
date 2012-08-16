'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from DocXMLRPCServer import XMLRPCDocGenerator, ServerHTMLDoc,\
    DocXMLRPCRequestHandler
from SimpleXMLRPCServer import SimpleXMLRPCServer, resolve_dotted_attribute
from myclips_server.xmlrpc.services.Service import Service
import SocketServer

class MyClipsXMLRPCDocGenerator(XMLRPCDocGenerator):
    
    def recursive_find_methods(self, methodsDict, dotObject, method_prefix=""):
        
        if isinstance(dotObject, Service) and hasattr(dotObject, '__API__'):
            iterateOver = dotObject.__API__
        else:
            iterateOver = dir(dotObject)

        for dotted in [x for x in iterateOver if x[0] != '_' or x == '__DOC__']:
            if '__DOC__' == dotted:
                methodsDict[".".join([method_prefix]) if method_prefix != "" else ""] = dotObject
            else:
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

class MyClipsXMLRPCServer(SocketServer.ThreadingMixIn,SimpleXMLRPCServer): 
    pass

class MyClipsDocXMLRPCServer(  MyClipsXMLRPCServer,
                        MyClipsXMLRPCDocGenerator):
    """XML-RPC and HTML documentation server.

    Adds the ability to serve server documentation to the capabilities
    of SimpleXMLRPCServer.
    """

    def __init__(self, addr, requestHandler=DocXMLRPCRequestHandler,
                 logRequests=1, allow_none=False, encoding=None,
                 bind_and_activate=True):
        MyClipsXMLRPCServer.__init__(self, addr, requestHandler, logRequests,
                                    allow_none, encoding, bind_and_activate)
        MyClipsXMLRPCDocGenerator.__init__(self)

