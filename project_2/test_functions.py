#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 19:49:23 2021

@author: brahimakeita
"""

def location(adress):
    """
    This function will convert an input adress in str and will return 
    the coordinates that matches the input adress

    Parameters
    ----------
    adress : str
        It's the input adress by the user.
        Ex: 15 avenue Blaise Pascal, Champs-sur-Marne

    Returns
    -------
    JSON file.
    It's all the adresses that matches the user's input adress. 
    Accurated is the adresses, accurate will be the returned adress

    """


post_url = 'https://api.openrouteservice.org/v2/' + 'directions/' + 'foot-walking/' + 'json'

def best_journey(post_url, start,end,authentification = my_token ): 
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
    body = {"coordinates":[[start[0],start[1]],[end[0],end[1]]]}

    r = request.post(url, data={key: authentification }, json=body)

    if r.status_code == 200:
        # Get returned data of the request
        returned_data = r.text
        # Transform JSON data to Python object
        data = json.loads(returned_data)
        # We Print data with indentation using json module
        #data_dumped = json.dumps(data, indent=4)
        distance = data['routes'][0]['summary']['distance']
        duration = data['routes'][0]['summary']['duration']
        return distance , duration 
    else:
        #print("error: status_code={}".format(r.status_code))
        returned_data = "error: status_code={}".format(r.status_code)
        return returned_data


a = best_journey(start = (2.36309,48.86703) , end =  (2.32738,48.86381))
a