


class Services(object):
    from myclips_server.xmlrpc.services.Rules import Rules as RulesImpl
    Rules = RulesImpl
    
    from myclips_server.xmlrpc.services.WorkingMemory import WorkingMemory as WorkingMemoryImpl
    WorkingMemory = WorkingMemoryImpl
    
    from myclips_server.xmlrpc.services.TypeFactory import TypeFactory as TypeFactoryImpl
    TypeFactory = TypeFactoryImpl
    
    from myclips_server.xmlrpc.services.SessionsManager import SessionsManager as SessionsManagerImpl
    SessionsManager = SessionsManagerImpl
    
    pass
    
    
    
    