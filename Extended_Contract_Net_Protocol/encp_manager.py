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
        self.best_bid = [math.inf,None ]#best_bid(0) is value of Best bid, best_bid(1) is that corrosponding bidding Agent
        self.bids = {}# Dictionary for Key:Agent Value:Tuple (BID,ID of agent)
        self.x = location#which field does the ENCP manager manage
        self.phase = 1#inital phase 1 of 2 
        self.id = Encp_manager.id_counter
        self.phase = 1
        self.finished = False
        #self.pre_bid_rounds = 0
        #self.agent_L = agents
        Encp_manager.instances.append(self)
        Encp_manager.id_counter += 1
        self.best_bid_changed= False #inital 0 for first enter in loop, if  this is >0, it means we have a imrpoved bidder



    def manage(self):
    #function that manages ai/acting of manager
    #inital call of this method, to start manager 
    #once Task is managed, encp_manager instance will terminate through this method, free ressources?
   #    for rounds in self.pre_bid_rounds#repeat for N pre bidding rounds
        print("MANAGER WITH ID : >>>>>>>>>>>>"+str(self.id)+"<<<<<<STARTING!!!")            
        self.get_pre_bids()#collect al inital pre bids
        print("M-"+str(self.id)+"P1_____________DONE WITH FIRST COLLECTION OF BIDS______")
        
        self.send_pre_accepts()#send pre accet to agent, who is best_bid[0]    
        print("M-"+str(self.id)+"P1_____________DONE WITH FIRST PRE ACCEPT________________________")#if best_bider changed, go to beginning of p1.2

        self.send_pre_rejects()#send reject to every agent, who is not best_bid[0], they will answer withnwe bids, if bid is not better than best_bid[0]-> send defenitive bid()
        print("M-"+str(self.id)+"P1.3_____________DONE WITH SENDING FIRST WAVE OF PRE REJECTS______")

        if self.best_bid_changed == True :
           self.reset_phase1()
        else: 1+1
        print("P2 _____NOBODY IMPROVED, STARTING PHASE 2____________")
        self.send_def_reject()
        print("M-"+str(self.id)+"_____DONE WITH SENDING DEF REJECTS!_____")
        self.send_def_accept()
        print("M-"+str(self.id)+"_____DONE WITH SENDING DEF ACCEPTS!_____")
        


        
    #todo, not really implemented
    def reset_phase1(self):
        print("________RESETTING PHASE 1_________")
        self.send_pre_accepts()#send pre accet to agent, who is best_bid[0]    
        print("P1_____________DONE WITH FIRST PRE ACCEPT________________________")#if best_bider changed, go to beginning of p1.2

        self.send_pre_rejects()#send reject to every agent, who is not best_bid[0], they will answer withnwe bids, if bid is not better than best_bid[0]-> send defenitive bid()
        print("P1.3_____________DONE WITH SENDING FIRST WAVE OF PRE REJECTS______")
        if self.best_bid_changed == True :
           self.reset_phase1()#rekursiv weiter aufrufen, bis es keine verbesserung gibt
        #PASTE REST OF MANAGE FUNCTION IN RESET
    
    #edge from 1 to 2, collect all pre bids, ask all agents for their bids
    #set bestbidder with function call

    def set_phase(self):

        if self.best_bid_changed == True:
            print ("M-ID:"+str(self.id)+  "SETTING PHASE BACK TO 1 ")
            self.phase = 1
        else :
            print("M-ID:"+str(self.id)+"SETTING PHASE TO 2")
            self.phase = 2
    


    def get_pre_bids(self):
        print("M-ID:"+str(self.id)+"Collecting bids...")
        for agent_it in Agent.instances: #ANNOUNCE TASK/Inform Every Agent and get Pre Bid (1) Task Announcement and (2) Recieving end of Pre Bid
            self.bids[agent_it] = (agent_it.send_pre_bid(self), agent_it.id)#aka Call for proposals(cfp),Use Agent as Key and Bid as Value
            print("M-ID: "+str(self.id)+"Recieved bid :" + str(self.bids[agent_it][0]) + "from Agent ID:"+ str(self.bids[agent_it][1]))
            
        self.find_and_set_best_bidder()
        
    #set the best bidder variable 
    def find_and_set_best_bidder(self):
        for agent_it in Agent.instances:#find best bidder, send him Pre Accept, Pre Reject to the rest
            
            if(float(self.best_bid[0])> float(self.bids[agent_it][0])):
                self.best_bid[0] = str(self.bids[agent_it][0])#actual value of the bid
                self.best_bid[1] = str(self.bids[agent_it][1]) # id of the bidder
            else : 1+1
        print("M-ID :"+str(self.id)+"best Bid is:"+ str(self.best_bid[0] )+"with id :"+str(self.best_bid[1]))
            
        
    #Inteface for agents, so they can bid, Should only be called by agent, if they can actually offer a better bid
    def recv_pre_bid(self,agent_sender,bid):
        print("M-ID :"+str(self.id)+ "  recv pre bid from ID:" +str(agent_sender.id)+ "value:" + str(bid)+"old best bid was"+str(self.best_bid[0]))
        if(int(self.best_bid[0])> int(bid)):
            print("New best bidder, sending pre Accept to him and pre rej to old best bidder old was" +str(int(self.best_bid[0]))+ "new is" + str(int(bid)))            
            self.send_pre_reject_to_best_bidder()
            self.best_bid[0]= bid
            self.best_bid[1]= agent_sender.id
            agent_sender.recv_pre_accept(self)
            self.best_bid_changed= True
        else:

            print("Bidder did not improve,do nothing or def reject?or maybe safe? old was" +str(int(self.best_bid[0])) +"new is" + str(int(bid)))
            agent_sender.recv_def_reject(self)
            self.best_bid_changed= False
            



    #send a pre reject to current best bidder
    def send_pre_reject_to_best_bidder(self):
        for agent_it in Agent.instances:
            if int(agent_it.id) == int(self.best_bid[1]):
                agent_it.recv_pre_reject(self)
                
    #edge from step 2 to 4 , Send pre reject to every agent, who is not best bidder
    def send_pre_rejects(self):
        for agent_it in Agent.instances:
            if(int(agent_it.id) !=int(self.best_bid[1])):
                print("M-ID: "+str(self.id)+"sending pre reject to agent ID : "+ str(agent_it.id) )
                agent_it.recv_pre_reject(self)

    #edge from 2 to 4 
    #send pre accept to best bidder
    def send_pre_accepts(self):
        for agent_it in Agent.instances:
            if(int(agent_it.id) ==int(self.best_bid[1])):
                print("M-ID: "+str(self.id)+"sending pre Acc to agent ID : "+ str(agent_it.id) )
                agent_it.recv_pre_accept(self)
 
    
    
    
    #Edge from 3 to 5| @ param agent, agent that sends the def bid, this will recieve best_bid and then ask all agents for 
    def recv_def_bid(self,agent_sender,def_bid):
        print("M-ID: "+str(self.id)+"recieved def_bid!, Val:"+str(def_bid)+"from agent ID: " + str(agent_sender.id))
        if int(self.best_bid[0])<= def_bid:
            self.best_bid[0] = def_bid
        
    
    #edge from 5 to 6 -> END OF protocoll, manager stops managing after this
    def send_def_accept(self):
        for agent_it in Agent.instances:
            if(int(agent_it.id) == int(self.best_bid[1])):
                print("M-ID: "+str(self.id)+"sending DEF ACCEPT to agent ID : "+ str(agent_it.id) )
                agent_it.recv_def_accept(self)
        self.finished= True# this agent will stop working

    #edge from 5 to 7 -> END of protocoll
    def send_def_reject(self):
        for agent_it in Agent.instances:
            if(int(agent_it.id) ==int(self.best_bid[1])):
                print("M-ID: "+str(self.id)+"sending def Acc to agent ID : "+ str(agent_it.id) )
                agent_it.recv_def_accept(self)
 
"""
test_agent1= Agent(5,(0,0),15,20, [0])
test_agent2= Agent(5,(3,3),15,20, [0])
test_agent3= Agent(5,(1,1),15,20, [0])
test_agent4= Agent(5,(4,4),15,20, [0])

agent_list=[test_agent1,test_agent2,test_agent3,test_agent4]
manager_t= Encp_manager((5,5),agent_list)
#manager_t.recv_pre_bids()
manager_t.manage()
#print(test_agent1.get_distance_to((5,5)))
"""
