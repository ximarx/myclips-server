'''
Created on 10/lug/2012

@author: Francesco Capozzo
'''
import icse.parser as clipsparser
from icse.Production import Production
from tesi.daemons.MyClipsWrapper import MyClipsWrapper

class API(object):
    '''
    MyClips XML-RPC api
    '''

    def parseProduction(self, defrule):
        parsedItems = clipsparser.parse(defrule)
        
        rule = parsedItems[0][1]
        default_rule = {'name': '', 'lhs': [], 'rhs': [], 'declare': {'salience': 0}, 'description': ''}
        default_rule.update(rule)
        rule = default_rule
        p = Production(rule['name'], rule['lhs'], rule['rhs'], rule['declare'], rule['description'])
        MyClipsWrapper.i().rete.add_production(p)
        
        

    def assert_fact(self, *args, **kargs):
        MyClipsWrapper.i().rete.assert_fact(*args, **kargs)
