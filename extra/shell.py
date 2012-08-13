
import xmlrpclib
import pprint


def gs():
    return xmlrpclib.Server('http://localhost:8081')

def demo():
    
    s = gs()
    
    print "    >> Creating a new rule instance -> rule"
    print '        rule = s.TYPES.newInstance("myclips.Rule")'
    rule = s.TYPES.newInstance("myclips.Rule")
    pp(rule)
    print '                    ...press enter...'
    print
    raw_input()

    print "    >> Setting rule name to 'NomeDellaRegola'"
    print '        rule = s.TYPES.do(rule, "setName", "NomeDellaRegola")'
    rule = s.TYPES.do(rule, "setName", "NomeDellaRegola")
    pp(rule)
    print '                    ...press enter...'
    print
    raw_input()

    print "    >> Creating a new pattern-CE instance (PositivePredicate type) -> pospred"
    print '        pospred = s.TYPES.newInstance("myclips.PositivePredicate")'
    pospred = s.TYPES.newInstance("myclips.PositivePredicate")
    pp(pospred)
    print '                    ...press enter...'
    print
    raw_input()

    print "    >> Setting pattern constraints in pattern-CE instance"
    print '        pospred = s.TYPES.do(pospred, "setPattern", [1,1,"A"])'
    pospred = s.TYPES.do(pospred, "setPattern", [1,1,"A"])
    pp(pospred)
    print '                    ...press enter...'
    print
    raw_input()

    print "    >> Setting created pattern as rule lhs"
    print '        rule = s.TYPES.do(rule, "setField", "lhs", [pospred])'
    rule = s.TYPES.do(rule, "setField", "lhs", [pospred])
    pp(rule)
    print '                    ...press enter...'
    print
    raw_input()


pp = pprint.pprint

s = gs()

print "type:"
print "    pp(s.services())"
print "        : get services list"
print "    pp(s.apis(SERVICENAME))"
print "        : get the list of apis in the service"
print "    demo()"
print "        : show a little demo"
print

