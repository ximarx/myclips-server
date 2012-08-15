'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
from myclips.rete.Network import Network

class Engine(Service):
    '''
    Bridge to the myclips.rete.Network api
    '''

    _TYPE = "Engine"
    _NAME = "Engine_MyClips"
    __API__ = ['ping']
    
    def getNetwork(self, aSessionToken):
        
        theSessionsService = self._factory.instance('Sessions')
        theNetwork = theSessionsService.getProperty(aSessionToken, 'Engine_MyClips.network', None) 
        if theNetwork is None:
            
            #---- Prepare the stdout/stdin redirect ----------#
            #---- for the client through ClientIO service ----#
            
            resources = {}
            
            # prepare a stream suppressor to use for an unspecified stream
            suppressor = SuppressStream()
            
            try:
                # get the service
                theClientIOService = self._factory.instance('ClientIO')
            except:
                # no service available, use suppressor for stdin/stdout
                resources['stdout'] = suppressor
                resources['stdin'] = suppressor
            else:
                # resolve each resource to a stream in ClientIO service
                # streamMap items format:
                #    #0: theResourceName is the resource name for the stream
                #    #1[0]: theStreamName is the name of the stream to search for in the ClientIO
                #    #1[1]: theAlternative is the resource name of a resource (already binded) to use as alternative
                streamMap = [('stdout'   ,  ['stdout', None]),
                             ('stdin'    ,  ['stdin', None]),
                             ('t'        ,  ['t', 'stdout']),
                             ('wclips'   ,  ['wclips', 'stdout']),
                             ('wdialog'  ,  ['wdialog', 'stdout']),
                             ('wdisplay' ,  ['wdisplay', 'stdout']),
                             ('wwarning' ,  ['wwarning', 'stdout']),                             
                             ('werror'   ,  ['werror', 'stdout']),
                             ('wtrace'   ,  ['wtrace', 'stdout'])]

                for resourceName, (streamName, otherResourceAlternative) in streamMap:
                    try:
                        # search a stream for the resource
                        resources[resourceName] = theClientIOService.getStream(aSessionToken, streamName)
                    except:
                        # ... but it isn't found
                        try:
                            # ... i no alternative is possible, just use the suppressor
                            if otherResourceAlternative is None: raise Exception()
                            # ... otherwise try to bind to a previous bound resource
                            resources[resourceName] = resources[otherResourceAlternative]
                        except:
                            # the previous bound resource is not avaialble, use the suppressor
                            resources[resourceName] = suppressor

            #---- Create the instance of Network for the client ----#
            #---- and store it in the session ----------------------#
            
            # use the map of resources in the Network initialization
            theNetwork = Network(resources=resources)
            theSessionsService.setProperty(aSessionToken, 'Engine_MyClips.network', theNetwork)
            
        return theNetwork
    
    
class SuppressStream(object):
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
    def __repr__(self, *args, **kwargs):
        return object.__repr__(self, *args, **kwargs)
    def __getattr__(self, name):
        if name.startswith("read"):
            return lambda *args,**kwargs:""
        else:
            return lambda *args,**kwargs:None
    