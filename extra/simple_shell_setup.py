
import xmlrpclib
import pprint


def gs():
    return xmlrpclib.Server('http://localhost:8081')

pp = pprint.pprint

print "type:"
print "    s = gs()"
print "    pp(s.services())"

