# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:52:26 2020

@author: Acer
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
print(BASE_DIR)
sys.path.append(BASE_DIR )
from project_dir import *
from db_connection import *
from datetime import datetime 
import pytz    
    
  
   

class RegisterAdmin:
    
    def __init__(self, name, username, email, cell_num, password,auth_access):
        self.conn =  Database()
        self.conn = self.conn.create_connection()
        self.transaction = self.conn.begin()
        self.unique_id =  self.generate_uniq_useridkey()
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
     
        
    async def get_current_time():
        
        IST = pytz.timezone('Asia/Karachi') 
        now = datetime.now(IST) 
        reg_date = str(now.strftime('%Y-%m-%d %H:%M:%S'))
        self.reg_date = reg_date 
         
    
        
    async def sanitize_user_input(self):
        
        cleaner = Cleaner(tags=[], attributes={}, styles=[], protocols=[], strip=True, strip_comments=True, filters=None)
        self.username = (cleaner.clean(self.username))
        self.email = (cleaner.clean(self.email))
        self.password = (cleaner.clean(self.password))
    
    
    
    async def encrypt_user_password(self):
        
        self.password = sha256((self.password).encode('utf-8')).hexdigest()
    
        
    async def check_admin_exist(self,username):
        
        result = self.conn.execute('SELECT * FROM auth_users where email = "{}" or username = "{}" '.format(self.email,self.username))
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
        result = self.conn.execute('SELECT * FROM auth_users where useridkey = "{}"'.format(self.unique_id))    
        record  = len(result.fetchall())
        if(record == 0):
            return self.unique_id
        else:
            generate_useridkey(self)
    


    async def add_new_admin(self):
        try:
            insert_query = "INSERT INTO auth_users VALUES ('','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(self.unique_id,self.name,self.username,self.email,self.cell_num,self.password,self.reg_date,self.last_login,self.auth_access,self.verifcation, self.login_count )
            result = self.conn.execute(insert_query)
            return True 
        except Exception as e:
            print(e)
            return False
        
        
    async def close_database(self):
        self.conn.close()
   
  
if __name__ == "__main__":
   
    
    
    user_one = RegisterAdmin("Naveed","asdfDASDfred","asdads@naveed.com","0313232431324","test","Full Control")
    user_one.add_new_admin()
  