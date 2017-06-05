#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 23:29:43 2017

@author: loan
"""

import encp_manager as manager

class Agent():

    object_counter = 0
    instances = []
    id_counter = 0


#@param location : (x,y)  X height/vertical, Y Horizontal
    def __init__(self, capacity, location, speed, preferences):
        self.capacity = capacity
        self.location = location
        self.speed = speed
        self.preferences = preferences
        self.id = Agent.id_counter
        self.schedule = ""
        Agent.instances.append(self)
        Agent.object_counter += 1
        Agent.id_counter += 1
    


    def __str__(self):
        return "Agent ID: " + str(self.id) + "Location: " + str (self.location) + "Capacity:" +  str(self.capacity) + "Speed: " + str(self.speed) + "Preferences: " + str(self.preferences)
    
    
    #calculate using  |x1-x2| + |y1-y2|
    #Schedule berücksichtigen
    def get_distance_to(self,location):
        dist = abs(self.location[0]-location[0])+ abs(self.location[1]+location[1])
        return dist



    ##edge from step 1 to 2,  should be done?
    def send_pre_bid(self,location, manager):
        bid = self.get_distance_to(location)
                    
        return bid
    
    #edge from step 3 to 5
    def send_def_bid(self):
        return "Todo"

    #edge from step 2 to 4
    def recv_pre_reject(self):
        return "TODO"
    
    #edge from step 2 to 3
    def recv_pre_accept(self):
        return "TODO"
    
    
    #edge from step 5 to 6
    def recv_def_accept(self):
        return "Todo"
    
    #edge from step 4 to 7
    def recv_def_reject(self):
        return "TODO"
    
    def get_id(self):
       return self.id
