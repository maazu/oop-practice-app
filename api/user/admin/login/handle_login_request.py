# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 05:59:11 2020

@author: Maaz
"""
import asyncio
from login_admin import *
from functools import wraps ##windows rm rerror imports
from asyncio.proactor_events import _ProactorBasePipeTransport ##windows rm rerror imports
            
 
class ReguestLogin:
   
   def __init__(self,username, email, password):
       self.login_request = AdminLogin(username, email, password)
        

   async def handle_login(self):
       """
       Looks for user credentials
       for login purpose 
       Returns
       -------
       TYPE
           login code: str VALID, str INVP, str NUE.
           VALID: user exist
           INVP: invalid password
           NUE: user not exist

       """
       if (await self.login_request.check_admin_exist()):
           if (await self.login_request.match_password()):
               if (await self.login_request.update_login_history()):
                   user_id_key = await self.login_request.retrive_user_id_key()
                   if(user_id_key):
                       await  self.login_request.close_database()
                       return ["VALID",user_id_key]
                   else:
                       return ["nont"]
               else:
                   return ["updatefailure"]  ##INVLID PASSWORD 
           else:
               return ["INVP"] ## NO USER EXIST 
       else:
            return ["NUE"]

         
       
        
   def perform_login_action(self):
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
          task_obj = loop.create_task(self.handle_login())
          login_code = loop.run_until_complete(task_obj)
          return  login_code
         
         
       
"""
if __name__ == "__main__":
    from datetime import datetime 

    start_time = datetime.now() 
    for i in range(0,1):
       
        a = ReguestLogin("asdfDASDfred","asdads@naveed.com","test")
        foo =  a.perform_login_action()
        print(foo)
    time_elapsed = datetime.now() - start_time     
    print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
 """