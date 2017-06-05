#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 23:30:59 2017

@author: loan
"""

import numpy as np
import math
class encp_manager():
    
    object_counter = 0
    instances = []
    id_counter = 0
    
    
    #@param location, which location will be managed by this manager
    def __init__(self, location):
        best_bid= (math.inf,None ) # best_bid(0) is value of Best bid, best_bid(1) is that corrosponding bidding Agent
        self.bids = {}# Dictionary for Key:Agent Value:BestBid of Agent
        self.location = location#which field does the ENCP manager manage
        self.phase = 1#inital phase 1 of 2 
        self.id = encp_manager.id_counter
        encp_manager.id_counter += 1
        self.phase = 1        
    
    def manage(self):
    #function that manages ai/acting of manager
    #inital call of this method, to start manager 
    #once Task is managed, encp_manager instance will terminate through this method, free ressources?
    
        recv_pre_bids()#collect al inital pre bids
        send_pre_reject()#send reject to every agent, who is not best_bid[0]
        send_pre_accept()#send pre accet to agent, who is best_bid[0]            

    #edge from 1 to 2, collect all pre bids
    def recv_pre_bids(self):
        for agent in Agent.instances:#ANNOUNCE TASK/Inform Every Agent and get Pre Bid (1) Task Announcement and (2) Recieving end of Pre Bid
            self.bids[agent] = agent.getPreBid(location,self)#aka Call for proposals(cfp),Use Agent as Key and Bid as Value                
            print("Recieved bid :" + str(bid[agent]) + "from Agent :"+ str(agent.id))
        for bid in bids:#find best bidder, send him Pre Accept, Pre Reject to the rest
            if(best_bid[0]> bid[0]):
                best_bid[0] = bid[0]
                best_bid[1] = best_bid # the key of the dict is the Agent id!
            else : a = 1#we could already send pre rejects here for optimization, but meh.. do thema all at once later   
        print("best Bidder is:"+ best_bid[0])
       
        ##send pre reject /acc

    
    
    #edge from step 2 to 4 
    def send_pre_reject(agent):
        #iterate over all agents, send Rej to everyone except best_bid[1], which is the ID of best bidder
        #for agent in Agent.instances:
         #   if (ag)
        
        
 
        return " TODO"


    #edge from 2 to 4
    def send_pre_accept(agent):
        return "TODO"
    
    def recv_pre_bids(agent):
        return "todo"
    
    #Edge from 3 to 5
    def recv_def_bids(agent):
        return " todo"
    
    #edge from 5 to 6 -> END OF protocoll
    def send_def_accept(agent):
        return "todo"

    #edge from 5 to 7 -> END of protocoll
    def send_def_reject(agent):
        return "todo"