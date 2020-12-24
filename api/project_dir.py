# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 23:47:58 2020

@author: Acer
"""
import os 
import sys 


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
if(BASE_DIR + '/applog/' not in sys.path):
    sys.path.insert(0, BASE_DIR + '/applog/')
    sys.path.insert(0, BASE_DIR +'/api/auth/')
    sys.path.insert(0, BASE_DIR + '/api/config/')
    sys.path.insert(0, BASE_DIR + '/api/')

