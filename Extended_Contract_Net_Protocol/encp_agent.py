#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 23:29:43 2017
@author: loan
"""

#import encp_manager as manager
import math
import copy

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
#@preferences[], a List with ID'S of all Agents, preferences[0] most favorized manager, pref[n] lest favorized manager
    def __init__(self, x, k, g, p):
        # def __init__(self, capacity, location, speed, preferences):
        self.id = Agent.id_counter
        self.location = x
        self.capacity = k
        self.speed = g
        self.preferences = p
        #self.schedule = {} 
        Agent.instances.append(self)
        Agent.id_counter += 1
        self.schedule =  OrderedDict()#key: manager , value0: bid value , value1 : bool defentive? 
        

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
            

#sum up the distances for the managers we already gave DEf bids to
    def sum_def_path(self,manager_new,manager_already_in_schedule):#a
        last_stop=0
        managers_calculated_count=0
        last_location=self.location
        dist = 0
        for manager_it in self.schedule:#sum all previous bids which where DEF first! ITERATE WITH PREFERENCES!
            if self.schedule[manager_it][1]==True:
                if(managers_calculated_count == 0):
                    dist+=self.calculate_distance(self.location,manager_it.x)                
                else:
                    dist+=self.calculate_distance(last_stop,manager_it.x)                
                print("AG-ID:"+str(self.id)+"Def bid for manager ID:"+str(manager_it.id)+"calculated dist sofar: "+str(dist))
                last_stop = manager_it.x
                managers_calculated_count+=1
        return dist

#sum up all the locations for pre bids given to managers, starting from location start
    def sum_pre_path(self,manager_new,manager_already_in_schedule):
        last_stop=0
        managers_calculated_count=0
        last_location=self.location
        last_manager_added=0
        dist = 0
        for manager_it in self.schedule:
            #print("AG-ID:"+str(self.id)+"Schedule entry for Manager ID:" + str(manager_it.id)+"is :" + str(self.schedule[manager_it]))            
            #print("man calc count ="+ str(managers_calculated_count))
            if self.schedule[manager_it][1]== False:
                if managers_calculated_count == 0 :           
                    #print("calc own dist")
                    dist+= self.calculate_distance(self.location,manager_it.x )#shoudnt actually happen
                else:
                    #print("calc last manager to man it dist LasT ID : "+ str(last_manager_added.id )+ "IT ID:" +str(last_manager_added.id))
                    dist+=self.calculate_distance(last_manager_added.x,manager_it.x)  
            last_manager_added = manager_it
            managers_calculated_count+=1

        
    def get_schedeuled_distance_to(self,manager_new):
        dist=0
        last_manager_added=0
        managers_calculated_count=0
        last_location=self.location
        
        manager_already_in_schedule=False
       
        if manager_new in self.schedule :           
            manager_already_in_schedule = True#setup help var
        
        
        if(len( self.schedule)==0):# if schedule is empty, this will return false -> no need is taking care of scheduling
          print("AG-ID:"+str(self.id)+"schedule was empty")
          dist= self.calculate_distance(self.location,manager_new.x )
          return dist 

        if(len(self.schedule)== 1 and manager_already_in_schedule == True):#same case as above, if only 1 agent in schedule and we calculate bid for him, we dont need taking care of scheduling
          dist= self.calculate_distance(self.location,manager_new.x )
          return dist 

        #manager is not yet in schedule and schedule len >= 1
          dist+=self.sum_def_path(manager_new,manager_already_in_schedule)                
          print("AG-ID:"+str(self.id)+ "Def Path calculation Returned:"+str(dist))
          


#sum up all pre bids                     TODO modularize this to function  sum_pre_path()
        for manager_it in self.schedule:
            #print("AG-ID:"+str(self.id)+"Schedule entry for Manager ID:" + str(manager_it.id)+"is :" + str(self.schedule[manager_it]))            
            #print("man calc count ="+ str(managers_calculated_count))
            if self.schedule[manager_it][1]== False:
                if managers_calculated_count == 0 :           
                    #print("calc own dist")
                    dist+= self.calculate_distance(self.location,manager_it.x )#shoudnt actually happen
                else:
                    #print("calc last manager to man it dist LasT ID : "+ str(last_manager_added.id )+ "IT ID:" +str(last_manager_added.id))
                    dist+=self.calculate_distance(last_manager_added.x,manager_it.x)  
            last_manager_added = manager_it
            managers_calculated_count+=1



        if manager_new not in self.schedule: #if he isnt there, we didint take care of him, since weonly worked with schedules
            dist+=self.calculate_distance(last_manager_added.x,manager_new.x)  
                        

        print("AG-ID:"+str(self.id)+"calculated Scheduled dist" + str(dist))            
         
        return dist 
        
        

##edge from step 1 to 2,
    def send_pre_bid(self,manager):
        print("AG-ID:"+str(self.id)+"<______IN PRE BID FOR_________MANAGER  ID: "+str(manager.id))
        new_pre_bid = self.get_schedeuled_distance_to(manager)
        

        if manager in self.schedule:
            if (new_pre_bid< self.schedule[manager][0]):#only send the bid, when it was better than the old one
                print("AG-ID:"+str(self.id)+"sending Imrpoved bid :"+ str(new_pre_bid) + "old bid was: "+ str(self.schedule[manager][0]))
                self.schedule[manager]=[new_pre_bid,False] # key: manager, value is the bid the agent send him            
                manager.recv_pre_bid(self,new_pre_bid)          
#                print("AG-ID:"+str(self.id)+", schedule is "+ str(self.schedule))
                return new_pre_bid
            else :
                print("AG-ID:"+ str(self.id)+ " Old bid:"+str(self.schedule[manager][0])+", new bid:"+ str(new_pre_bid)+", Stoping Bidding with M-"+str(manager.id))
                self.schedule.pop(manager)
                return new_pre_bid#or maybe smth else but not nothing!or mybe?

        print("AG-ID:"+str(self.id)+"sending FIRST pre bid value: "+str(new_pre_bid)+(" to manager ID : "+str(manager.id)))
        self.schedule[manager]= [new_pre_bid,False]#update schedule with a list
        return new_pre_bid
        
# edge from step 3 to 5
    def send_def_bid(self,manager):
        
        self.schedule[manager]= [math.inf,True]
        #call special def bid function?
        def_bid = self.get_schedeuled_distance_to(manager)            
        print("AG-ID:"+ str(self.id)+ "sending def bid Value:" + str(def_bid)+"to Manager ID: " + str(manager.id))
        manager.recv_def_bid(self,def_bid)


# edge from step 2 to 4
#TODO re schedeuling 
#called when recieving a pre reject, try to reschedule and send a better bid
    def recv_pre_reject(self,manager):
        
        print("Ag-ID "+  str(self.id)+"Recieved pre Reject from Manager ID : "+ str(manager.id))
        self.send_pre_bid(manager)#try to send a better bid
        


# edge from step 2 to 3
    def recv_pre_accept(self,manager):
        
        print("Ag-ID "+  str(self.id)+"Recieved pre Accept from Manager ID : "+ str(manager.id))
        self.send_def_bid(manager)


# edge from step 5 to 6 AGENT IS DONE FOR THIS SIM AND MANAGER
    def recv_def_accept(self,manager):
        #if we recieve def accept and manager is not in schedeule, this means special case, we were perviously rejected and coudnt improve, but manager wants old bad bid->!wokrs!
        print("Ag-ID "+  str(self.id)+"Recieved |def Accept| WON BIDDING WITH BID >>>>"+ str(self.schedule[manager][0] )+ "FOR MANAGER ID" + str(manager.id))
        self.schedule[manager]= [self.schedule[manager][0],True]
        self.send_def_bid(manager)
        #todo, start doing job and def add to schedeule

# edge from step 4 to 7 TODO IMPLEMENT RESCHEDEULING
#should be done,e agent should just stop communicating after def rreject
    def recv_def_reject(self,manager):
        print("Ag-ID "+  str(self.id)+"RECIEVED |DEFF REJECT| FROM MANAGER >>>>"+ str(manager.id))
        if manager in self.schedule:
            self.schedule.pop(manager, None)

        
"""        
        print("AG-ID:"+str(self.id)+"SCHEDULE NOT EMPTY! ") 
        for manager_it in self.schedule:#sum all previous bids 
            last_manager_added= manager_it
            #print("it id:"+str(manager_it.id)+ ("new id:")+ str(manager_new.id))
            if manager_it.id != manager_new.id:
                dist+= self.schedule[manager_it][0]  #bid value  saved in thee dict
                #print("DIST is " +str(dist))
                last_manager_added= manager_it #in new Python versions, Dicts are orderd, so in the last iteration last_manager should become last manager added to dict
                
        #print("last manager added" + str(last_manager_added.x[1]))
        if last_manager_added.id == manager_new.id:#only 1 manager in schedule
            dist =self.calculate_distance (self.location, manager_new.x)#calculate distance from last job on schedule to new job from manager_new        
            print("AG-ID:"+str(self.id)+"calculated Scheduled dist" + str(dist))
            return dist                         
        dist += self.calculate_distance (last_manager_added.x, manager_new.x)#calculate distance from last job on schedule to new job from manager_new
        
        print("AG-ID:"+str(self.id)+"calculated Scheduled dist" + str(dist))            
        return dist
"""
