# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:52:26 2020

@author: Acer
"""
from hashlib import sha256

class RegisterAdmin:

    def __init__(self, name, username, email,cell_num, password):
        self.name = name
        self.username = username
        self.email = email
        self.cell_num = cell_num
        self.password = sha256((password).encode('utf-8')).hexdigest()
        self.check_user_exist()
    
   
    def check_user_exist(self):
        user_name = self.username
   
    def check_user_exist(self):
        user_name = self.username
        
       
    
  
    
  
    
  
if __name__ == "__main__":
    user_one = RegisterAdmin("Naveed","naveed123","test@naveed.com","03132324324","test" )
