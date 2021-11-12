#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 09:25:12 2021

@author: brahimakeita
"""

### Module imports
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from sqlalchemy import create_engine

## import of the 2 functions geocoding: adress_coord and best journey: best_journey
from location import adress_coord
from locations import pd_adress_coord
from best_journey import best_journey

students_list = pd.read_csv('students.csv')
schools_list = pd.read_csv('schools.csv')

### Geocoding URL 
url_geocoding = 'https://api.openrouteservice.org/geocode/search?api_key=5b3ce3597851110001cf624894bc9991e18844d58c8215f966965e3d&text=5 avenue Anatole France, 75007 Paris'


## Header Dictionnary 
header_dict = {
    "Authorization" : '5b3ce3597851110001cf6248a43df362067a4396a8d747bfe12d47c6'
}

## best_journey URL 
post_url = 'https://api.openrouteservice.org/v2/' + 'directions/' + 'foot-walking/' + 'json'

## Test requests 

## geocoding 
test_1 = adress_coord(url_geocoding, header_dict["Authorization"] )

## best journey 
a = best_journey(post_url,(2.36309,48.86703),(2.32738,48.86381),header_dict["Authorization"], 'name')

