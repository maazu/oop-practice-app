# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:52:26 2020

@author: Maaz
"""
import os
import random
from hashlib import sha256
from sqlalchemy.orm import sessionmaker
import sys
import asyncio
import nest_asyncio
nest_asyncio.apply()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../../api/'))
sys.path.append(BASE_DIR )
from project_dir import *
from db_connection import *
from datetime import datetime 
import pytz    
from sqlalchemy import exc      
  
class CreateAdmin:
    
    def __init__(self, name, username, email, cell_num, password,auth_access):
        
        
        self.conn =  Database()
        self.conn = self.conn.initialise_db_connection()
        self.transaction = self.conn.begin()
        self.unique_id =  ""
        self.name = name
        self.username = username
        self.email = email
        self.cell_num = cell_num
        self.password = password
        self.auth_access = auth_access
        self.reg_date = ""
        self.last_login = "NA"
        self.verifcation = "No"
        self.login_count = 0
     
        
    async def get_current_time(self):
        """
        Return the current time to log user registration

        """
        
        IST = pytz.timezone('Asia/Karachi') 
        now = datetime.now(IST) 
        reg_date = str(now.strftime('%Y-%m-%d %H:%M:%S'))
        self.reg_date = reg_date 
        return self.reg_date 
    
        
    async def sanitize_user_input(self):
        
        cleaner = Cleaner(tags=[], attributes={}, styles=[], protocols=[], strip=True, strip_comments=True, filters=None)
        self.name = (cleaner.clean(self.name))
        self.username = (cleaner.clean(self.username))
        self.email = (cleaner.clean(self.email))
        self.cell_num = (cleaner.clean(self.cell_num))
        self.password = (cleaner.clean(self.password))
        self.auth_access =  (cleaner.clean(self.auth_access))
    
    
    
    async def encrypt_user_password(self):
        
        self.password = sha256((self.password).encode('utf-8')).hexdigest()
        return self.password
        
    
    
    async def check_admin_exist(self):
        
        query ='SELECT * FROM auth_users where email = (%s) or username = (%s);'
        result =  self.conn.execute(query,self.email,self.username)
        record  = result.fetchall()
        if(len(record) > 0):
            return True
        else:
            return False  
    

    async def generate_uniq_useridkey(self):
        
        characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        self.unique_id = ''
        for i in range(0, 11):
            self.unique_id += random.choice(characters)
        query ='SELECT * FROM auth_users where useridkey = %s;'
        result =  self.conn.execute(query,self.unique_id)    
        record  = len(result.fetchall())
        if(record == 0):
            return self.unique_id
        else:
            await self.generate_uniq_useridkey()
    


    async def add_new_admin(self):
        """
        Adds a new admin 
    
        """
        try:  
            self.unique_id = await self.generate_uniq_useridkey()
            self.reg_date = await self.get_current_time()
            self.password = await self.encrypt_user_password() 
                           
            query = "INSERT INTO auth_users VALUES (%s,%s, %s, %s,%s,%s, %s, %s, %s ,%s, %s, %s);"
            result = self.conn.execute(query,'',self.unique_id,self.name,self.username,self.email,self.cell_num,self.password,self.reg_date,self.last_login,self.auth_access,self.verifcation, self.login_count )
            
        except exc.SQLAlchemyError:
            self.transaction.rollback()
            raise
            return False
        else:
            self.transaction.commit()
            return True
       
        
       
        
    async def close_database(self):
        """
        Close  the database connection.
    
        """
        self.conn.close()
   
  
