#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 23:29:43 2017

@author: loan
"""

#import encp_manager as manager
import math
from collections import OrderedDict # so we can remember, in which order we set the bids

class Agent():
    instances = []
    id_counter = 0


# x ∈ L.Orte – Position des Agenten zu Beginn einer Simulation.
# @param location : (x,y)  X eight/vertical, Y Horizontal
# k ∈ {1, ..., kmax} – Kapazität: drückt aus, wie viele Kilometer der Agent ohne Batteriewechsel fahren kann. Zu Beginn ist die Batterie voll geladen.
# g ∈ {1, 2, 3, 4} - Geschwindigkeit: Anzahl der Kilometer, die der Agent in einem Zeitschritt fahren kann.
#   p = (t1, ..., tm) mit ∀i,k ti ∈ T.ID und ti ≠ tk
# Präferenzen: Nur Aufträge ti ∈ p kann der Agent bearbeiten. Immer wenn ein
# solcher Auftrag entsteht, nimmt der Agent am korrespondierenden ECNP
# teil. Entstehen 2 Aufträge ti ≠ tk gleichzeitig, dann drückt ti ≻ tk aus, dass der
# Agent die Task ti präferiert, d.h. sie möglichst früh anfährt1.



#@schedule, dictionary, Keys Managers:M-0,M-1,M-2.. , Values : next line
#@schedeule[a][0] is bid that was send last to that manager 
#@schedule[a][1] Boolean, IF true -> Bid send to Manager was DEFENTIVE, IF false -> Bid send to manager was PRE bid
#@schedule [a][n] A list , 2 elements 
    def __init__(self, id, x, k, g, p):
        # def __init__(self, capacity, location, speed, preferences):
        self.id = Agent.id_counter
        self.location = x
        self.capacity = k
        self.speed = g
        self.preferences = p
        #self.schedule = {} 
        Agent.instances.append(self)
        Agent.id_counter += 1
        self.schedule =  {}#key: manager , value0: bid value , value1 : bool defentive? 
        

    def __str__(self):
        return "Agent ID: " + str(self.id) + "Location: " + str(self.location) + "Capacity:" + str(
            self.capacity) + "Speed: " + str(self.speed) + "Preferences: " + str(self.preferences)


# calculate using  |x1-x2| + |y1-y2|
# todo Schedule berücksichtigen
    def get_distance_to(self, location):
        dist = abs(self.location[0] - location[0] )+ abs(self.location[1] - location[1])
        return dist



# calculate using  |x1-x2| + |y1-y2| , for location a to location b (tuples (x,y))
    def calculate_distance(self,a,b):
        
        
        
        
        dist = abs(a[0] - b[0] )+ abs(a[1] -b[1])
        

        return dist
            

#redeschedule and try better bid
    def get_schedeuled_distance_to(self,manager_new):
        #dist=self.get_distance_to(location)#todo take care of reschedule
        last_manager_added=1
        dist=0
        for manager_it in self.schedule:#sum all previous bids 
            dist+= self.schedule[manager_it][0]  #bid value  saved in thee dict
            print("value is " +str(self.schedule))
            last_manager_added= manager_it #in new Python versions, Dicts are orderd, so in the last iteration last_manager should become last manager added to dict
                
        print("last manager added" + str(last_manager_added.x[1]))
        dist += self.calculate_distance (last_manager_added.x, manager_new.x)#calculate distance from last job on schedule to new job from manager_new
        print("calculated Scheduled dist" + str(dist))
            
        return dist


##edge from step 1 to 2,
    def send_pre_bid(self,manager):
        new_pre_bid = self.get_distance_to(manager.x)#ACTUALLY GET RESCHEDUELED DISTANCE
               
        if(not self.schedule == True):# if schedule is empty, this will return false -> no need is taking care of scheduling
        #take care of sending the bid /actucally finding out if it is better
            if manager  in self.schedule:# if this is the case, we have already send the manager a bid, now we must try to reschedule and send a better one
                if (new_pre_bid< self.schedule[manager][0]):#only send the bid, when it was better than the old one
                    print("AG-ID:"+str(self.id)+"sending Imrpoved bid :"+ str(new_pre_bid))
                    self.schedule[manager]=[new_pre_bid,False] # key: manager, value is the bid the agent send him            
                    manager.recv_pre_bid(self,new_pre_bid)          
            else:
                print("AG-ID:"+str(self.id)+"sending FIRST bid to the manager")
                self.schedule[manager]= [new_pre_bid,False]#update schedule with a list
                return new_pre_bid  

        #handling reschedule, since schedule is not empty
        scheduled_bid= self.get_schedeuled_distance_to(manager)
        
        print("TRYED SCHEDULED BID" +str(scheduled_bid))
        print("AG-ID:"+ str(self.id)+ " Cannot send improved bid, Stoping Bidding with M-"+str(manager.id))
        return math.inf# maybe smth else here.... maybe old bid again?

# edge from step 3 to 5
    def send_def_bid(self,manager):
#        def_bid= get_dstance_to(manager.)
        def_bid=self.get_distance_to(manager.x)#TODO TAKE CARE OF SCHEEDULEEs
        
        print("AG-ID:"+ str(self.id)+ "sending def bid Value:" + str(def_bid))
        manager.recv_def_bid(self,def_bid)


# edge from step 2 to 4
#TODO re schedeuling 
#called when recieving a pre reject, try to reschedule and send a better bid
    def recv_pre_reject(self,manager):
        self.send_pre_bid(manager)#try to send a better bid
        


# edge from step 2 to 3
    def recv_pre_accept(self,manager):
        print("Ag-ID "+  str(self.id)+"Recieved pre Accept")
        self.send_def_bid(manager)


# edge from step 5 to 6 TODO IMPLEMENT Rescheduleuing
    def recv_def_accept(self,manager):
        print("Ag-ID "+  str(self.id)+"Recieved |def Accept| WON BIDDING WITH BID"+ str(self.schedule[manager][0] ))
        self.schedule[manager][1]= True#set DEF bool

        #todo, start doing job and def add to schedeule

# edge from step 4 to 7 TODO IMPLEMENT RESCHEDEULING
#should be done,e agent should just stop communicating after def rreject
    def recv_def_reject(self,manager):
        print("Ag-ID "+  str(self.id)+"Recieved Def Rej, LOST BIDDING WITH BID:"+str(self.schedule[manager][0]))
        self.schedule.pop(manager, None)

    

