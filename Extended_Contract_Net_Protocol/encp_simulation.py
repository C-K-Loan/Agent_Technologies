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
from encp_animation import Encp_animation
import encp_manager as manager
import encp_animation as anim

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
            
            print("TASK FOR " + str(self.task.x)+"initiated!")
            manager_t = Encp_manager(self.task.x,agent_list)
            print ("IN SIMULATION")
            manager_t.manage()
            print(" OUT MANAGE")

        else:
            print("Time for Task has not yet come, expected: " + str(self.task.t)+ "time is" + str (time_global))
         #   print ("World time is " + str(time_global) )


def simulate(t,manager_release_time_list):
    global time_global
    time_global = 0
    i = 0
    #every time iteration, tasks get announced and if the time is right, Encp manager will be created
    for time in range(t):
        i = 0
        if (manager_release_time_list[time]!= []):# if list is not empty at position, then there are managers to simulate
            while(confirm_no_more_managers_to_simulate(time) == False):#Only simulate, if managers for that time are unfinished
                   
                print(">>>>>>>>>>>>ITERATION : "+ str(i) + "FOR TIME "+ str(time)+"<<<<<<<<<<<<<")
                #Phase 1STEP 2 collect Pre Bids
                print("PHASE1:>>>>>>>>>>>>COLLECTING PRE BIDS STEP 2<<<<<<<<<<<<<")     
                for manager_sim in manager_release_time_list[time]:#simulate evermanger for time 
                    print(">>>>>>>>>>>MANAGER ID :"+ str(manager_sim.id)+"TURN<<<<<<<<<<")
                    if manager_sim.finished == False and manager_sim.phase == 1: # ALPHA IF
                        manager_sim.get_pre_bids()

                print("PHASE1:>>>>>>>>>>>>EVALUATING BIDS....<<<<<<<<<<<<<")
                #Phase1#STEP 3 And 4 Evaluate Pre Bids and send Responses to Agents, Agents will react with DEF bids
                for manager_sim in manager_release_time_list[time]:#simulate evermanger for time 
                    print(">>>>>>>>>>>MANAGER ID :"+ str(manager_sim.id)+"TURN<<<<<<<<<<")
                    if manager_sim.finished == False and manager_sim.phase == 1: # ALPHA IF
                        manager_sim.find_and_set_best_bidder()                        
                
                print("PHASE1:>>>>>>>>>>>>SENDING PRE REJECTS <<<<<<<<<<<<<")
                #Phase1#STEP 3 And 4 Evaluate Pre Bids and send Responses to Agents, Agents will react with DEF bids
                for manager_sim in manager_release_time_list[time]:#simulate evermanger for time 
                    print(">>>>>>>>>>>MANAGER ID :"+ str(manager_sim.id)+"TURN<<<<<<<<<<")
                    if manager_sim.finished == False and manager_sim.phase == 1: # ALPHA IF
                        manager_sim.send_pre_rejects()#after this, everyone who is rejected whill send a new pre_bid, if they can imrpove



                print("PHASE1:>>>>>>>>>>>>SENDING PRE   ACCEPTS<<<<<<<<<<<<<")
                #Phase1#STEP 3 And 4 Evaluate Pre Bids and send Responses to Agents, Agents will react with DEF bids
                for manager_sim in manager_release_time_list[time]:#simulate evermanger for time 
                    print(">>>>>>>>>>>MANAGER ID :"+ str(manager_sim.id)+"TURN<<<<<<<<<<")
                    if manager_sim.finished == False and manager_sim.phase == 1: # ALPHA IF
                        manager_sim.send_pre_accepts()#after this, def bid is send automatically

         #wait 1 s for agents to answer 

                print(">>>>>>>>>>>>SETTING PHASES<<<<<<<<<<<<<")
                #update phase status, check if there is a neew best bidder, if yes -> phase 1, if best bidder didint change ->phase 2 (sending DEF Rej/Acc)
                for manager_sim in manager_release_time_list[time]:
                    print(">>>>>>>>>>>MANAGER ID :"+ str(manager_sim.id)+"TURN<<<<<<<<<<")
                    if manager_sim.finished == False:
                        manager_sim.set_phase()
                
               # animation.update_bids()#RENDERING
              #  animation.mainloop()

                print("PHASE2:>>>>>>>>>>>>SENDING DEF   REJECTS<<<<<<<<<<<<<")                    
                #Phase 2 STEP 3 Agents havesend Def bids by now, if best_bidder didint changed manager sends def Accepts and Def Rejects 
                for manager_sim in manager_release_time_list[time]:#simulate evermanger for time 
                    print(">>>>>>>>>>>MANAGER ID :"+ str(manager_sim.id)+"TURN<<<<<<<<<<")
                    if manager_sim.finished == False and manager_sim.phase == 2: # ALPHA IF
                        manager_sim.send_def_reject()

                print("PHASE2:>>>>>>>>>>>>SENDING DEF ACCEPTS  <<<<<<<<<<<<<")                    
                #Phase 2 STEP 3 Agents havesend Def bids by now, if best_bidder didint changed manager sends def Accepts and Def Rejects 
                for manager_sim in manager_release_time_list[time]:#simulate evermanger for time 
                    print(">>>>>>>>>>>MANAGER ID :"+ str(manager_sim.id)+"TURN<<<<<<<<<<")
                    if manager_sim.finished == False and manager_sim.phase == 2: # ALPHA IF
                        manager_sim.send_def_accept()

                i+=1 
                input("press enter")    
        
        
        time_global += 1

                
    



#confirm if there are managers to simulate for time t
#return FALSE,if there are unfinished managers for time T
#return TRUE, if every manager for time T  is finished (def acc/rej send)
def confirm_no_more_managers_to_simulate(time):
    result = True
    for manager in manager_release_time_list[time]:
        if manager.finished == False:
            result = False
    return result
        
    


#bulding agent: 
#id, location, capacity ,speed, preferences[]


test_agent0= Agent((0,1),5,1,(0,1))#he manager likes 0 >1
#test_agent1= Agent(5,(3,3),15,20, [0])
test_agent2= Agent((4,1),5,1,(0,1))# he manager likes 0>1
#test_agent4= Agent(5,(6,6),15,20, [0]) 

agent_list=[test_agent0,test_agent2]
print ("PRE MANAGER CONSTRUCT")
#manager_t= Encp_manager((5,5),agent_list)


manager1=Encp_manager((2,3),agent_list)
manager2=Encp_manager((0,1),agent_list)
#A list, whoose elements are Lists of Managers 
#list [0] is a list of managers, who should be initated for Time 0
#list [n] is list of managers, who should be initated at time N
manager_release_time_list= []
manager_release_time_list.insert(0,[])
manager_release_time_list.insert(1,[])
manager_release_time_list.insert(2,[])
manager_release_time_list.insert(3,[])
manager_release_time_list.insert(4,[])#Encp_manager((3,0),agent_list)
manager_release_time_list.insert(5,[manager1,manager2])
manager_release_time_list.insert(6,[])
manager_release_time_list.insert(7,[])
manager_release_time_list.insert(8,[])
manager_release_time_list.insert(9,[])
manager_release_time_list.insert(10,[])
manager_release_time_list.insert(11,[])

animation = Encp_animation()

#print ("relase time lsit :" + str(manager_release_time_list))
simulate(10,manager_release_time_list)


#task1= Task(5,(0,4))#should be won my agent 1

#task2= Task(5,(3,0))#should be won by agent 2 
#task3= Task(4,(7,7))#should be won by ag3
#test_agent= agent.Agent(5,(0,0),15,20, [0])
#initiator1 = Initiator(task1)
#initiator2 = Initiator(task2)
#initiator3 = Initiator(task3)

#init_world(5,5)

#test_manager.recv_pre_bids()
