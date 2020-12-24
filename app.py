# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 23:21:11 2020

@author: Acer
"""
import sys
import os
import bottle
from bottle import route, run, post, request, static_file,error,get,hook, response
from handle_auth import *
  


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


app = bottle.app()

@app.get("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="static/css")

@app.get("/static/font/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filepath):
    return static_file(filepath, root="static/font")

@app.get("/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="static/img")

@app.get("/static/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="static/js")

@app.get("/static/lib/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="static/lib/js")


@app.get("/static/lib/js/<filepath:re:.*\.map>")
def js(filepath):
    return static_file(filepath, root="static/lib/js")
@app.get("/static/lib/css/<filepath:re:.*\.css>")
def js(filepath):
    return static_file(filepath, root="static/lib/css")


@app.route('/')
def server_static(filepath="views/login.html"):
    return static_file(filepath, root= os.getcwd())


@app.route('/login', method = 'POST')
def process():
    name =  request.query['username']
    occupation =  request.query['password']
    print(occupation)
    return "Your name is {0} and you are a(n) {1}".format(name, occupation)


@app.error(404)
def error404(error):
    return '404 - the requested page could not be found'  



app.install(EnableCors())
app.run(host='localhost', reloader=True, port=9090, debug=True)