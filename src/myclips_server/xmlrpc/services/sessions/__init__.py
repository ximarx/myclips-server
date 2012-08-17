from functools import wraps


def renewer(theFunction):
    """
    This decorator allow to automatically renew
    a sessionToken when an api method is called
    """
    
    @wraps(theFunction)
    def decorator(*args, **kwargs):
        args[0]._broker.Sessions.renew(args[1])
        theReturn = theFunction(*args, **kwargs)
        args[0]._broker.Sessions.renew(args[1])
        return theReturn
        
    return decorator
