'''
Created on Tue Aug 14 12:31:49 2012

@author: Francesco Capozzo
'''

from myclips_server.xmlrpc.services.types.Skeleton import Skeleton



class AndPatternCE(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.AndPatternCE'
    __PROPERTIES__ = {
        "patterns" : None
    }


class Lexeme(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.Lexeme'
    __PROPERTIES__ = {
        "content" : None
    }


class TemplateRhsPattern(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.TemplateRhsPattern'
    __PROPERTIES__ = {
        "templateName" : None,
		"templateSlots" : None
    }


class PositiveTerm(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.PositiveTerm'
    __PROPERTIES__ = {
        "term" : None
    }


class DefFunctionConstruct(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.DefFunctionConstruct'
    __PROPERTIES__ = {
        "functionName" : None,
		"comment" : None,
		"params" : None,
		"actions" : None
    }


class Integer(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.Integer'
    __PROPERTIES__ = {
        "content" : None
    }


class FieldLhsSlot(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.FieldLhsSlot'
    __PROPERTIES__ = {
        "slotName" : None,
		"slotValue" : None
    }


class MultiFieldVariable(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.MultiFieldVariable'
    __PROPERTIES__ = {
        "content" : None
    }


class DefGlobalConstruct(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.DefGlobalConstruct'
    __PROPERTIES__ = {
        "moduleName" : None,
		"assignments" : None
    }


class TestPatternCE(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.TestPatternCE'
    __PROPERTIES__ = {
        "function" : None
    }


class DefaultAttribute(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.DefaultAttribute'
    __PROPERTIES__ = {
        "defaultValue" : None
    }


class OrderedRhsPattern(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.OrderedRhsPattern'
    __PROPERTIES__ = {
        "values" : None
    }


class SingleFieldLhsSlot(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.SingleFieldLhsSlot'
    __PROPERTIES__ = {
        "slotName" : None,
		"slotValue" : None
    }


class Constraint(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.Constraint'
    __PROPERTIES__ = {
        "constraint" : None
    }


class ImportSpecification(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.ImportSpecification'
    __PROPERTIES__ = {
        "item" : None,
		"moduleName" : None
    }


class UnnamedMultiFieldVariable(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.UnnamedMultiFieldVariable'
    __PROPERTIES__ = {
        "content" : None
    }


class Variable(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.Variable'
    __PROPERTIES__ = {
        "content" : None
    }


class GlobalAssignment(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.GlobalAssignment'
    __PROPERTIES__ = {
        "variable" : None,
		"value" : None,
		"runningValue" : None
    }


class SingleFieldVariable(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.SingleFieldVariable'
    __PROPERTIES__ = {
        "content" : None
    }


class Attribute(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.Attribute'
    __PROPERTIES__ = {
        
    }


class TemplatePatternCE(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.TemplatePatternCE'
    __PROPERTIES__ = {
        "templateName" : None,
		"templateSlots" : None
    }


class SlotDefinition(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.SlotDefinition'
    __PROPERTIES__ = {
        "slotName" : None,
		"attributes" : None
    }


class BaseParsedType(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.BaseParsedType'
    __PROPERTIES__ = {
        "content" : None
    }


class DefTemplateConstruct(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.DefTemplateConstruct'
    __PROPERTIES__ = {
        "templateName" : None,
		"templateComment" : None,
		"slots" : None
    }


class Float(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.Float'
    __PROPERTIES__ = {
        "content" : None
    }


class MultiFieldRhsSlot(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.MultiFieldRhsSlot'
    __PROPERTIES__ = {
        "slotName" : None,
		"slotValue" : None
    }


class Symbol(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.Symbol'
    __PROPERTIES__ = {
        "content" : None
    }


class NegativeTerm(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.NegativeTerm'
    __PROPERTIES__ = {
        "term" : None
    }


class TypeAttribute(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.TypeAttribute'
    __PROPERTIES__ = {
        "allowedTypes" : None
    }


class NotPatternCE(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.NotPatternCE'
    __PROPERTIES__ = {
        "pattern" : None
    }


class SingleFieldRhsSlot(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.SingleFieldRhsSlot'
    __PROPERTIES__ = {
        "slotName" : None,
		"slotValue" : None
    }


class InstanceName(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.InstanceName'
    __PROPERTIES__ = {
        "content" : None
    }


class FieldRhsSlot(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.FieldRhsSlot'
    __PROPERTIES__ = {
        "slotName" : None,
		"slotValue" : None
    }


class Term(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.Term'
    __PROPERTIES__ = {
        "term" : None
    }


class ConnectedConstraint(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.ConnectedConstraint'
    __PROPERTIES__ = {
        "constraint" : None,
		"connectedConstraints" : None
    }


class String(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.String'
    __PROPERTIES__ = {
        "content" : None
    }


class PortItem(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.PortItem'
    __PROPERTIES__ = {
        "portType" : None,
		"portNames" : None
    }


class Number(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.Number'
    __PROPERTIES__ = {
        "content" : None
    }


class OrPatternCE(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.OrPatternCE'
    __PROPERTIES__ = {
        "patterns" : None
    }


class FunctionCall(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.FunctionCall'
    __PROPERTIES__ = {
        "funcName" : None,
		"funcArgs" : None
    }


class PatternCE(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.PatternCE'
    __PROPERTIES__ = {
        
    }


class SingleSlotDefinition(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.SingleSlotDefinition'
    __PROPERTIES__ = {
        "slotName" : None,
		"attributes" : None
    }


class ExportSpecification(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.ExportSpecification'
    __PROPERTIES__ = {
        "item" : None
    }


class MultiSlotDefinition(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.MultiSlotDefinition'
    __PROPERTIES__ = {
        "slotName" : None,
		"attributes" : None
    }


class GlobalVariable(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.GlobalVariable'
    __PROPERTIES__ = {
        "content" : None
    }


class NullValue(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.NullValue'
    __PROPERTIES__ = {
        "content" : None
    }


class MultiFieldLhsSlot(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.MultiFieldLhsSlot'
    __PROPERTIES__ = {
        "slotName" : None,
		"slotValue" : None
    }


class DefModuleConstruct(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.DefModuleConstruct'
    __PROPERTIES__ = {
        "moduleName" : None,
		"comment" : None,
		"comment" : None,
		"specifications" : None
    }


class AssignedPatternCE(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.AssignedPatternCE'
    __PROPERTIES__ = {
        "variable" : None,
		"pattern" : None
    }


class UnnamedSingleFieldVariable(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.UnnamedSingleFieldVariable'
    __PROPERTIES__ = {
        "content" : None
    }


class DefFactsConstruct(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.DefFactsConstruct'
    __PROPERTIES__ = {
        "deffactsName" : None,
		"deffactsComment" : None,
		"rhs" : None
    }


class RuleProperty(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.RuleProperty'
    __PROPERTIES__ = {
        "propertyName" : None,
		"propertyValue" : None
    }


class DefRuleConstruct(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.DefRuleConstruct'
    __PROPERTIES__ = {
        "defruleName" : None,
		"defruleComment" : None,
		"defruleDeclaration" : None,
		"lhs" : None,
		"rhs" : None
    }


class OrderedPatternCE(Skeleton):
    
    __CLASS__ = 'myclips.parser.Types.OrderedPatternCE'
    __PROPERTIES__ = {
        "constraints" : None
    }

class Fact(Skeleton):
    __CLASS__ = 'myclips.Fact.Fact'
    __PROPERTIES__ = {
        'templateName' : None,
        'moduleName' : None,
        'values' : None
    }

class WME(Skeleton):
    __CLASS__ = 'myclips.rete.WME.WME'
    __PROPERTIES__ = {
        'factId' : None,
        'fact' : None
    }

