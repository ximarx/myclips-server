'''
Created on 10/lug/2012

@author: Francesco Capozzo
'''
import icse.parser as clipsparser
from icse.Production import Production
from tesi.daemons.MyClipsWrapper import MyClipsWrapper
import inspect

class API(object):
    '''
    MyClips XML-RPC api
    '''

    def __init__(self, services):
        class fakeobj(object):
            def __init__(self):
                self.assert_fact = MyClipsWrapper().i().rete.assert_fact
                
        self.RETE = fakeobj()
        #setattr(self.RETE, "assert_fact", MyClipsWrapper().i().rete.assert_fact)
        #self.RETE.assert_fact = MyClipsWrapper().i().rete.assert_fact
        
        
        if not isinstance(services, dict):
            services = {}

        self._services = services
        
        for (sKey, Service) in services.items():
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

    def apis(self, service):
        return [
                [
                 ".".join([service, func]), #SERVICENAME.func
                 API._vectorizeArgs(getattr(self._services[service], func))
                ] 
                for func in dir(self._services[service]) if func[0] != '_'
            ]

    def parseProduction(self, defrule):
        parsedItems = clipsparser.parse(defrule)
        
        rule = parsedItems[0][1]
        default_rule = {'name': '', 'lhs': [], 'rhs': [], 'declare': {'salience': 0}, 'description': ''}
        default_rule.update(rule)
        rule = default_rule
        p = Production(rule['name'], rule['lhs'], rule['rhs'], rule['declare'], rule['description'])
        MyClipsWrapper.i().rete.add_production(p)
#        
#
#    def assert_fact(self, *args, **kargs):
#        MyClipsWrapper.i().rete.assert_fact(*args, **kargs)

