# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 19:27:38 2020

@author: Acer
"""
import os
import sys
import datetime
import random


timestamp = datetime.datetime.now().isoformat()
error_id_list = []

error_logs = {}


def generate_random_error_id():
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    error_id_list = ''
    for i in range(0, 11):
        error_id_list += random.choice(characters)
        
    error_tracking_id = str(timestamp)+"-"+str(error_id_list)
    return error_tracking_id


def add_error_log(reason,error):
    error_id =  generate_random_error_id()
    error_logs[error_id] = [reason,error,"RAISED"]
    
    
