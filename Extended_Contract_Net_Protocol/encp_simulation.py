# -*- coding: utf-8 -*-
"""
Created on Thu May 25 23:29:11 2017

@author: Komat
"""
import numpy as np
import math
import networkx as nx
import encp_agent as agent
from encp_agent import Agent
from encp_manager import Encp_manager

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

    instances = []
    id_counter = 0
    #create a job
    #@param t = time, WHEN the task is released/created
    #@param x = Location, where is the task

    def __init__(self, t, x):
        self.t = t
        self.x = x
        self.id = Task.id_counter
        Task.id_counter +=1
        #Status
        self.done = False
         


# vergibt tasks
#an initiator, will initiate the encp Manager instance, of A location with announce_task(), when time is right        
class Initiator():

    instances = []
    id_counter = 0
    phase = 1

    def __init__(self, task):
        self.id = Initiator.id_counter
        self.task = task
        Initiator.id_counter +=1
        Initiator.instances.append(self)

    #announce Task , Create ENCP instance for that task
    def announce_task(self):
        if self.task.t == time_global: #only Release Task when world is at that time
            manager_t = manager.Encp_manager(self.task.x)#initiate encp instance
            

           # manager_t.print_smth("smth")
            manager_t.manage(manager_t)

            
            print("TASK FOR " + str(self.task.x)+"initiated!")
        else:
            print("Time for Task has not yet come, expected: " + str(self.task.t))
         #   print ("World time is " + str(time_global) )


def simulate(t, n=0):
    global time_global
    time_global = 0
    #every time iteration, tasks get announced and if the time is right, Encp manager will be created
    for t in range(t):
        for initiator in Initiator.instances:
            initiator.announce_task()
        time_global += 1
                
    

#bulding agent: 
#id, location, capacity ,speed, preferences[]


test_agent1= Agent(5,(0,0),15,20, [0])
test_agent2= Agent(5,(3,3),15,20, [0])
test_agent3= Agent(5,(1,1),15,20, [0])
test_agent4= Agent(5,(4,4),15,20, [0])

agent_list=[test_agent1,test_agent2,test_agent3,test_agent4]
print ("PRE MANAGER CONSTRUCT")
manager_t= Encp_manager((5,5),agent_list)

print ("IN SIMULATION")
manager_t.manage()
print(" OUT MANAGE")



#task1= Task(3,3)
#test_agent= agent.Agent(5,(0,0),15,20, [0])
#initiator = Initiator(task1)

#init_world(5,5)
#simulate(10)

#test_manager.recv_pre_bids()
