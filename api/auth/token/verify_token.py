# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:53:50 2020

@author: Acer
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:52:26 2020

@author: Acer
"""
import re
import os
import asyncio
import sys
import nest_asyncio
nest_asyncio.apply()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../../../api/'))
sys.path.append(BASE_DIR )
from project_dir import *

import pytz   
from functools import wraps ##windows rm rerror imports
from asyncio.proactor_events import _ProactorBasePipeTransport ##windows rm rerror imports
from generate import *
import datetime

class RefreshUserToken:
    
    def __init__(self,encrpted_token,cipher_suite):
         
         self.encrpted_token =  bytes(encrpted_token,encoding="utf-8")
         self.cipher_suite = cipher_suite
         self.user_id_key = ""
         self.current_token = str(self.encrpted_token)[2:-1] 
    
    
    
    
    async def verify_cookie_token(self):
        try:
            decoded_token = self.cipher_suite.decrypt(self.encrpted_token)
            return True
        except Exception as e:
            print("invalid toekn")
            return False
     
        
     
    async def retrive_usertokenidkey(self):
        try:
            if(await self.verify_cookie_token() == True):
                decode_token = str(self.cipher_suite.decrypt(self.encrpted_token))
                user_id_key =  (decode_token.split("useridkey",1)[1] [0:11])
                return user_id_key
            
        except Exception as e:
            print("error during retrival the token" + str(e))
            return False
          
     
        
    async def check_cookie_expiry_time(self):
        try:
            if(await self.verify_cookie_token() == True):
                decode_token = str(self.cipher_suite.decrypt(self.encrpted_token))[1:-1]
                
                current_time = float(datetime.datetime.now().timestamp())
                print(current_time)
                token_generate_time =  float(str((decode_token.split("timestamp",1)[1])))
                
                cookie_time = int(current_time - token_generate_time )
                print(cookie_time)
                
                if(cookie_time >= 300):
                    return True 
                else:
                    return False   
            
        except Exception as e:
            print("error checking time expiry token" + str(e))
            return False
        
     
        
     
    async def generate_refresh_token(self):
        try:
            if(await self.check_cookie_expiry_time() == True):
               self.user_id = await self.retrive_usertokenidkey()
               new_token = HandleTokenRequest( self.user_id ,self.cipher_suite )
               refreshed_token = new_token.perform_token_request()
               print("new Token generated")
               return refreshed_token 
            else:
                print("previous  Token returned")
                return self.current_token 
        except Exception as e:
            print("error during refreshing the token" + str(e))
          
            return False  
    
        
         

    


class HandleRefrehToken:
   
   def __init__(self,encrypted_token,cipher_suite):
       self.token_request = RefreshUserToken(encrypted_token,cipher_suite)
        

   async def handle_token_request(self):
       
       if(await self.token_request.verify_cookie_token() == True):
           token = await self.token_request.generate_refresh_token()
           return token
       else:
           return False
       
        
   def perform_token_request(self):
          """
           Cretes Async task to handle user login request separately
           """
          def silence_event_loop_closed(func):
                @wraps(func)
                def wrapper(self, *args, **kwargs):
                    try:
                        return func(self, *args, **kwargs)
                    except RuntimeError as e:
                        if str(e) != 'Event loop is closed':
                            raise
                return wrapper
          _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
          
          
          loop = asyncio.new_event_loop() 
          task_obj = loop.create_task(self.handle_token_request())
          encrypted_token = loop.run_until_complete(task_obj)
          return  encrypted_token
             




