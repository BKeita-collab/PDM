#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 22:35:27 2021

@author: brahimakeita
"""

import json 
import requests

def adress_coord(geocoding_url,authentification): 
    """
    This function will convert an input adress in str and will return 
    the coordinates that matches the input adress

    Parameters
    ----------
    geocoding_url : str
        It's the requests send by the user.
        Ex: https://api.openrouteservice.org/geocode/search?api_key=5b3ce3597851110001cf624894bc9991e18844d58c8215f966965e3d&text=5%20avenue%20Anatole%20France,%2075007%20Paris
    
    authentification: str 
        It's the token, it's the authentification key. By default, my values will be use. 
        Ex : 5b3ce3597851110001cf6248a43df362067a4396a8d747bfe12d47c6

    Returns
    -------
    coordinates : list.
    It's the coordinates of the corresponding point of the adress. 
    Ex : [2.592687, 48.840096]

    """
    r = requests.get(geocoding_url, authentification)
    
    if r.status_code == 200:
        # Get returned data of the request
        returned_data = r.text
         # Transform JSON data to Python object
        data = json.loads(returned_data)
        # We Print data with indentation using json module
        #data_dumped = json.dumps(data, indent=4)
        coordinates = data['features'][0]['geometry']['coordinates']

        return coordinates 
    else:
        #print("error: status_code={}".format(r.status_code))
        returned_data = "error: status_code={}".format(r.status_code)
        return returned_data
    
    
    
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    