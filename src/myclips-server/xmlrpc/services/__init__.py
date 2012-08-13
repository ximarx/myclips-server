


class Services(object):
    from myclips-server.xmlrpc.services.Rules import Rules as RulesImpl
    Rules = RulesImpl
    
    from myclips-server.xmlrpc.services.WorkingMemory import WorkingMemory as WorkingMemoryImpl
    WorkingMemory = WorkingMemoryImpl
    
    from myclips-server.xmlrpc.services.TypeFactory import TypeFactory as TypeFactoryImpl
    TypeFactory = TypeFactoryImpl
    
    from myclips-server.xmlrpc.services.SessionsManager import SessionsManager as SessionsManagerImpl
    SessionsManager = SessionsManagerImpl
    
    pass
    
    
    
    