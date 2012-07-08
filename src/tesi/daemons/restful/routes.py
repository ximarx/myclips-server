'''
Created on 08/lug/2012

@author: Francesco Capozzo
'''

from bottle import route, default_app, response
from tesi.daemons.MyClipsWrapper import MyClipsWrapper
from icse.rete.ReteNetwork import ReteNetwork
import json
import cgi

@route('/')
def GET_index():
    app = default_app()
    return "<html><body><h1>MyClips RESTful API</h1><pre>{0}</pre></body></html>".format(
                    "</pre><pre>".join([cgi.escape(x.method + " " + x.rule) for x in app.routes])                                            
                )

@route('/wmes', method='GET')
def GET_wmes():
    rete = MyClipsWrapper.i().rete
    assert isinstance(rete, ReteNetwork)
    
    wmes = rete.get_wmes()
    
    return {'facts': [{'fact': x.get_factid(), 'values': x.get_fact()} for x in wmes]}
    
@route('/activations', method='GET')
def GET_activations():
    #response.headers.append('Access-Control-Allow-Origin', '*')
    rete = MyClipsWrapper.i().rete
    assert isinstance(rete, ReteNetwork)
    
    actv = rete.agenda().activations()
    return {'activations': [{'salience': salience, 'rule': pnode.get_name(), 'token': [wme.get_factid() for wme in token.linearize(False)]} for (salience, pnode, token) in actv]}

@route('/fact/<factid:int>')
def GET_fact(factid):
    rete = MyClipsWrapper.i().rete
    assert isinstance(rete, ReteNetwork)
    
    fact = rete.get_wme(factid)
    return {'fact': factid, 'values': fact.get_fact()}
    