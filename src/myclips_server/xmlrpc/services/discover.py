'''
Created on 13/ago/2012

@author: Francesco Capozzo
'''

import myclips_server.xmlrpc.services as services
import sys
from genericpath import exists, isdir, isfile
from dircache import listdir
import os
import time
import importlib
import inspect
from myclips_server.xmlrpc.services.Service import Service
import json


class Logger(object):
        def __init__(self, filename="REPORT.txt"):
            self.terminal = sys.stdout
            self.log = open(filename, "w")

        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)


def getPaths(basePath, pathsVector):
    
    thisDirPaths = [basePath + "/" + x for x in listdir(basePath) if isdir(basePath + "/" + x)]
    for path in thisDirPaths:
        pathsVector.append(path)
        getPaths(path, pathsVector)
        
    return pathsVector



def discover(pathlist=None, manifestFile=None, basePackage="myclips_server.xmlrpc.services"):
    pathlist = pathlist or services.SERVICES_DIRS
    pathlist = pathlist if isinstance(pathlist, (list, tuple)) else [pathlist]
    manifestFile = manifestFile or "./"+services.SERVICES_MANIFEST
    reportFile = os.path.dirname(manifestFile) + "/REPORT.txt" 
    
    stats = {"services": 0,
             "types": {}}

    sys.stdout = Logger(reportFile)
    
    print "//:~ MyCLIPS-Server services discovery report: ", time.asctime()
    print
    
    validClasses = []
    
    for aDir in pathlist:
        
        theDirs = getPaths(aDir, [aDir])
        
        for theDir in theDirs:
        
            theRelativePackage = basePackage + (theDir.replace(aDir, "").replace("/", "."))
            
            print theRelativePackage
            
            for theFile in [x for x in listdir(theDir) if isfile(theDir + "/" + x) and x[-3:] == '.py' and x[0] != '_']:
            
                theModule = theFile[0:-3]
                
                theModuleComplete = "%s.%s"%(theRelativePackage, theModule)
                
                print "\t|--- ."+theModule
                
                try:
                    theModuleObject = importlib.import_module(theModuleComplete)
                except ImportError, e:
                    # if error ignore this module
                    print e
                    continue
                else:
                    for theName, theClass in [(x,y) for (x,y) in inspect.getmembers(theModuleObject) if isinstance(y, type)]:
                        if issubclass(theClass, Service) and theClass != Service:
                            print "\t:   \t|--- .%s (%s : %s)"%(theName, theClass._TYPE, theClass._NAME)
                            validClasses.append({"module"
                                                    : "%s.%s"%(theRelativePackage, theModule),
                                                 "class"
                                                    : theName,
                                                 "name"
                                                    : theClass._NAME,
                                                 "type"
                                                    : theClass._TYPE})
                            stats['services'] += 1
                            if not stats['types'].has_key(theClass._TYPE):
                                stats['types'][theClass.TYPE] = [theClass.NAME]
                            else:
                                stats['types'][theClass.TYPE].append(theClass.NAME)

            
    fr = open(manifestFile, "w")
    json.dump(validClasses, fr, indent=4)
    fr.close()

    
    statsString = """
================================
Number of types: {1}
{2}

Number of services: {0}

================================
"""

    perGroupString = """\
  |- {0}:
{1}"""
    perNameString = """\
  :   |- {0}"""
    
    print statsString.format(str(stats['services']), #{0}
                             str(len(stats['types'])), #{1}
                             #"\n".join([perGroupString.format(group, str(funcs)) for (group, funcs) in stats['groups'].items()]), #{2}
                             "\n".join([perGroupString.format(theTypeName,
                                                              "\n".join([perNameString.format(theName) for theName in theType])
                                                              ) for (theTypeName, theType) in stats["types"].items()])
                                 
                             )
    
    print "//:~ ", time.asctime()    
    

if __name__ == '__main__':
    
    discover()
    