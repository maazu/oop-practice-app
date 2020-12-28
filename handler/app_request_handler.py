# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 02:23:44 2020

@author: Acer
"""
import asyncio
import os 
import sys

from threading import Thread
from cryptography.fernet import Fernet

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
print(BASE_DIR)
if(BASE_DIR + '/applog/' not in sys.path):
    sys.path.insert(0, BASE_DIR + '/applog/')
    sys.path.insert(0, BASE_DIR + '/api/')
    sys.path.insert(0, BASE_DIR +'/api/auth/token/')
    sys.path.insert(0, BASE_DIR + '/api/config/')
    sys.path.insert(0, BASE_DIR + '/api/user/admin/login/')
    sys.path.insert(0, BASE_DIR + '/api/user/admin/register/')

from handle_login_request import *
from generate import *
from verify_token import *




def validate_login(username,email,password,cipher_key):
     
     validation_request = ReguestLogin(username,email,password)
     user_id_key = validation_request.perform_login_action()
     
     if( user_id_key[0] == "VALID"):
             token = HandleTokenRequest(str(user_id_key[1][0]),cipher_key)
             token = token.perform_token_request()
             return [user_id_key[0],token]
         
     elif(user_id_key[0] == "INVP"):
         return ["invalid password"]
    
     elif(user_id_key[0] == "updatefailure"):
         return ["something went wrong !"]
     
     else:
        return ["user does not exist"]

    

def get_encrypted_userlogin_token(username,email,password,cipher_suite):
    user_login_token = validate_login(username,email,password,cipher_suite)
    #user_login_token = str(user_login_token)[2:-1]
    return user_login_token
    
    


def verifiy_user_cookie_token(encrpted_token,cipher_suite):
    try:
       decoded_token2 = cipher_suite.decrypt(bytes(encrpted_token,encoding ="utf-8"))
       print(decoded_token2)
       return True
    except Exception as e:
        print(e)
        return "invalid token"


   
    
def get_refreshed_token(previous_token):
     if(verifiy_userlogin_token(previous_token)):
         
         token = HandleTokenRequest(str(user_id_key[1][0]),cipher_key)
         token = token.perform_token_request()
    
    
    
