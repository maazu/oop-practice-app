# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:52:26 2020

@author: Maaz
"""
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

sys.path.append(BASE_DIR )
from project_dir import *
from db_connection import *
from datetime import datetime 
import pytz   
from sqlalchemy import exc  

class AdminLogin:
    

    def __init__(self, username, email, password):
        
        self.conn =  Database()
        self.conn = self.conn.initialise_db_connection()
        self.transaction = self.conn.begin()
        self.username = str(username)
        self.email = str(email)
        self.password = sha256((password).encode('utf-8')).hexdigest()
        self.current_time =  ""
       
        
  
    
            
    async def sanitize_user_input(self):
        """
        Sanitize user input, removes all htmls characters and apply unicode 
        where applicable.
        """
        cleaner = Cleaner(tags=[], attributes={}, styles=[], protocols=[], strip=True, strip_comments=True, filters=None)
        self.username = (cleaner.clean(self.username))
        self.email = (cleaner.clean(self.email))
        self.password = (cleaner.clean(self.password))
   
        
   
  
    async def check_admin_exist(self):
        
        query = 'SELECT * FROM auth_users where email = %s or username = %s ;'
        result =   self.conn.execute(query,self.email,self.username)
        record  =  result.fetchall()
        if(len(record) > 0):
            return True
        else:
             return False  
         
            
         
    async def retrive_user_id_key(self):
        
        query =  "SELECT useridkey FROM auth_users where username = %s;"
        result =  self.conn.execute(query,self.username)
        record  = result.fetchall()
        record  = [user_id[0] for user_id in record]
        print(record)
        if(len(record) > 0):
            
            return record
        
        else:
            return False  
         

    async def match_password(self):
        
        query =  "SELECT * FROM auth_users where password =  %s AND username = %s;"
        result =  self.conn.execute(query,self.password,self.username)
        record  = result.fetchall()
        if(len(record) > 0):
            
            return True
        
        else:
            return False  
    
    
    async def get_current_time(self):
        
        IST = pytz.timezone('Asia/Karachi') 
        now = datetime.now(IST) 
        login_record_time = str(now.strftime('%Y-%m-%d %H:%M:%S'))
        return login_record_time
    
   

    async def update_login_history(self):
        try:
            self.current_time = await self.get_current_time() 
            
            query = "UPDATE auth_users SET last_login  = (%s),login_count = login_count + (%s) where username = %s  or email = (%s) ;"
            result =  self.conn.execute(query,self.current_time,1,self.username,self.email)
            
        except exc.SQLAlchemyError:
            self.transaction.rollback()
            raise
            return False
        else:
            self.transaction.commit()
            return True
        
   
    
   
    async def close_database(self):
        self.conn.close()
