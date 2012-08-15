'''
Created on 31/lug/2012

@author: Francesco Capozzo
'''
from myclips.FunctionsManager import FunctionDefinition,\
    Constraint_ArgType, Constraint_MinArgsLength
import myclips.parser.Types as types
from myclips.functions.Function import Function, InvalidArgValueError
from myclips.rete.Network import RuleNotFoundError

class DrawCircuit(Function):
    '''
    Refresh a rule status in the agenda
    '''
    def __init__(self, *args, **kwargs):
        Function.__init__(self, *args, **kwargs)
        
        
    def do(self, theEnv, theStream, *args, **kargs):
        """
        function handler implementation
        """
        
        theStream = self.resolve(theEnv, 
                                 self.semplify(theEnv, theStream, types.Symbol, ("1", "symbol")))
        
        try:
            _thePNodes = [theEnv.network.getPNode(ruleName) 
                            for ruleName 
                                in [self.resolve(theEnv, self.semplify(theEnv, ruleName, types.Symbol, ("ALL", "symbol"))) for ruleName in args]]
        except RuleNotFoundError, e:
            
            raise InvalidArgValueError(e.message)
            
        else:
            # RuleNotFoundError could be raised... but it will flow outside of the network
            # and it's ok!
    
            thePNodes = []
    
            for thePNode in _thePNodes:
                from myclips.rete.nodes.PNode import PNode
                assert isinstance(thePNode, PNode)
                thePNodes += [thePNode] + thePNode.getLinkedPNodes()
                
            import myclips.debug as debug
            
            thePlotter = debug.prepare_network_fragment_plotter(thePNodes)
            
            try:
                theDotString = thePlotter.dot_string()
            except:
                theDotString = ""
            
            if theStream != 'nil':
                try:
                    theStream = theEnv.RESOURCES[theStream]
                    theStream.write(theDotString)
                except Exception, e:
                    #print e
                    pass
            
            return types.String(theDotString)
    
    
DrawCircuit.DEFINITION = FunctionDefinition("?SYSTEM?", "draw-circuit", DrawCircuit(), types.String, DrawCircuit.do ,
            [
                Constraint_MinArgsLength(2),
                Constraint_ArgType(types.Symbol),
            ],forward=False)
        
        