#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 23:30:59 2017

@author: loan
"""

import numpy as np
import math
import encp_agent as agent
from encp_agent import Agent
class Encp_manager():

    instances = []
    id_counter = 0
    

    #@param agents, a list of all created agents in the world    
    #@param location, which location will be managed by this manager
    def __init__(self, location, agents):
        print ("HI")
        print("Agent for Location"+ str(location) + " initiated")
        self.best_bid = [math.inf,None ]#best_bid(0) is value of Best bid, best_bid(1) is that corrosponding bidding Agent
        self.bids = {}# Dictionary for Key:Agent Value:Tuple (BID,ID of agent)
        self.x = location#which field does the ENCP manager manage
        self.phase = 1#inital phase 1 of 2 
        self.id = Encp_manager.id_counter
        self.phase = 1
        #self.pre_bid_rounds = 0
        #self.agent_L = agents
        Encp_manager.instances.append(self)
        Encp_manager.id_counter += 1


    def manage(self):
    #function that manages ai/acting of manager
    #inital call of this method, to start manager 
    #once Task is managed, encp_manager instance will terminate through this method, free ressources?
   #    for rounds in self.pre_bid_rounds#repeat for N pre bidding rounds
        self.get_pre_bids()#collect al inital pre bids
        print("______________DONE WITH FIRST COLLECTION OF BIDS______")

        self.send_pre_rejects()#send reject to every agent, who is not best_bid[0]
        print("______________DONE WITH SENDING FIRST WAVE OF PRE REJECTS______")

        self.send_pre_accept()#send pre accet to agent, who is best_bid[0]    
        print("______________DONE WITH FIRST PRE ACCEPT______")
        
    # self.phase=2#def
        

    #TO TEST
    #edge from 1 to 2, collect all pre bids
    #ask all agents for their bids
    def get_pre_bids(self):
        print("Collecting bids...")
        for agent_it in Agent.instances: #ANNOUNCE TASK/Inform Every Agent and get Pre Bid (1) Task Announcement and (2) Recieving end of Pre Bid
            self.bids[agent_it] = (agent_it.send_pre_bid(self), agent_it.id)#aka Call for proposals(cfp),Use Agent as Key and Bid as Value
            print("Recieved bid :" + str(self.bids[agent_it][0]) + "from Agent ID:"+ str(self.bids[agent_it][1]))
            
        for agent_it in Agent.instances:#find best bidder, send him Pre Accept, Pre Reject to the rest
            if(float(self.best_bid[0])> float(self.bids[agent_it][0])):
                self.best_bid[0] = str(self.bids[agent_it][0])#actual value of the bid
                self.best_bid[1] = str(self.bids[agent_it][0]) # id of the bidder
            else : 1+1
        print("best Bid is:"+ str(self.best_bid[0] )+"with id :"+str(self.best_bid[1]))
        
        
    #Inteface for agents, so they can bid
    #Should only be called by agent, if they can actually offer a better bid
    def recv_pre_bid(self,agent_sender,bid):
        print("recieved Improved? pre bid from ID:" +str(agent_sender.id)+ "value:" + str(bid)+"old best bid was"+str(self.best_bid[0]))
        if(int(self.best_bid[0])< int(bid)):
            self.send_pre_reject_to_best_bidder()
            self.best_bid[0]= bid
            self.best_bid[1]= agent_sender.id
            print("New best bidder, sending pre Accept to him and pre rej to old best bidder")
            agent_sender.recv_pre_accept(self)
        else:
            agent_sender.recv_def_reject()
            



    #send a pre reject to current best bidder
    def send_pre_reject_to_best_bidder(self):
        for agent_it in Agent.instances:
            if int(agent_it.id) == int(self.best_bid[1]):
                agent_it.recv_pre_reject(self)
    #edge from step 2 to 4 
    #Send pre reject to every agent, who is not best bidder
    def send_pre_rejects(self):
        for agent_it in Agent.instances:
            if(int(agent_it.id) !=int(self.best_bid[1])):
                print("sending pre reject to agent ID : "+ str(agent_it.id) )
                agent_it.recv_pre_reject(self)

    #edge from 2 to 4 
    #send pre accept to best bidder
    def send_pre_accept(self):
        for agent_it in Agent.instances:
            if(int(agent_it.id) ==int(self.best_bid[1])):
                print("sending pre Acc to agent ID : "+ str(agent_it.id) )
                agent_it.recv_pre_accept(self)
 
    
    
    
    #Edge from 3 to 5| @ param agent, agent that sends the def bid
    #this will recieve best_bid and then ask all agents for 
    def recv_def_bid(self,agent_sender,def_bid):
        print("Manager recieved def_bid!, Val:"+str(def_bid)+"from agent ID: " + str(agent_sender.id))
        if int(self.best_bid[0])<= def_bid:
            self.best_bid[0] = def_bid
        
    
    #edge from 5 to 6 -> END OF protocoll
    def send_def_accept(self):
        return "todo"    
    #edge from 5 to 7 -> END of protocoll
    def send_def_reject(self):
        return"todo"

#agent.Agent()
test_agent1= Agent(5,(0,0),15,20, [0])
test_agent2= Agent(5,(3,3),15,20, [0])
test_agent3= Agent(5,(1,1),15,20, [0])
test_agent4= Agent(5,(4,4),15,20, [0])

#for agent_x in Agent.instances: print (agent_x)
agent_list=[test_agent1,test_agent2,test_agent3,test_agent4]
manager_t= Encp_manager((2,2),agent_list)
#manager_t.recv_pre_bids()
manager_t.manage()
#print(test_agent1.get_distance_to((5,5)))
