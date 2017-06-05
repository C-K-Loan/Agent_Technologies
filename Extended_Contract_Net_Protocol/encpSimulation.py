# -*- coding: utf-8 -*-
"""
Created on Thu May 25 23:29:11 2017

@author: Komat
"""
import numpy as np
import math
import networkx as nx
import encp_agent as agent
import encp_manager as manager

width = 5
height = 5
global time_Global


#@ Param Agents List of Tupels with Agent Parameters 
#@ Param width, height world size
#@ aram
def init_world( width, height, agents):
    global world
    #create gridworld
    world = nx.grid_2d_graph( width, height)

    #create Agents from Agents List
    for i in range (agents):
        Agent(agents[i])


             
class task():
    
    object_counter = 0
    instances = []
    id_counter = 0
    #create a job 
    #@param Task Location, where is the task
    #@param time, WHEN the task is released/created
    def __init__(self, task_location, time):
        self.task_location = task_location
        self.time = time
        self.id = task.id_counter
        task.id_counter +=1
        self.done = False 
        return " TODO" 

        
class initiator():
    
    object_counter = 0
    instances = []
    id_counter = 0
    phase = 1

    def __init__(self, task):
        self.time = time
        self.id = initiator.id_counter
        initiator.id_counter +=1        
        self.task = task
        return " TODO"

    #announce Task , Create ENCP instance for that task
    def announce_task(self):
        if self.task.time == time_global: #only Release Task when world is at that time
            manager = encp_manager(self.task.task_location)#initiate encp instance            
            manager.manage()# maybe remove this and let everything be handelt in __init__ encp
            return "kinda implemented on Manage side"
        else:
            print("Time for Task has not yet come, expected: " + self.task.time)
        
def simulate(t, n=0):
    time_global=0
    print("______________________________________________")
    for t in range(t):
        time_global += 1
        #simulate world TODO
        
        
test_agent= agent.Agent(5,(0,0),15,20)
print(test_agent.get_distance_to((10,10)))

test_manager = manager.encp_manager(1)
#test_manager.recv_pre_bids()