'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''
from myclips_server.xmlrpc.services.Service import Service
from myclips.rete.Network import Network
from myclips_server import MyClipsServerException, InvalidArgTypeError
import myclips_server.xmlrpc.services.types.skeletons as skeletons
from myclips_server.xmlrpc.services import sessions

class Engine(Service):
    '''
    MyClips inference engine service:
        a bridge to the myclips.rete.Network api
    
        WARNING: output/input streams must be registered with
            ClientIO service before any method of this service is called,
            otherwise any input request will have EOF as return value
            and any output will be suppressed.
    
    A good way to be sure that client streams are used
    is to call .destroyNetwork after streams registration.
    Then, any call to the Engine service will create a new
    network to work with (and with streams registered)
    
    '''

    _TYPE = "Engine"
    _NAME = "Engine_MyClips"
    __API__ = Service.__API__ + [ 
               # Network creation api
               'addConstruct', 'addDefRule', 'addDefFacts', 'addDefFunction', 
               'addDefModule', 'addDefGlobal', 'addDefTemplate',
               # WM manipulation 
               'assertFact', 'retractFact', 'retractFactId',
               # WM query
               'getWme', 'getWmes',
               # Engine api
               'clear', 'reset', 'run', 'destroyNetwork']
    
    def onSessionDestroy(self, aSessionToken):
        self.destroyNetwork(aSessionToken)
    
    def destroyNetwork(self, aSessionToken):
        '''
        Destroy a Network for this session (if any) 
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        '''
        theSessionsService = self._broker.Sessions
        theSessionsService.delProperty(aSessionToken, 'Engine_MyClips.network') 
        
    
    def getNetwork(self, aSessionToken):
        '''
        Return the myclips.rete.Network object for the session.
        If no Network has been registered before, a new one will
        be created 
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @return: a Network object for this session
        @rtype: myclips.rete.Network 
        '''
        
        theSessionsService = self._broker.Sessions
        theNetwork = theSessionsService.getProperty(aSessionToken, 'Engine_MyClips.network', None) 
        if theNetwork is None:
            
            #---- Prepare the stdout/stdin redirect ----------#
            #---- for the client through ClientIO service ----#
            
            resources = {}
            
            # prepare a stream suppressor to use for an unspecified stream
            suppressor = SuppressStream()
            
            try:
                # get the service
                theClientIOService = self._broker.ClientIO
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
        'myclips.Fact.Fact' : 'assertFact'
    }
    
    @sessions.renewer
    def addConstruct(self, aSessionToken, aConstructSkeleton):
        '''
        Add a generic construct skeleton in the engine.
        This helper redirect automatically the skeleton
        to the add* method that fits best to the skeleton
        
        myclips.Fact.Fact skeletons are redirected to
        the .assertFact method
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aConstructSkeleton: a skeleton for a valid construct
                accepted by a add* method
        @type aConstructSkeleton: dict
        @raise InvalidArgType: for invalid aConstructSkeleton
        '''
        
        theRegistryService = self._broker.Registry
        
        for (theType, theHandler) in self._CONSTRUCT_HANDLER_MAP_.items():
            if theRegistryService.isA(aConstructSkeleton, theType):
                return getattr(self, theHandler)(aSessionToken, aConstructSkeleton)
            
            
        raise MyClipsServerException("Invalid <aConstructSkeleton> type")
        
    @sessions.renewer
    def addDefRule(self, aSessionToken, aRuleSkeleton):
        '''
        Add a defrule construct to a network
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aRuleSkeleton: a valid myclips.parser.Types.DefRuleConstruct skeleton
        @type aRuleSkeleton: dict
        @return: the added rule name (in the complete form MODULE::RuleName)
        @rtype: string
        @raise InvalidArgType: for invalid aRuleSkeleton
        '''
        
        theNetwork = self.getNetwork(aSessionToken)
        theRegistryService = self._broker.Registry
        
        if theRegistryService.isA(aRuleSkeleton, skeletons.DefRuleConstruct.__CLASS__):
            
            aDefRule = theRegistryService.toConcrete(aSessionToken, aRuleSkeleton)
            aPNode = theNetwork.addRule(aDefRule)
            return aPNode.completeMainRuleName()
        
        else:
            raise InvalidArgTypeError("addDefRule", 2, skeletons.DefRuleConstruct.sign(), repr(aRuleSkeleton))
            
        
    @sessions.renewer
    def addDefModule(self, aSessionToken, aModuleSkeleton):
        '''
        Add a defmodule construct to a network
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aModuleSkeleton: a valid myclips.parser.Types.DefModuleConstruct skeleton
        @type aModuleSkeleton: dict
        @return: True on success
        @rtype: boolean
        @raise InvalidArgType: for invalid aRuleSkeleton
        '''

        theRegistryService = self._broker.Registry
        
        if theRegistryService.isA(aModuleSkeleton, skeletons.DefModuleConstruct.__CLASS__):
            
            # toConcrete create a types.DefModuleConstruct object
            # and its constructor take care of module insertion in Network
            theRegistryService.toConcrete(aSessionToken, aModuleSkeleton)
            return True
        
        else:
            raise InvalidArgTypeError("addDefModule", 2, skeletons.DefModuleConstruct.sign(), repr(aModuleSkeleton))

    @sessions.renewer
    def addDefFacts(self, aSessionToken, aDeffactsSkeleton):
        '''
        Add a deffact to the network
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aDeffactsSkeleton: a valid myclips.parser.Types.DefFactsConstruct skeleton
        @type aDeffactsSkeleton: dict
        @return: True on success
        @rtype: boolean
        @raise InvalidArgTypeError: for invalid aDeffactsSkeleton
        '''

        theNetwork = self.getNetwork(aSessionToken)
        theRegistryService = self._broker.Registry
        
        if theRegistryService.isA(aDeffactsSkeleton, skeletons.DefFactsConstruct.__CLASS__):
            
            aDeffacts = theRegistryService.toConcrete(aSessionToken, aDeffactsSkeleton)
            theNetwork.addDeffacts(aDeffacts)
            return True
        
        else:
            raise InvalidArgTypeError("addDefFacts", 2, skeletons.DefFactsConstruct.sign(), repr(aDeffactsSkeleton))

    @sessions.renewer
    def addDefGlobal(self, aSessionToken, aDefglobalSkeleton):
        '''
        Add a defglobal to the network
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aDefglobalSkeleton: a valid myclips.parser.Types.DefGlobalConstruct skeleton
        @type aDefglobalSkeleton: dict
        @return: True on success
        @rtype: boolean
        @raise InvalidArgTypeError: for invalid aDeffactsSkeleton
        '''
        

        theRegistryService = self._broker.Registry
        
        if theRegistryService.isA(aDefglobalSkeleton, skeletons.DefGlobalConstruct.__CLASS__):
            
            # toConcrete create a types.DefGlobalConstruct object
            # and its constructor take care of module insertion in Network
            theRegistryService.toConcrete(aSessionToken, aDefglobalSkeleton)
            return True
        
        else:
            raise InvalidArgTypeError("addDefGlobal", 2, skeletons.DefGlobalConstruct.sign(), repr(aDefglobalSkeleton))

    @sessions.renewer
    def addDefTemplate(self, aSessionToken, aDefTemplateSkeleton):
        '''
        Add a deftemplate to the network
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aDefTemplateSkeleton: a valid myclips.parser.Types.DefTemplateConstruct skeleton
        @type aDefTemplateSkeleton: dict
        @return: True on success
        @rtype: boolean
        @raise InvalidArgTypeError: for invalid aDefTemplateSkeleton
        '''
        
        theRegistryService = self._broker.Registry
        
        if theRegistryService.isA(aDefTemplateSkeleton, skeletons.DefTemplateConstruct.__CLASS__):
            
            # toConcrete create a types.DefTemplateConstruct object
            # and its constructor take care of module insertion in Network
            theRegistryService.toConcrete(aSessionToken, aDefTemplateSkeleton)
            return True
        
        else:
            raise InvalidArgTypeError("addDefTemplate", 2, skeletons.DefTemplateConstruct.sign(), repr(aDefTemplateSkeleton))

    @sessions.renewer
    def addDefFunction(self, aSessionToken, aDefFunctionSkeleton):
        '''
        Add a deffunction to the network
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aDefFunctionSkeleton: a valid myclips.parser.Types.DefFunctionConstruct skeleton
        @type aDefFunctionSkeleton: dict
        @return: True on success
        @rtype: boolean
        @raise InvalidArgTypeError: for invalid aDefFunctionSkeleton
        '''
        
        theRegistryService = self._broker.Registry
        
        if theRegistryService.isA(aDefFunctionSkeleton, skeletons.DefFunctionConstruct.__CLASS__):
            
            # toConcrete create a types.DefFunctionConstruct object
            # and its constructor take care of module insertion in Network
            theRegistryService.toConcrete(aSessionToken, aDefFunctionSkeleton)
            return True
        
        else:
            raise InvalidArgTypeError("addDefFunction", 2, skeletons.DefFunctionConstruct.sign(), repr(aDefFunctionSkeleton))

    @sessions.renewer
    def assertFact(self, aSessionToken, aFactSkeleton):
        '''
        Assert a new fact
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aFactSkeleton: a valid myclips.Fact.Fact skeleton
        @type aFactSkeleton: dict
        @return: a tuple (<Skeleton: myclips.rete.WME.WME>, boolean)
            If the fact asserted was already in the network, the boolean value is False.
            For new facts, the boolean valud is True
            The Wme skeleton is the new (or old) wme for the asserted fact
        @rtype: tuple (or list of 2 values)
        @raise InvalidArgTypeError: for invalid aFactSkeleton
        '''
        
        
        theNetwork = self.getNetwork(aSessionToken)
        theRegistryService = self._broker.Registry
        
        if theRegistryService.isA(aFactSkeleton, skeletons.Fact.__CLASS__):
            
            aFact = theRegistryService.toConcrete(aSessionToken, aFactSkeleton)
            return theRegistryService.toSkeleton(theNetwork.assertFact(aFact))
        
        else:
            raise InvalidArgTypeError("assertFact", 2, skeletons.Fact.sign(), repr(aFactSkeleton))
    
    @sessions.renewer
    def retractFact(self, aSessionToken, aFactSkeleton):
        '''
        Retract a fact from the network. This function required a fact
        skeleton as representation of the fact to remove
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aFactSkeleton: a valid myclips.Fact.Fact skeleton
        @type aFactSkeleton: dict
        @return: True on success
        @rtype: boolean
        @raise InvalidArgTypeError: for invalid aFactSkeleton
        '''
        

        theNetwork = self.getNetwork(aSessionToken)
        theRegistryService = self._broker.Registry
        
        if theRegistryService.isA(aFactSkeleton, skeletons.Fact.__CLASS__):
            
            aFact = theRegistryService.toConcrete(aSessionToken, aFactSkeleton)
            aWme = theNetwork.getWmeFromFact(aFact)
            theNetwork.retractFact(aWme)
            return True
        
        else:
            raise InvalidArgTypeError("retractFact", 2, skeletons.Fact.sign(), repr(aFactSkeleton))


    @sessions.renewer
    def retractFactId(self, aSessionToken, aFactId):
        '''
        Retract a fact from the network. This function required a fact-id
        (clips's fact-index) as representation of the fact to remove
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aFactId: an id for an asserted fact
        @type aFactId: dict
        @return: True on success
        @rtype: boolean
        @raise InvalidArgTypeError: for invalid aFactId
        '''

        theNetwork = self.getNetwork(aSessionToken)
        
        if isinstance(aFactId, int):
            
            aWme = theNetwork.getWmeFromId(aFactId)
            return theNetwork.retractFact(aWme)
        
        else:
            raise InvalidArgTypeError("retractFactId", 2, '<int>', repr(aFactId))

    @sessions.renewer
    def getWme(self, aSessionToken, aFactId):
        '''
        Return a <Skeleton: myclips.rete.WME.WME> for a fact with id aFactId
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param aFactId: a fact-id (clips's fact-index)
        @type aFactId: int
        @return: a myclips.rete.WME.WME skeleton for the fact with id aFactId
        @rtype: dict
        '''
        
        
        theNetwork = self.getNetwork(aSessionToken)
        
        if isinstance(aFactId, int):
            
            theRegistryService = self._broker.Registry
            return theRegistryService.toSkeleton(theNetwork.getWmeFromId(aFactId))
        
        else:
            raise InvalidArgTypeError("getWme", 2, '<int>', repr(aFactId))
    
    @sessions.renewer
    def getWmes(self, aSessionToken, moduleName=None):
        '''
        Return a list of <Skeleton: myclips.rete.WME.WME>
        
        If the moduleName arg is specified (not None)
        all facts asserted-by or visible-by a the module with name moduleName
        will be appended to the list.
        If the moduleName is not specified the list of
        asserted-by or visible-by facts for the current module
        will be returned
        If the moduleName value is '*', the complete working memory
        will be returned as list of <Skeleton: myclips.rete.WME.WME>
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: dict
        @param moduleName: a module name for facts filtering, '*' or None
        @type moduleName: string|None|'*'
        '''

        theNetwork = self.getNetwork(aSessionToken)
        
        if moduleName is None or isinstance(moduleName, basestring):
            
            theRegistryService = self._broker.Registry
            
            if moduleName == "*" :
                return theRegistryService.toSkeleton(theNetwork.facts)
            else:
                return theRegistryService.toSkeleton(theNetwork.factsForScope(moduleName))
        
        else:
            raise InvalidArgTypeError("getWmes", 2, '<string> or <None>', repr(moduleName))

    @sessions.renewer
    def clear(self, aSessionToken):
        '''
        Clear the network
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        '''
        theNetwork = self.getNetwork(aSessionToken)
        return theNetwork.clear()
        
    @sessions.renewer
    def reset(self, aSessionToken):
        '''
        Reset the network
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        '''
        theNetwork = self.getNetwork(aSessionToken)
        return theNetwork.reset()
    
    @sessions.renewer
    def run(self, aSessionToken, steps=None):
        '''
        Execute all or a number of activations available in the network
        
        @param aSessionToken: a token for a valid session
        @type aSessionToken: string
        @param steps: to limit the activations execution to a max-bound number
        @type steps: int
        '''
        
        theNetwork = self.getNetwork(aSessionToken)
    
        if steps is None or isinstance(steps, int):
            theNetwork.run(steps)
        else:
            raise InvalidArgTypeError("run", 2, '<int> or <None>', repr(steps))

    
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
    