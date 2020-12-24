# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 05:59:11 2020

@author: Maaz
"""
from create_admin import *
from functools import wraps ##windows rm rerror imports
from asyncio.proactor_events import _ProactorBasePipeTransport ##windows rm rerror imports
            
 
class HandleRegRequest:
   
   def __init__(self, name, username, email, cell_num, password,auth_access):
       
       self.registration_request = CreateAdmin( name, username, email, cell_num, password,auth_access)
        

   async def handle_reg_request(self):
       """
       Handles the user new user admin request
       Returns
       -------
       TYPE
           login code: str VALID, str INVP, str NUE.
           VALID: user exist
           INVP: invalid password
           NUE: user not exist

       """
       if (await self.registration_request.check_admin_exist() == False):
           
           if (await self.registration_request.add_new_admin() == True ):
               await self.registration_request.close_database()
               return "SuccesAdmin!"
           else:
               return "Error occured!"
           
       else:
            return "UAE"
           
              
        
   def perform_registration_process(self):
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
          task_obj = loop.create_task(self.handle_reg_request())
          registration_code = loop.run_until_complete(task_obj)
          return registration_code
         
         
       
  
if __name__ == "__main__":
    from datetime import datetime 

    start_time = datetime.now() 
    for i in range(0,1):
       
          user_one = HandleRegRequest("Naveed","test12","asdads@test.com","0313232431324","teasdasst","Full Control")
         
          foo =  user_one.perform_registration_process()
          print(foo)
    time_elapsed = datetime.now() - start_time     
    print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))
    
    
    
    
    
    
    
    
"""
if __name__ == "__main__":
   
    
    
    user_one = RegisterAdmin("Naveed","asdfDASDfred","asdads@naveed.com","0313232431324","test","Full Control")
    user_one.add_new_admin()
  
    
"""