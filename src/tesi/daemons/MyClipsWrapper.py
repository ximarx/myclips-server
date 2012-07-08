'''
Created on 08/lug/2012

@author: Francesco Capozzo
'''
from icse.rete.ReteNetwork import ReteNetwork
from icse.Production import Production
from icse.predicates.Predicate import PositivePredicate
from icse.predicates.Eq import Eq

class MyClipsWrapper(object):
    '''
    classdocs
    '''

    __i = None

    def __init__(self):
        '''
        Constructor
        '''
        self.rete = ReteNetwork()
        self.rete.assert_fact([])
        self.rete.assert_fact([1,2,3])
        self.rete.assert_fact([2,2])
        self.rete.add_production(Production('regola1',
                                            lhs=[
                                                 (PositivePredicate, [(Eq, 1), (Eq, 2), (Eq, 3) ]),
                                                 (PositivePredicate, [(Eq, 2), (Eq, 2) ]),
                                                 ],
                                            rhs=[],
                                            properties=None, description="Regola di prova"))
        
        self.rete.add_production(Production('regola2',
                                            lhs=[
                                                 (PositivePredicate, [(Eq, 1), (Eq, 2), (Eq, 3) ]),
                                                 ],
                                            rhs=[],
                                            properties={'salience':100},
                                            description="Regola di prova"))

    @classmethod
    def i(cls):
        if cls.__i == None:
            cls.__i = cls()
        return cls.__i