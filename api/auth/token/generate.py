# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:52:26 2020

@author: Acer
"""
import re
import os
import asyncio
import random

from hashlib import sha256
from sqlalchemy.orm import sessionmaker
import sys
from bleach.sanitizer import Cleaner
import nest_asyncio
nest_asyncio.apply()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../../../api/'))
from faker import Faker
sys.path.append(BASE_DIR )
from project_dir import *
from db_connection import *
import datetime
import pytz   
from sqlalchemy import exc  
from functools import wraps ##windows rm rerror imports
from asyncio.proactor_events import _ProactorBasePipeTransport ##windows rm rerror imports

class GenetateUserTempToken:
    
    def __init__(self,user_id_key,cipher_suite):
        
         self.conn =  Database()
         self.conn = self.conn.initialise_db_connection()
         self.transaction = self.conn.begin()
         self.user_id_key = user_id_key
         self.cipher_suite = cipher_suite
    
    
    async def generate_encrypted_token(self):
        
        cleaner = Cleaner(tags=[], attributes={}, styles=[], protocols=[], strip=True, strip_comments=True, filters=None)
        faker = Faker()
        profile1 = faker.simple_profile()
        profile = list(profile1.values())
        profile_string = ''.join(map(str, profile)) 
        token_generate_time = datetime.datetime.now().timestamp()
        final_token_key = bytes(str(re.sub(r"[\n\t\s]*", "", cleaner.clean(profile_string))) +"useridkey" + self.user_id_key +"timestamp" + str(token_generate_time),encoding="utf-8")
        encrypted_token = self.cipher_suite.encrypt((final_token_key))
    
        
        return encrypted_token
               
    
            
         



class HandleTokenRequest:
   
   def __init__(self,useridkey,cipher_suite):
       self.token_request = GenetateUserTempToken(useridkey,cipher_suite)
        

   async def handle_token_request(self):
       token = await self.token_request.generate_encrypted_token()
       return token
         
       
        
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
          encrypted_token = str(encrypted_token)[2:-1]
          return  encrypted_token
