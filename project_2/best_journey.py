#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 22:27:14 2021

@author: brahimakeita
"""

import requests
import json

def best_journey(post_url, start,end,authentification,name, json_file=True): 
    """
    This function will compute the best direction from start to end

    Parameters
    ----------
    start : tuple 
        It's the starting point.
        Ex: (2.36309,48.86703)
    
    end : tuple 
        It's the destination point.
        Ex: (2.32738,48.86381)
    name : str 
        It's the name of the person making the research'
        Ex : Brahima
    authentification: str 
        It's the token, it's the authentification key. By default, my values will be use. 
        Ex : 5b3ce3597851110001cf6248a43df362067a4396a8d747bfe12d47c6

    Returns
    -------
    distance : float.
        It's the distance in meter(m) return in meter. 
        Ex : 2592687
    duration : float.
        It's the time in seconde(s) spent to go from starting point to the destination point. 
        Ex : 25 
        

    """
    header_dict = {
    "Authorization" : str(authentification)
    }
    
    body = {"coordinates":[[start[0],start[1]],[end[0],end[1]]]}

    r = requests.post(post_url,headers = header_dict, json = body)

    if r.status_code == 200:
        # Get returned data of the request
        returned_data = r.text
        # Transform JSON data to Python object
        data = json.loads(returned_data)
        # We Print data with indentation using json module
       
        # distance = data['routes'][0]['summary']['distance']
        # duration = data['routes'][0]['summary']['duration']
        # data_dumped = json.dumps(data, indent=4)

        
        if json_file == True:
            
            output_file = 'journey/journey_'+ name + '.json'
            with open(output_file, 'w') as outfile:
                data_dumped = json.dump(data, outfile, indent=4)
            return data_dumped
        
        else : 
            print('#####')
            distance = data['routes'][0]['summary']['distance']
            duration = data['routes'][0]['summary']['duration']
            return  distance , duration 
    else:
        #print("error: status_code={}".format(r.status_code))
        returned_data = "error: status_code={}".format(r.status_code)
        return returned_data
    
    
    
    
    
    