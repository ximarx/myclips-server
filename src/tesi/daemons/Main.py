'''
Created on 08/lug/2012

@author: Francesco Capozzo
'''
from bottle import run, default_app, response
import bottle


if __name__ == '__main__':
    
    #default_app.push()
    
    def allow_origin(callback):
        def wrapper(*args, **kwargs):
            body = callback(*args, **kwargs)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return body
        return wrapper
    
    bottle.install(allow_origin)    
    
    import tesi.daemons.restful.routes
    
    #app = default_app.pop()
    
    #run(app, host='localhost', port=8080, debug=True)
    run(host='localhost', port=8080, debug=True)
    
    