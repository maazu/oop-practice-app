# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 04:41:52 2020

@author: Acer
"""
from faker import Faker
import re
from hashlib import sha256
import base64 
from bleach.sanitizer import Cleaner
import datetime
from Crypto.Cipher import AES    
from Crypto.Hash import SHA256
from cryptography.fernet import Fernet

def protector_of_the_user(user_id_key,validity):
    
    cleaner = Cleaner(tags=[], attributes={}, styles=[], protocols=[], strip=True, strip_comments=True, filters=None)
    faker = Faker()
    profile1 = faker.simple_profile()
    profile = list(profile1.values())
    profile_string = ''.join(map(str, profile)) 
    ct = datetime.datetime.now() 
    final_token_key = str(re.sub(r"[\n\t\s]*", "", cleaner.clean(profile_string))) +"timestamp" +str(ct.timestamp() )
    
    return final_token_key
 



from cryptography.fernet import Fernet
key = Fernet.generate_key() #this is your "password"
cipher_suite = Fernet(key)
encoded_token = cipher_suite.encrypt(token)
encoded_token2 = cipher_suite.encrypt(token2)
print(encoded_token)
print(encoded_token2)

decoded_token = cipher_suite.decrypt(encoded_token)
decoded_token2 = cipher_suite.decrypt(encoded_token2)

print("\ndecodne\n")
print(decoded_token)
print("\ndecodne22\n")
print(decoded_token2)



def generate_encrypted_token(self,user_id_key):
        
        cleaner = Cleaner(tags=[], attributes={}, styles=[], protocols=[], strip=True, strip_comments=True, filters=None)
        faker = Faker()
        token_key = faker.simple_profile()
        token_key = list(token_key.values())
        token_key_string = ''.join(map(str, token_key)) 
        ct = datetime.datetime.now() 
        final_token = str(re.sub(r"[\n\t\s]*", "", cleaner.clean( token_key_string))) +"timestamp" +str(ct.timestamp() )
        key = Fernet.generate_key() #this is your "password"
        cipher_suite = Fernet(key)
        encoded_token = cipher_suite.encrypt(final_token)
        
        
        return encoded_token