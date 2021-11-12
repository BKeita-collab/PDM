#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 00:39:03 2021

@author: brahimakeita
"""

# def best_journey(post_url, start,end,authentification, json_file=True):
def best_journeys(student,authentification): 
    """
    This function will compute the best direction from start to end

    Parameters
    ----------
    student: pandas dataframe
        It's the dataframe of all information for each student.
        Ex: column:	id,student_address,school_name,student_latitude,	student_longitude
    
    
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
    
    
    
    