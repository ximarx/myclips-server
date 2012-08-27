
import xmlrpclib
import pprint
import sys
import thread
from SimpleXMLRPCServer import SimpleXMLRPCServer

def aStream():
    
    #aFile = open("./_THE_STREAM_.txt", "w")
    oFile = sys.stdout
    iFile = sys.stdin
    
    fakeStdOut = SimpleXMLRPCServer(("localhost", 0), allow_none=True, logRequests=False)    
    fakeStdOut.register_function(lambda t: "pong", 'Stream.ping')
    fakeStdOut.register_function(lambda t: "pong", 'Listener.ping')    
    fakeStdOut.register_function(lambda t,s: oFile.write("RPC: "+s+"\n") or True, 'Stream.write')
    fakeStdOut.register_function(lambda *args: oFile.write("RPC: CLOSE!") or True, 'Stream.close')
    fakeStdOut.register_function(lambda t: oFile.write("RPC Input: ") or iFile.readline(), 'Stream.readline')
    fakeStdOut.register_function(lambda t,en,*args: oFile.write("RPC Notify: [%s] %s\n"%(en, repr(args))) or True, 'Listener.notify')
    
    thread.start_new_thread(fakeStdOut.serve_forever, ())
    
    #return fakeStdOut.server_address
    return "http://%s:%s"%tuple([str(x) for x in fakeStdOut.server_address]) 


def gs():
    return xmlrpclib.Server('http://localhost:8081', allow_none=True, verbose=False)


pp = pprint.pprint

s = gs()

aToken = s.Sessions.new()

def linkStream():
    
    aAddress = aStream()
    
    s.ClientIO.register(aToken, "t", aAddress, 324)
    s.ClientIO.register(aToken, "stdout", aAddress, 324)
    s.ClientIO.register(aToken, "stdin", aAddress, 324)
    s.ClientIO.register(aToken, "wtrace", aAddress, 324)
    
def linkListener():
    
    aAddress = aStream()
    s.ClientEvents.register(aToken, "aListener%s"%aAddress, aAddress, 213, 'fact-retracted', 'fact-asserted', 'node-added' )
    
def tryDraw():
    
    s.RemoteShell.do(aToken, '(defrule r (A B C) =>)')
    s.RemoteShell.do(aToken, '(draw-circuit wtrace r)')
    
def tryAddRule():
    return s.Engine.addDefRule(aToken, 
                        s.Registry.new('DefRuleConstruct', 
                                       {
                                            'defruleName': 'BLABLA', 
                                            'lhs': [
                                                s.Registry.new('OrderedPatternCE', 
                                                               {
                                                                    'constraints': [
                                                                        s.Registry.new('Symbol', {'content': 'A'})
                                                                        ]
                                                                })
                                                ]
                                        }))
    
    
def tryAssertTemplate():
    
    pp(s.RemoteShell.do(aToken, '(deftemplate tmpl (slot A) (slot B))'))
    pp(s.RemoteShell.do(aToken, '(assert (tmpl (A 10) (B 100)))'))
    
    

print "type:"
print "    pp(s.services())"
print "        : get services list"
print "    pp(s.apis(SERVICENAME))"
print "        : get the list of apis in the service"
print "    linkStream()"
print "        : redirect server output streams here!"
print "    linkListener()"
print "        : redirect events here!"
print "    tryAddRule()"
print "        : add a new rule"
print "    tryDraw()"
print "        : draw a rule"
print "    tryAssertTemplate()"
print "        : add a deftemplate + assert a new template-fact"
print

