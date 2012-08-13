'''
Created on 15/lug/2012

@author: Francesco Capozzo
'''
from tesi.daemons.xmlrpc.Service import Service
from tesi.daemons.xmlrpc.TypeFactory import TypeRegistry
from icse.Production import Production

class Rules(Service):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        TypeRegistry.default.addType("myclips.Rule", Production, "MyClips Production Rule",
                                        ("myclips.Rule",[
                                                ("name", ""),
                                                ("comment", ""),
                                                ("declarations", [
                                                        ("salience", 0)
                                                    ]),
                                                ("lhs", []),
                                                ("rhs", [])
                                            ]), 
                                        {
                                            "setName": myclips_Rule_setName,
                                            "setField": myclips_Rule_setField
                                         }, 
                                         lambda t:t,
                                         lambda t:t
                                    )

        TypeRegistry.default.addType("myclips.PositivePredicate", Production, "MyClips Production Rule",
                                        ("myclips.PositivePredicate",[
                                                ("pattern", []), #1/0/1
                                                ("assignment", []) #1/1/1
                                            ]), 
                                        {
                                            "setPattern": myclips_PositivePredicate_setPattern,
                                            "setAssignment": myclips_PositivePredicate_setAssignment,
                                         }, 
                                         lambda t:t,
                                         lambda t:t
                                    )
        
    def ping(self):
        return "PONG"
    
    def addRule(self, ruleSkeleton):
        return False

    def removeRule(self, ruleName=None, ruleSkeleton=None):
        return False
    
    def getRules(self):
        return []
    
    def getRule(self, ruleName=None):
        return []
    
    
    
def myclips_Rule_setName(instance, value):
    '''
    Set the rule name for the instance
    @param instance: myclips.Rule instance
    @param value: string rulename
    @return: myclips.Rule
    '''
    instance[1][0][1] = value
    return instance

def myclips_Rule_setField(instance, fieldName, value):
    '''
    Set a rule field by fieldName to value
    @param instance: myclips.Rule instance
    @param fieldName: string a myclips.Rule skeleton field
    @param value: mixed value to set
    @return myclips.Rule 
    '''
    for (i, field) in enumerate(instance[1]):
        if field[0] == fieldName:
            instance[1][i][1] = value
            break
    return instance

def myclips_PositivePredicate_setPattern(instance, pattern):
    """
    Set a pattern for PositivePredicate
    @param instance: myclips.PositivePredicate
    @param pattern: list a list of Symbols/Variable
    @return myclips.PositivePredicate 
    """
    instance[1][0][1] = pattern
    return instance

def myclips_PositivePredicate_setAssignment(instance, variable):
    """
    Set a variable binding for PositivePredicate
    @param instance: myclips.PositivePredicate
    @param variable: myclips.Variable
    @return myclips.PositivePredicate 
    """
    instance[1][1][1] = variable
    return instance

