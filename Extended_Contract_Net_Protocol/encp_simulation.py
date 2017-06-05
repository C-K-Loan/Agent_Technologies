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

w = 5
h = 5
global time_global


#@ Param Agents List of Tupels with Agent Parameters 
#@ Param width, height world size
#@ aram
def init_world( width = w, height= h):
    global world
    #create gridworld
    world = nx.grid_2d_graph( width, height)

    #create Agents from Agents List
    #for i in range (agents):
     #   Agent(agents[i])

            
class Task():
#represents a task/job, for location and time(whic his announce time)     

    object_counter = 0
    instances = []
    id_counter = 0
    #create a job 
    #@param Task Location, where is the task
    #@param time, WHEN the task is released/created
    def __init__(self, task_location, time):
        self.task_location = task_location
        self.time = time
        self.id = Task.id_counter
        Task.id_counter +=1
        self.done = False
         



#an initiator, will initiate the encp Manager instance, of A location with announce_task(), when time is right        
class Initiator():
    
    object_counter = 0
    instances = []
    id_counter = 0
    phase = 1

    def __init__(self, task):
        self.id = Initiator.id_counter
        Initiator.id_counter +=1        
        self.task = task
        Initiator.instances.append(self)

    #announce Task , Create ENCP instance for that task
    def announce_task(self):
        if self.task.time == time_global: #only Release Task when world is at that time
            manager_t = manager.Encp_manager(self.task.task_location)#initiate encp instance            
            #manager_t.manage()
            manager_t.recv_def_bids()
            
            print("TASK FOR " + str(self.task.task_location)+"initiated!")
        else:
            print("Time for Task has not yet come, expected: " + str(self.task.time))
         #   print ("World time is " + str(time_global) )
def simulate(t, n=0):
    global time_global
    time_global = 0
#every time iteration, tasks get announced and if the time is right, Encp manager will be created
    for t in range(t):
        time_global += 1
        for initiator in Initiator.instances: 
            initiator.announce_task()   
                
    
    #if time should start at 1, put this at beginning of for loop

        #simulate world TODO
        
        
#bulding agent: 
#capacity, location, speed, pref
test_agent= agent.Agent(5,(0,0),15,20)


task1= Task(3,3)
initiator = Initiator(task1)

init_world(5,5)
simulate(10)

#test_manager.recv_pre_bids()
