#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 23:29:43 2017

@author: loan
"""

#import encp_manager as manager

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


    def __init__(self, id, x, k, g, p):
        # def __init__(self, capacity, location, speed, preferences):
        self.id = Agent.id_counter
        self.location = x
        self.capacity = k
        self.speed = g
        # jede Präfrenz kommt einmalig vor
        self.preferences = p

        self.schedule = "empty" #implement as dictionary, keys:0,1,2.. values, where 0 is key for job with highest priority  #values are tuples (location,manager), with location = location of job and and manager = manager who gave the job
        Agent.instances.append(self)
        Agent.id_counter += 1


    def __str__(self):
        return "Agent ID: " + str(self.id) + "Location: " + str(self.location) + "Capacity:" + str(
            self.capacity) + "Speed: " + str(self.speed) + "Preferences: " + str(self.preferences)


# calculate using  |x1-x2| + |y1-y2|
# Schedule berücksichtigen
    def get_distance_to(self, location):
        dist = self.location[0]# - location[0] #+ abs(self.location[1] - location[1])
        print("Agent with ID:"+ str(self.id)+"sends bid to:"+"<Manager>"+ " with Bid Value:" + str(dist) + "for Location" + str(location))
        return dist


##edge from step 1 to 2,  should be done?
    def send_pre_bid(self, x, manager):
        bid = self.get_distance_to(x)
        #self.schedule.append(x)


        return bid


# edge from step 3 to 5
    def send_def_bid(self,manager):
#        def_bid= get_dstance_to(manager.)
        def_bid="placeholder"
        
        print("Agent ID:"+ str(self.id)+ "sending def bid Value:" + str(def_bid)+ "for Manager loc:" + str(manager.x))
        manager.recv_def_bids(self,def_bid)

# edge from step 2 to 4
#TODO re schedeuling 
    def recv_pre_reject(self,manager):
        print("Recieved pre rej, i have ID "+  str(self.id))
        return "TODO"


# edge from step 2 to 3
    def recv_pre_accept(self,manager):
        print("Recieved pre acc, i have ID " + str(self.id))
        self.send_def_bid(manager)
        return "TODO"


# edge from step 5 to 6
    def recv_def_accept(self):
        return "Todo"


# edge from step 4 to 7
    def recv_def_reject(self):
        return "TODO"


    def get_id(self):
        return self.id
