'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
from myclips.rete.Network import Network
from myclips_server import MyClipsServerException, InvalidArgTypeError
import myclips_server.xmlrpc.services.types.skeletons as skeletons

class Engine(Service):
    '''
    Bridge to the myclips.rete.Network api
    '''

    _TYPE = "Engine"
    _NAME = "Engine_MyClips"
    __API__ = ['ping', 
               # Construct creation api
               'addConstruct', 'addDefRule', 'addDefFacts',  
               'addDefModule', 'addDefGlobal', 'addDefTemplate',
               # WM manipulation 
               'assertFact', 'retractFact', 'retractFactId'
               # WM query
               'getFact', 'getFacts']
    
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
                            # the previous bound resource is not availalble, use the suppressor
                            resources[resourceName] = suppressor

            #---- Create the instance of Network for the client ----#
            #---- and store it in the session ----------------------#
            
            # use the map of resources in the Network initialization
            theNetwork = Network(resources=resources)
            theSessionsService.setProperty(aSessionToken, 'Engine_MyClips.network', theNetwork)
            
        return theNetwork
    

    _CONSTRUCT_HANDLER_MAP_ = {
        'myclips.parser.Types.DefRuleConstruct' : 'addDefRule',
        'myclips.parser.Types.DefModuleConstruct' : 'addDefModule',
        'myclips.parser.Types.DefFactsConstruct' : 'addDefFacts',
        'myclips.parser.Types.DefGlobalConstruct' : 'addDefGlobal',
        'myclips.parser.Types.DefTemplateConstruct' : 'addDefTemplate',
    }
    
    def addConstruct(self, aSessionToken, aConstructSkeleton):
        
        theRegistryService = self._factory.instance('Registry')
        
        for (theType, theHandler) in self._CONSTRUCT_HANDLER_MAP_.items():
            if theRegistryService.isA(aConstructSkeleton, theType):
                return getattr(self, theHandler)(aSessionToken, aConstructSkeleton)
            
            
        raise MyClipsServerException("Invalid <aConstructSkeleton> type")
        
        
    def addDefRule(self, aSessionToken, aRuleSkeleton):
        
        theNetwork = self.getNetwork(aSessionToken)
        theRegistryService = self._factory.instance('Registry')
        
        if theRegistryService.isA(aRuleSkeleton, skeletons.DefRuleConstruct.__CLASS__):
            
            aDefRule = theRegistryService.toConcrete(aSessionToken, aRuleSkeleton)
            theNetwork.addRule(aDefRule)
            return True
        
        else:
            raise InvalidArgTypeError("addDefRule", 2, skeletons.DefRuleConstruct.sign(), repr(aRuleSkeleton))
            
        
    
    def addDefModule(self, aSessionToken, aModuleSkeleton):

        theRegistryService = self._factory.instance('Registry')
        
        if theRegistryService.isA(aModuleSkeleton, skeletons.DefModuleConstruct.__CLASS__):
            
            # toConcrete create a types.DefModuleConstruct object
            # and its constructor take care of module insertion in Network
            theRegistryService.toConcrete(aSessionToken, aModuleSkeleton)
            return True
        
        else:
            raise InvalidArgTypeError("addDefModule", 2, skeletons.DefModuleConstruct.sign(), repr(aModuleSkeleton))

    
    def addDefFacts(self, aSessionToken, aDeffactsSkeleton):

        theNetwork = self.getNetwork(aSessionToken)
        theRegistryService = self._factory.instance('Registry')
        
        if theRegistryService.isA(aDeffactsSkeleton, skeletons.DefFactsConstruct.__CLASS__):
            
            aDefRule = theRegistryService.toConcrete(aSessionToken, aDeffactsSkeleton)
            theNetwork.addRule(aDefRule)
            return True
        
        else:
            raise InvalidArgTypeError("addDefFacts", 2, skeletons.DefFactsConstruct.sign(), repr(aDeffactsSkeleton))

    
    def addDefGlobal(self, aSessionToken, aDefglobalSkeleton):

        theRegistryService = self._factory.instance('Registry')
        
        if theRegistryService.isA(aDefglobalSkeleton, skeletons.DefGlobalConstruct.__CLASS__):
            
            # toConcrete create a types.DefGlobalConstruct object
            # and its constructor take care of module insertion in Network
            theRegistryService.toConcrete(aSessionToken, aDefglobalSkeleton)
            return True
        
        else:
            raise InvalidArgTypeError("addDefGlobal", 2, skeletons.DefGlobalConstruct.sign(), repr(aDefglobalSkeleton))

    
    def addDefTemplate(self, aSessionToken, aDefTemplateSkeleton):
        theRegistryService = self._factory.instance('Registry')
        
        if theRegistryService.isA(aDefTemplateSkeleton, skeletons.DefTemplateConstruct.__CLASS__):
            
            # toConcrete create a types.DefTemplateConstruct object
            # and its constructor take care of module insertion in Network
            theRegistryService.toConcrete(aSessionToken, aDefTemplateSkeleton)
            return True
        
        else:
            raise InvalidArgTypeError("addDefTemplate", 2, skeletons.DefTemplateConstruct.sign(), repr(aDefTemplateSkeleton))

    def addDefFunction(self, aSessionToken, aDefFunctionSkeleton):
        theRegistryService = self._factory.instance('Registry')
        
        if theRegistryService.isA(aDefFunctionSkeleton, skeletons.DefFunctionConstruct.__CLASS__):
            
            # toConcrete create a types.DefTemplateConstruct object
            # and its constructor take care of module insertion in Network
            theRegistryService.toConcrete(aSessionToken, aDefFunctionSkeleton)
            return True
        
        else:
            raise InvalidArgTypeError("addDefFunction", 2, skeletons.DefFunctionConstruct.sign(), repr(aDefFunctionSkeleton))

    
    def assertFact(self, aSessionToken, aFactSkeleton):
        pass
    
    def retractFact(self, aSessionToken, aFactSkeleton):
        pass

    def retractFactId(self, aSessionToken, aFactId):
        pass
    
    def getFact(self, aSessionToken, aFactId):
        pass
    
    def getFacts(self, aSessionToken, moduleName=None):
        pass
    
    def clear(self, aSessionToken):
        pass
        
    def reset(self, aSessionToken):
        pass
    
    def run(self, aSessionToken, steps=None):
        pass
    
    
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
    