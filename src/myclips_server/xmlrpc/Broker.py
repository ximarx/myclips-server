'''
Created on 10/lug/2012

@author: Francesco Capozzo
'''
import inspect

class Broker(object):
    '''
    MyClips-Server Service Broker
    '''

    def __init__(self, services):
        
        if isinstance(services, dict):
            self._services = services
        elif isinstance(services, list):
            self._services = {}
            for service in services:
                if self._services.has_key(service._TYPE):
                    self._services[service._NAME] = service
                else:
                    self._services[service._TYPE] = service
        
        
        for (sKey, Service) in self._services.items():
            setattr(self, sKey, Service)

    def services(self):
        return [(x, ".".join([y.__class__.__module__ , y.__class__.__name__])) for (x,y) in self._services.items()]
            
    @staticmethod
    def _vectorizeArgs(func):
        args, _, _, defaults = inspect.getargspec(func)
        return [(arg,) if defaults is None
                    else (arg, defaults[index]) if len(args) == len(defaults) 
                        else (arg, defaults[index - (len(args) - len(defaults))]) if (index - (len(args) - len(defaults))) >= 0
                            else (arg,) 
                for (index, arg) in enumerate(args) if (index > 0 or (index == 0 and args[0] != "self"))]

    def apis(self, aServiceName):
        theService = self._services[aServiceName]
        return [
                [
                 ".".join([aServiceName, func]), #SERVICENAME.func
                 self.__class__._vectorizeArgs(getattr(self._services[aServiceName], func))
                ] 
                for func in dir(theService) if func[0] != '_' and callable(getattr(theService, func))
            ]

#    def parseProduction(self, defrule):
#        parsedItems = clipsparser.parse(defrule)
#        
#        rule = parsedItems[0][1]
#        default_rule = {'name': '', 'lhs': [], 'rhs': [], 'declare': {'salience': 0}, 'description': ''}
#        default_rule.update(rule)
#        rule = default_rule
#        p = Production(rule['name'], rule['lhs'], rule['rhs'], rule['declare'], rule['description'])
#        MyClipsWrapper.i().rete.add_production(p)
#        
#
#    def assert_fact(self, *args, **kargs):
#        MyClipsWrapper.i().rete.assert_fact(*args, **kargs)

