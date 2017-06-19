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
        self.max_capacity = k
        self.charge = k
        self.speed = float(g)
        self.preferences = p
        #self.schedule = {}
        Agent.instances.append(self)
        Agent.id_counter += 1
        self.schedule =  OrderedDict()#key: manager , value0: bid value , value1 : bool defentive?
        self.def_path_sum = 0
        self.def_path = [] #of managers
        self.def_path_charge = 0
        self.pre_path = []#
        self.pre_path_sum = 0
        self.tasks = []
        self.last_def_location = self.location
        self.last_pre_location = self.location
        self.all_path_sum = 0
        self.order  = []


    def calc_distance_to_known_manager_prefered(self,manager):
        first =self.location
        dist = 0
        dist+=self.def_path_sum
        #print("Adding def_path_sum" + str(self.def_path_sum))
        #start either from self or last def bid location
        if len(self.def_path)== 0 :
            first =self.location
        else:
            first = self.def_path[-1]
            
        for pref in range(0,4):#first pos of pre_path should be most favored manager, since we call agents in Pref order
            for manager_it in self.pre_path:
                #print("PREF IS :" + str(pref)+"And manager to calc is" + str(manager_it.id))
                if manager_it.id == pref:
                    #print("calc and pref was same and "+ str(tuple == type (first)))
                    if( tuple == type (first)):#special case, because if first = self.location we need to call function differntly
                        dist+=self.calculate_distance(first,manager_it.x)[1]
                        #print("CALC FOR TUPLE is "+ str(dist)+" For "+str(first) + "To"+ str(manager_it.x))
                        
                        first=manager_it

                    else:
                        print(type(first))
                        dist+=self.calculate_distance(first.x,manager_it.x)[1]
                        #print("CALC FOR NOT TUPLE is "+ str(dist)+" For "+str(first.x) + "To"+ str(manager_it.x))

                        first=manager_it
                        
                #print("DIST IS" + str (dist))
            
            if pref ==manager.id:#manager for pref =ID has been taken care of
                print("AG-ID: "+str(self.id)+"Calculated ---PREF--- dist:"+ str(dist)+"for Manager ID: "+str(manager.id))
                return dist

    

    def __str__(self):
        return "Agent ID: " + str(self.id) + "Location: " + str(self.location) + "Capacity:" + str(
            self.capacity) + "Speed: " + str(self.speed) + "Preferences: " + str(self.preferences)




#move after every time step
    def move(self):
        
        if self.def_path != []:#do we have a location to move to?
            self.last_pre_location = self.def_path[-1].x
        
        return 1+1#TODO
        
            
            
        
# calculate using  |x1-x2| + |y1-y2| , for location a to location b (tuples (x,y))
    def calculate_distance(self,a,b):

        raw = abs(a[0] - b[0] )+ abs(a[1] -b[1])
        charges = self.plan_charge(self.charge, raw)[0]
        dist = math.ceil(raw / self.speed)
        dist += charges
        return (dist, raw)

    # return how many charges are needed
    def plan_charge(self, charge, distance):
        ret = -1  # first iteration wouldnt need recharge
        c = charge
        d = distance
        while d >= 0:
            d -= c
            if d>c:
                c = self.max_capacity
            if d <= 0:
                c = c- d
            ret = ret + 1
        new_charge = c
        return (ret, new_charge)


    def get_scheduled_distance_to_new_manager(self, manager_new, pre_accepted=False):
        dist = 0
        #print("AG-ID: "+ str(self.id)+ "CALCULATING BIDS FOR NEW MANAGER AND pre PATH SUM IS _ "+ str(self.pre_path_sum))
        dist += self.def_path_sum
  
        
        
        if self.pre_path != []:
            dist+= self.calculate_distance(self.last_pre_location, manager_new.x)[1]
           # print("PRE LOC IS:" + str(self.last_pre_location)+ "and BID for "+str(manager_new.x)+"IS"+str(dist)+"ADDING PRE PATH"+ str(self.pre_path_sum))
            dist += self.pre_path_sum
            self.tasks.append(manager_new)
            if manager_new not in self.pre_path:
                self.pre_path.append(manager_new)
            self.update_pre_path_sum_and_last_pre_loc()
            #print("AG-ID:"+str(self.id)+"CALCULATED DISTANCE TO: " + str(manager_new.x )+"VALUE: " +str(dist))

            return dist
            #self.update_pre_path_sum_and_last_pre_loc()
            
            
        
        
       # print("AG-ID:"+str(self.id)+"PRE PATH SUM RETURNED: " + str(dist)+"and pre_path sum is"+ str(self.pre_path_sum))     
        dist += self.calculate_distance(self.last_pre_location,manager_new.x)[1]
        
        
        self.tasks.append(manager_new)
        self.pre_path.append(manager_new)
        self.update_pre_path_sum_and_last_pre_loc()
        #print("AG-ID:"+str(self.id)+"CALCULATED DISTANCE TO: " + str(manager_new.x )+"VALUE: " +str(dist))
       
        return dist


    def get_scheduled_distance_to_known_manager(self, manager_new, pre_accepted=False):
        dist = 0
 

        #print("AG-ID:"+str(self.id)+"CALCULATING BIDS FOR KNOWn MANAGER")
        
        dist+=self.def_path_sum
        
        self.update_pre_path_sum_and_last_pre_loc()
        dist += self.pre_path_sum
        
        #print("AG-ID:"+str(self.id)+"PRE PATH SUM IS:" + str(self.pre_path_sum)+"and dist is"+str(dist))
     
        if manager_new not in self.pre_path:
            self.pre_path.append(manager_new)
            dist += self.calculate_distance(self.last_pre_location,manager_new.x)[1]
        
        #self.last_pre_location = manager_new.x
        #self.pre_path_sum = dist
        #print("AG-ID:"+str(self.id)+"CALCULATED DISTANCE TO: " + str(manager_new.x )+"VALUE: " +str(dist))
        #print("AG-ID:"+str(self.id)+"old prepath="+str(self.pre_path_sum)+ "and new" + str(dist))        

        self.last_pre_location = manager_new.x        
        
        return dist



    def dist_of_path(self,path):#first is a tupel
        dist = 0
        if path == []:
            return 0
        first = path[0]
        
        if len(path) == 1 :
            #print("path len was 1")
            if self.def_path != []:
               dist += self.calculate_distance(self.def_path[-1].x,path[0].x)[1]
    
            else :
                dist += self.calculate_distance(self.location,path[0].x)[1]
                return dist        

        
        
        for manager_it in path:
           # print("first ID is "+str(first.id)+"and manager_it is :"+str(manager_it.id))
            if(first.id != manager_it.id):
                distx= self.calculate_distance(first.x,manager_it.x)[1] 
             #   print("TO "+str(dist)+"ADDING"+str(distx)+"FOR"+str(first.x) +"AND"+str(manager_it.x))

                dist+=distx
            if(first.id == manager_it.id):
                distx = self.calculate_distance(self.location,first.x)[1]
              #  print("TO "+str(dist)+"ADDING"+str(distx)+str(first.x) +"AND SELF")               
                dist+= distx
            first= manager_it
            
        return dist

    def print_pre_path(self):
        string=""
        for loc in self.pre_path:
            string+=loc.x
        print("PRE PATH IS:"+string)
        
        
    def update_pre_path_sum_and_last_pre_loc(self):
         #print("UPDATING LOC FROM"+str(self.last_pre_location))        
         if self.pre_path == [] :
             self.last_pre_location=self.location
         else : 
             self.last_pre_location= self.pre_path[-1].x
       #      print("UPDATING TO-->"+str(self.last_pre_location))        
        #     print("UPDATING TO-->"+str(self.last_pre_location))        

             
         #print("UPDATING PRE PATH FROM:"  +str(self.pre_path_sum))
         self.pre_path_sum = self.dist_of_path(self.pre_path)
         #print("UPDATING PRE PATH TO:"  +str(self.pre_path_sum))

 
##edge from step 1 to 2,
    def send_pre_bid(self,manager):
        print("AG-ID:"+str(self.id)+"<______IN PRE BID FOR_________MANAGER  ID: "+str(manager.id))
        if manager not in self.tasks:#adds manager to task/schedule
            #bid = self.get_scheduled_distance_to_new_manager(manager) OLD V
            self.pre_path.append(manager)
            self.tasks.append(manager)
            bid = self.calc_distance_to_known_manager_prefered(manager)              
            self.schedule[manager]= [bid,False]#update schedule with a list  
            print("AG-ID : " +str(self.id)+"SENDING FIRST PRE BID :" +str(bid))
            return bid
        #we are sending a new bid, we must have been rejected
        if manager in self.tasks:    
            bid = self.calc_distance_to_known_manager_prefered(manager)
            print("AG-ID : " +str(self.id)+"SENDING NEW PRE BID :" +str(bid))            
            #bid= self.get_scheduled_distance_to_known_manager(manager)            
            self.schedule[manager]= [bid,False]
            
            return bid

# edge from step 3 to 5
    def send_def_bid(self,manager):

        #call special def bid function?
        #def_bid = self.get_scheduled_distance_to_known_manager(manager, True)
        def_bid = self.calc_distance_to_known_manager_prefered(manager)
        print("AG-ID: "+ str(self.id)+ "sending def bid Value:" + str(def_bid)+"to Manager ID: " + str(manager.id))
        #print("SENDING DEF BID"+ str(def_bid))
        manager.recv_def_bid(self,def_bid)


# edge from step 2 to 3
    def recv_pre_accept(self,manager):
        #self.path
        print("Ag-ID "+  str(self.id)+"Recieved pre Accept from Manager ID : "+ str(manager.id))
        self.send_def_bid(manager)

# edge from step 2 to 4
#TODO re schedeuling
#called when recieving a pre reject, try to reschedule and send a better bid
    def recv_pre_reject(self,manager):
#        self.pre_path.remove(manager)
        
        print("Ag-ID: "+  str(self.id)+"Recieved pre Reject from Manager ID : "+ str(manager.id))
        new_bid = self.calc_distance_to_known_manager_prefered(manager)#try to send a better bid
            
        if new_bid < self.schedule[manager][0]:
                print("AG-ID: "+str(self.id)+"sending Imrpoved bid : "+ str(new_bid) + "old bid was: "+ str(self.schedule[manager][0]))
                self.schedule[manager]=[new_bid,False] 
                self.last_pre_location = manager.x
                manager.recv_pre_bid(self,new_bid)#???

        else :
                print("AG-ID: "+ str(self.id)+ " Old bid: "+str(self.schedule[manager][0])+", new bid: "+ str(new_bid)+", Stoping Bidding with M-ID: "+str(manager.id))
                #self.schedule.pop(manager)
                self.schedule[manager]= [new_bid,False]#update schedule with a list
                
                self.pre_path.remove(manager)
                self.tasks.remove(manager)
                self.update_pre_path_sum_and_last_pre_loc()
#                self.last_pre_location = self.location
 #               if self.pre_path != []:
  #                  self.last_pre_location = self.pre_path[-1]
                return new_bid#or maybe smth else but not nothing!or mybe?




# edge from step 5 to 6 AGENT IS DONE FOR THIS SIM AND MANAGER
    def recv_def_accept(self,manager):
        #if we recieve def accept and manager is not in schedeule, this means special case, we were perviously rejected and coudnt improve, but manager wants old bad bid->!wokrs!
        print("Ag-ID: "+  str(self.id)+"Recieved |DEFF ACCEPT| WON BIDDING WITH BID >>>>"+ str(self.schedule[manager][0] )+ "FOR MANAGER ID" + str(manager.id))
        self.def_path.append(manager)
        self.pre_path.remove(manager)
        self.last_def_location=manager.x
        self.schedule[manager][1]= True
        self.def_path_sum+= self.schedule[manager][0]#altes gebot summieren auf path

# edge from step 4 to 7 TODO IMPLEMENT RESCHEDEULING
#should be done,e agent should just stop communicating after def rreject
    def recv_def_reject(self,manager):
        print("Ag-ID: "+  str(self.id)+"RECIEVED |DEFF REJECT| FROM MANAGER >>>>"+ str(manager.id))
        if manager in self.schedule:
            self.schedule.pop(manager, None)
            #self.tasks.remove(manager)         should already be removeds
            #print("PRE PATH IS"+str(self.pre_path))
            #self.pre_path.remove(manager)should be romoved alreadxy
        if self.pre_path != []:
            self.last_pre_location=self.pre_path[-1].x
        #??

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
-----------------------------------
   def get_scheduled_distance_to(self, manager_new, pre_accepted = False):
        dist=0
        last_manager_added=0
        managers_calculated_count=0
        manager_already_in_schedule = False
        last_location = self.location
        bid_sum = 0
        if self.def_path != []:
            last_location =self.def_path[-1].x

        #if last_location == manager_new.x | self.location ==manager_new.x:

         #   return 0

        if pre_accepted :
            manager_already_in_schedule = True #setup help var
            dist = self.calculate_distance(last_location, manager_new.x)[0]
            raw_dist = self.calculate_distance(last_location, manager_new.x)[1]
            #self.schedule[manager_new][1] = True
            self.def_path.append(manager_new)
            self.pre_accepted_tasks.remove(manager_new)
            self.def_path_charge = self.plan_charge(self.def_path_charge, raw_dist)
            return self.def_path_sum

        #self.calculate_distance(last_location, manager_new.x)

        # if(len( self.schedule)==0):# if schedule is empty, this will return false -> no need is taking care of scheduling
        #   print("AG-ID:"+str(self.id)+"schedule was empty")
        #   dist = self.calculate_distance(self.location,manager_new.x )
        #   return dist

        #if(len(self.schedule)== 1 and manager_already_in_schedule == True):#same case as above, if only 1 agent in schedule and we calculate bid for him, we dont need taking care of scheduling
         # dist= self.calculate_distance(self.location,manager_new.x )
          #return dist

        #manager is not yet in schedule and schedule len >= 1
        self.def_path_sum =

            dist +=self.sum_def_path(manager_new,manager_already_in_schedule) #TODO UPDATE self location
            print("AG-ID:"+str(self.id)+ "Def Path calculation Returned:"+ str(dist))



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



        if manager_new not in self.schedule: #if he isnt there, we didint take care of him, since we only worked with schedules
            dist+=self.calculate_distance(last_manager_added.x,manager_new.x)


        print("AG-ID:"+str(self.id)+"calculated Scheduled dist" + str(dist))

        return dist
"""
