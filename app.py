
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 01:52:11 2020

@author: Maaz
"""
import os
import sys
from flask import Flask,redirect,url_for,render_template , request, jsonify,make_response
from flask_cors import CORS, cross_origin
sys.path.insert(0 , os.getcwd() + '/handler/')
from app_request_handler import *
from cryptography.fernet import Fernet


app = Flask(__name__, template_folder="templates", static_folder="static")


CORS(app)
app.config['SERVER_NAME'] = 'localhost:9090'
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_SORT_KEYS'] = False
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)
CORS(app, resources={r"/*": {"origins": "*"}})

   
key = Fernet.generate_key()    
cipher_suite = Fernet(key)


def send_auth_reponse(user_cookie_token,template_page_name):
    
    get_fresh_token = HandleRefrehToken(user_cookie_token,cipher_suite)
    refrehed_token = str(get_fresh_token.perform_token_request())
    print(refrehed_token)
    if(refrehed_token != "False"):
        response = make_response((render_template(template_page_name)))
        response.set_cookie( key="token", value = str(refrehed_token), httponly=True, samesite='Lax', max_age= 1200)
        return response
    
    else:  
        response = make_response(redirect('/'))
        return response
    
    





@app.route('/login')
@app.route('/')
def home():
    response = make_response((render_template("login.html"))) 
       
    return response




    



@app.route('/login-request',methods = ['POST'])
@cross_origin()
def handle_user_login_request():
    username = str(request.values.get('username'))
    password = str(request.values.get('password'))
    email = str(request.values.get('email'))
   
    validation_request = ReguestLogin(username,email,password)
    user_id_key = validation_request.perform_login_action()
    
    if( user_id_key[0] == "VALID"):
             token = HandleTokenRequest(str(user_id_key[1][0]),cipher_suite)
             token = token.perform_token_request()
             
             response = make_response(redirect(('/dashboard')))
             response.set_cookie( key="token", value = str(token), httponly=True, samesite='Lax', max_age= 1200)
             
    elif(user_id_key[0] == "INVP"):
         
        response = make_response('/')
       
    elif(user_id_key[0] == "updatefailure"):
         response = make_response('/')
        
    else:
        response = make_response('/')
       
    return response
    





@app.route('/dashboard')
@cross_origin()
def handle_dashboard_page():
    user_cookie_token  = (request.cookies.get('token'))
    
    if(user_cookie_token != None):
       response = send_auth_reponse(user_cookie_token,"dashboard.html")
    else:
         response = make_response(redirect(('/')))
         
    return response



@app.route('/logout')
def logout():
    response = make_response(redirect(('/')))
    response.set_cookie( key="token", value = "loggedout", httponly=True, samesite='Lax', max_age= 0.5)
    return response







if __name__ == '__main__':
    app.run(debug=True)