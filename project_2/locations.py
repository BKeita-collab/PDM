#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 00:06:21 2021

@author: brahimakeita
"""

from location import adress_coord
import pandas as pd

def pd_adress_coord(geocoding_adresses,authentification,output_file):  
    
    """
    This function will convert an input adress in str and will return 
    the coordinates that matches the input adress

    Parameters
    ----------
    geocoding_adresses : panda dataframe 
        They are all the adresses in str format in each row of the dataframe.
        Ex:each line look line '15 avenue Blaise Pascal, 77420'
    
    authentification: str 
        It's the token, it's the authentification key. By default, my values will be use. 
        Ex : 5b3ce3597851110001cf6248a43df362067a4396a8d747bfe12d47c6

    Returns
    -------
    coordinates : csv file 
    It's the CSV of all the element inside geocoding. 
    

    """
    #url_geocoding = 'https://api.openrouteservice.org/geocode/search?api_key=5b3ce3597851110001cf624894bc9991e18844d58c8215f966965e3d&text=5 avenue Anatole France, 75007 Paris'
    
    geocoding_dict = {geocoding_adresses.head(0).columns[0] : [], 
                    geocoding_adresses.head(0).columns[1] : [],
                    'latitude': [],
                    'longitude':[]
                    }
    list_keys = list(geocoding_dict.keys())
    
    for i in range (geocoding_adresses.shape[0]):
        
        geocoding_url = 'https://api.openrouteservice.org/geocode/search?api_key='+ authentification+'&text='+geocoding_adresses.loc[i][1]
        
        coord = adress_coord(geocoding_url,authentification)
        
        geocoding_dict[list_keys[0]].append(geocoding_adresses.loc[i][0])
        geocoding_dict[list_keys[1]].append(geocoding_adresses.loc[i][1])
        geocoding_dict['latitude'].append(coord[0])
        geocoding_dict['longitude'].append(coord[1])
    
    
    geocoding_dict_df = pd.DataFrame(geocoding_dict)
    
    #geocoding_dict_csv = pd.to_csv(geocoding_dict_df, index = False)
    output_file = output_file+'.csv'
    return geocoding_dict_df.to_csv(output_file, index = False)








