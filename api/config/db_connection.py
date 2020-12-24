# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 18:20:08 2020

@author: Acer
"""
import os
import sys
from app_error_log import *
import sqlalchemy as sql
import asyncio
import nest_asyncio

class Database:  
    
    
    def __init__(self):
        
       self.db_user = "root"
       self.db_pass = ""
       self.db_host = "localhost"
       self.db_port = "3306"
       self.db_name = "akberi_internal"  ###dumy database
       
       
    def initialise_db_connection(self):
        
        try:
            url =  ('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(self.db_user, self.db_pass,self.db_host, self.db_port, self.db_name))
            engine = sql.create_engine(url)
            connection = engine.connect()
            return connection
            
        except Exception as e:
            print(e)
            add_error_log("database error connection",str(e))



























'''
    def create_database(self):
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
          
          
          loop = asyncio.get_event_loop() 
          task_obj = loop.create_task(self.initialise_db_connection())
          database_connection = loop.run_until_complete(task_obj)
          return database_connection
'''




