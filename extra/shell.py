
import xmlrpclib
import pprint
import sys
import thread
from SimpleXMLRPCServer import SimpleXMLRPCServer

def aStream():
    
    #aFile = open("./_THE_STREAM_.txt", "w")
    oFile = sys.stdout
    iFile = sys.stdin
    
    fakeStdOut = SimpleXMLRPCServer(("localhost", 55555), allow_none=True, logRequests=False)    
    fakeStdOut.register_function(lambda t: "pong", 'ping')    
    fakeStdOut.register_function(lambda t,s: oFile.write("RPC: "+s) or True, 'write')
    fakeStdOut.register_function(lambda *args: oFile.write("RPC: CLOSE!") or True, 'close')
    fakeStdOut.register_function(lambda t: oFile.write("RPC Input: ") or iFile.readline(), 'readline')
    
    thread.start_new_thread(fakeStdOut.serve_forever, ())


def gs():
    return xmlrpclib.Server('http://localhost:8081', allow_none=True)

def myself():
    return xmlrpclib.Server('http://localhost:55555', allow_none=True)


pp = pprint.pprint

s = gs()
aToken = s.Sessions.new()

def linkStream():
    
    aStream()
    
    s.ClientIO.register(aToken, "t", "http://localhost:55555", 324)
    s.ClientIO.register(aToken, "stdout", "http://localhost:55555", 324)
    s.ClientIO.register(aToken, "stdin", "http://localhost:55555", 324)
    
    


print "type:"
print "    pp(s.services())"
print "        : get services list"
print "    pp(s.apis(SERVICENAME))"
print "        : get the list of apis in the service"
print "    linkStream()"
print "        : redirect server output streams here!"
print

