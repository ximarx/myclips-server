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
            
            try:
                theClientIOService = self._factory.instance('ClientIO')
            except:
            
                resources['stdout'] = SuppressStream.default
                resources['stdin'] = SuppressStream.default
            
            else:
                
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
                        resources[resourceName] = theClientIOService.getStream(aSessionToken, streamName)
                    except:
                        try:
                            resources[resourceName] = resources[otherResourceAlternative]
                        except:
                            resources[resourceName] = SuppressStream.default
            

            #---- Create the instance of Network for the client ----#
            #---- and store it in the session ----------------------#
            
            theNetwork = Network(resources=resources)
            theSessionsService.setProperty(aSessionToken, 'Engine_MyClips.network', theNetwork)
            
        return theNetwork
    
    
class SuppressStream(object):
    default = None
    def __getattr__(self, name):
        return lambda *args,**kwargs:None
SuppressStream.default = SuppressStream()
    