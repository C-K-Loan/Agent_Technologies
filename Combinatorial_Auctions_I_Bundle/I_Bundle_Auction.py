import numpy as np
import math
import copy
#from I_Bundle_Agent import Bid 
#from I_Bundle_Agent import Agent

class Auction():
    instances = []
    id_counter = 0

    def __init__(self,bundle_list,agent_list,epsilon ):
        self.id = Auction.id_counter
        self.agent_list = agent_list
        self.bundle_list = bundle_list
        Auction.instances.append(self)
        Auction.id_counter += 1
        self.agents_bid_list = {}# dictonary with key= Agent, Value is the bid list from that agent , for the list in the dict :  #[0] is bundle, [1] is bid value
        self.init_price_list()
        self.bids_recieved = 0 
        self.epsilon = epsilon # by how much do we increase prices 
        self.iteration = 0
        self.combi_dict = {}
        self.agents_out = 0
        self.all_bids_recieved = False

    def start_auction(self):
        
        self.advertise_bundles()#start by sending all agent pricelist
        
 
    def advertise_bundles(self):
        for agent in self.agent_list:
            agent.recv_price_list(self.price_list,self)
        
        

    def hello_auction(self):
        print("Hello from Auction!")
    
    def recv_leaving_notification(self,agent):
        # API for Agents, to inform Auction that there is nothimg Profitable left or this Agent-> Auction will wait or 1 Bid less per Iteration!
        self.agents_out +=1       
        if (self.bids_recieved == len(self.agent_list)-self.agents_out and self.all_bids_recieved == False):
            #make a delayed start, because main auction is waiting for this Agent and didint lower Expecting Agent Count in Time
            self.recv_bid_list("DEBUG","DEBUG",False)#call recv bid function, but ignore values and just start auction if it is not already started!
        else : 
            pass
    
    def print_winners_and_loosers(self):
        win_str = "AUCTION : WINNERS: [ "
        loosers_str= "LOOSERS: [ "
        
        for ag in self.winner_list:
            win_str+="AG-ID "+ str (ag.id) + ", "
        
        win_str += "]"
        
        for ag in self.looser_list:
            loosers_str += " AG-ID " + str(ag.id) + ", "
        
        loosers_str += "]"
            
        print (win_str + loosers_str)
            
            
            
    def recv_bid_list(self, agent,bid_list,real_bid):
        if (real_bid == True):
            self.bids_recieved += 1 
            #recviece the bids of an agent and safe the bids until we have all bids recieved or Timeout
            self.agents_bid_list[agent] = bid_list# for Every Agent entry in DIct, there is a List of his XOR bids, #[0] is bundle, [1] is bid value
            #print("AUCTION: Recieved bid "+ str(bid_list[0][0].name) + "from agent" + str(agent.id) + "fscaor price" + str(bid_list[0][1]))

        if self.bids_recieved == len(self.agent_list)-self.agents_out:# ADD ENDING CONDITION, maybe self.agent_llist length = 1 or smth
            self.all_bids_recieved = True
            self.print_agents_bid_list()
            self.print_price_list()
            input("Iteration["+ str(self.iteration)+"]--------------------AUCTION RECIEVED ALL BIDS, PRESS [ENTER] TO EVALUATE. -----------")

            self.iteration +=1
  
            self.bids_recieved= 0
            #print("Auction: recieved all bids , deciding on winner....")
            self.calculate_all_possible_distributions()
            
            self.calculate_new_price_list()
            self.all_bids_recieved = False
            #input("Iteration:"+ str(self.iteration-1)+"--------------------Press Enter to Notify Agents ---------------------------------")
            
            self.print_winners_and_loosers()
            print("END OF ITERATION [" + str(self.iteration-1)+"]--------------------------------------------------------")
            input("START OF ITERATION[" + str(self.iteration)+"]-----PRESS [ENTER] TO NOTIFY AGENTS--------------------------------")
            
            print()
            self.notify_loosers()
            self.notify_winners()
           
            
    def calculate_new_price_list(self):#copy Old list, increase the price for each Bundle by epsilon
        for agent in self.looser_list:
            print("Auction: increasing Price for bundle : [ "+self.agents_bid_list[agent][0][0].name+ "] by " + str(self.epsilon)+" so it costs now " + str (self.price_list[self.agents_bid_list[agent][0][0]] +1))
            self.price_list[self.agents_bid_list[agent][0][0]] +=self.epsilon# the bundle, the agent wanted to win
        #self.print_price_list()
        
   

       
    def init_combo_dict(self,max_combo):
        #@param max_combo -> The amout of empty lists , for combos we will initilize in combo dict
        #initalize combo_list to size 1, just every bid we recieved
        init_combo_dict = {}
        for agent_it in self.agents_bid_list:
            #print("ele is " + str(self.agents_bid_list[agent_it][0][0].name))
            init_combo_dict[agent_it]= [([copy.copy(self.agents_bid_list[agent_it][0][0])],[[agent_it]])]#1 combo for every agent of size 1, his own bid
            
            for  i in range(max_combo):
                init_combo_dict[agent_it].append(([],[]))#initilize empty list, for the inner list of combos
        return init_combo_dict
            
      



     
    def find_compatible_bids_for_bundle(self,bundle, bundle_agents):
        #@param bundle_agents, the agents that belong to the bundle we want combinations for
        # given an N combo list, try to find N+1 Combo List
        #INPUT : list of compatible Bundles Size N  OUTPUT: List of compatible Bundles choosen self.agents_bid_list. So each Element in the Returnlist can make a compatible combo with input_bundle_list of size N+1 
        #IF no compatible bundles found, returns False! -> implies that we have tried out all possible combinations for that agent!
        combo_list = []
        #print("input Bundle is " + str (bundle.name))
        return_list = [] # A LIST WITH MERGED COMPATIBLE BUNDLES OF SIZE N+1
        for agent_it in self.agents_bid_list:
        #    print("Try to match with bundle " + str (self.agents_bid_list[agent_it][0][0].name))    
            if bundle.compatible(self.agents_bid_list[agent_it][0][0]):
        #        print("was compatible!")
                combo_list.append((self.agents_bid_list[agent_it][0][0],[agent_it]))
        
        if combo_list != []: #only create new bundles if we found compatible stuff
            for combo in combo_list :
                new_b= bundle.merge_with_bundle(combo[0])
                #print("New Combo" + str (new_b.name))
                
                return_list.append((new_b,bundle_agents+combo[1]))# we Append tupels (bundles|Agents belonging to bundle)
        #        print("merged new bundle" + str(new_b.name))
        #input("continue?")    
        #TODO BUILD CORRECT COMBO LIST! 
        # I.E. If Given A , and Found Combos with B, C
        #Return List[AB, AC]
        # Next iteration
        # GIVEN List [AB]
        if combo_list == []: return []
        else : return return_list
        
 #    def recv_win_notification(self,new_bundle_price_list,bundle_won,auctioneer):#Notify API for Auctioneer, to tell Agent he won
      
            
    def calculate_all_possible_distributions(self):# We do this by calculate_all_possible_distributions
        #calc all possible combinations, check  revenue for all and pick most profitable and distribute evenly

        combination_dict = copy.copy(self.init_combo_dict(10))# A Dict with Bidding Agents as Key and as Value a list of every posible combination , initialized with size 1 Combos(only 1 bid)
        combo_size= 0#
        new_combos = []
        x= 0 
        overall_combo_count= 0
        for agent_it in self.agents_bid_list:# calculate all possible combinations compatible with agents who send in bids. each bid agent has a combo list which is a list of all possible combination which are compatible
            #print("Auction: Calculating Combos for Bidder Agent-ID-" +str(agent_it.id))
            #print("Combo dict for this agent is: " + str(combination_dict[agent_it][0]))
            #new_combos[combo_size] = copy.copy(combination_dict[agent_it][0])#initially , we only have 1 combo, the bid of each agent
            #print("new comboat [0] is " + str(new_combos[0]))

            while (len(combination_dict[agent_it][combo_size][0]) != 0):# TODO, stop if no more new combos, for agent_IT
                #print("Calculating Combos for Input Size : " + str(combo_size +1))
                overall_combo_count+=1
                for bundle in combination_dict[agent_it][combo_size][0]:
                    #print("Searching Combos for : AG-ID-"+ str(agent_it.id) + "and Bundle [" +str(bundle.name)+ "]")
                    new_combos= self.find_compatible_bids_for_bundle(bundle,[agent_it])# returns list of combos with input Bundle and all other compatible bundles which are not already in the combo
                    combination_dict = self.update_combination_dict(combination_dict,agent_it,new_combos,combo_size)
                    #old_combos = combination_dict[agent_it][combo_size+1][0]
                    #print("old combos are " + str(old_combos))
                    #print("new combos are " + str (new_combos))
                   # new_combos += old_combos[0]
                    #combination_dict[agent_it][combo_size+1][0] += new_combos[0]
             #       print("GONNA CHECK: " + str(combination_dict[agent_it][combo_size][0]))
                    x+=1                    
                combo_size += 1
                x=0
            combo_size = 0
            
        #print("AUCTION: DONE COMPUTING ALL COMBINATIONS! Amount of Combos found: " + str(overall_combo_count))
        #self.print_combo_dict(combination_dict)
        #print("startung to Calculate Prices for All combos..")
        revenue_vector = self.calculate_revenue_vector(combination_dict)      
        max_rev = self.find_biggest_revenue_in_revenue_vector(revenue_vector)
        
        self.set_looser_list(max_rev)
        self.set_winner_list(max_rev)
        
        print("Auction: biggest Revenue from: AG " + self.print_max_rev(max_rev))
        #print(self.print_revenue_vecotr(revenue_vector))
        
        
 
    def print_max_rev(self,max_rev):
        print_str = "Bundle ["+ str(max_rev[0].name)+ "] for Revenue ( " + str(max_rev[1]) +" )$ and Agents ID "
        
        for agent in max_rev[2]:
            print_str += str(agent.id) + " and "
        return print_str 
 
    def print_revenue_vecotr(self,revenue_vector):
        print_str = ""
        for tripel in revenue_vector: 
            print_str += "B:"+ str(tripel[0].name) + "and AG:"
            for agent in tripel[2]:
                print_str += str(agent.id) + ","
            print_str+="Rev:"+str(tripel[1])
            print_str += "|"
        return print_str 
        
          
            
    
    
    
    def set_looser_list(self,max_rev):
        backup_list = []
        for agent in self.agents_bid_list:
            backup_list.append (agent)
        
        for agent in max_rev[2]:
            backup_list.remove(agent)
        self.looser_list = backup_list

    def set_winner_list(self,max_rev):
        backup_list = []

        for agent in max_rev[2]:
            backup_list.append(agent)
        self.winner_list = backup_list
 
    
    
    
    def find_biggest_revenue_in_revenue_vector(self,rev_vector):#check all combinations, return the one with biggest rev
        max_rev= [0,-(math.inf),0]#tripel [0] = Bundle  , tripel[1] revenue, tripel [2] Agents
        
        for tripel in rev_vector:
            #print("Checking : " + str(tripel[0].name) + " and rev" + str(tripel[1] ))
            #for agent in tripel[2]:
            #    print("and Agent " + str (agent.id))
            if tripel[1]>= max_rev[1] :
                max_rev = tripel
        
        return max_rev
            
            
            
            
    def get_revenue_for_agent_list(self,ag_list):#given a list of agents, returns the sum of all their bids
        rev_sum = 0
        
        for ag in ag_list :
            rev_sum += self.agents_bid_list[ag][0][1]
        return rev_sum

                    
                    
    def calculate_revenue_vector(self,combo_dict):#calculate a list with tupels of every combination, with the value of the Tupel
        combo_size = 0
        bundle_str= ""
        agent_str=""
        x= 0#für das wievielte bundle müssen wir eine Agentenliste besorgen? beschreibt x!
        rev_vector = []
        ag_list = []
        for agent_it in self.agents_bid_list:
            while(len(combo_dict[agent_it][combo_size][0]) != 0 ):
                for bundle in combo_dict[agent_it][combo_size][0]:
                    for agent_bidder in combo_dict[agent_it][combo_size][1][x]:
                        ag_list.append(agent_bidder)

                    x+=1
                    rev_vector.append((bundle,self.get_revenue_for_agent_list(ag_list),ag_list))
                    ag_list = []

                combo_size +=1
                x=0
            combo_size=0
        return rev_vector

    def print_combo_dict(self,combo_dict) :
        combo_size = 0
        bundle_str= ""
        agent_str=""
        x= 0#für das wievielte bundle müssen wir eine Agentenliste besorgen? beschreibt x!
        for agent_it in self.agents_bid_list:
            #print("for agent id : " +str(agent_it.id))
            while(len(combo_dict[agent_it][combo_size][0]) != 0 ):
                for bundle in combo_dict[agent_it][combo_size][0]:
                    bundle_str+= "|"+str(bundle.name)+"|"
                    #print("DEBUG:" +str(combo_dict[agent_it][combo_size][1][x]))
                    for agent_bidder in combo_dict[agent_it][combo_size][1][x]:
                        #print("Found AGENT!"+str(agent_bidder.id))
                        agent_str += "|"+str(agent_bidder.id)+"|"
                    #print("For Combo size " + str(combo_size)+" Found Combo"+ bundle_str +" and Agents" + str(agent_str))
                    #print("Bunlde Amount is "+ str(len(combo_dict[agent_it][combo_size][0]))+ "and aglist amount is " + str(combo_dict[agent_it][combo_size][1]))
                    bundle_str = ""
                    agent_str = ""
                    x+=1
                combo_size +=1
                x=0
            combo_size=0

            print()
            print()


            combo_size=0
            
    def update_combination_dict(self,combination_dict,agent_it,new_combos,combosize):
        for combo in new_combos:
            app_list=[]
            #print("cmbo is" + str(combo))
            #print("combo dict 0 is " + str(combination_dict[agent_it][combosize+1][0]))
            
            #print("combo dict 1 is " + str(combination_dict[agent_it][combosize+1][1]))
            combination_dict[agent_it][combosize+1][0].append(combo[0])#update bundle
            for ele in combo[1]:
                app_list.append(ele)
            #print("updating Dict with" + str(app_list))
            combination_dict[agent_it][combosize+1][1].append(app_list)#update agents
            #print("AFTER UPDATE : " )
            #print("combo dict 0 is " + str(combination_dict[agent_it][combosize+1][0][-1].name))
            #for ag in app_list:
            #    print("ID'S ARE:" +str(ag.id))
            #print("combo dict 1 is " + str(combination_dict[agent_it][combosize+1][1][-1][-1]))
            #print("combo dict 2 is " + str(combination_dict[agent_it][combosize+1][1][-1]))
            #print("combo dict 3 is " + str(combination_dict[agent_it][combosize+1][1]))
            #print("combo dict 4 is " + str(combination_dict[agent_it][combosize+1][1][0][0]))
            
        return combination_dict

    def print_bid_list(self,bid_list):
        for bundle in bid_list:
            print ("extra print" + bundle.name)

    def recv_test_agent(self,test_agent):
        test_agent.hello_agent()

    def init_price_list(self):
        #init all bundle prices to 0
        self.price_list = {}
        for bundle in self.bundle_list:
            self.price_list[bundle]= 0


       
    def notify_winners(self):#notify all agents, wo who the round
            notify_winnerlist = copy.copy(self.winner_list)
            self.winner_list = []
            for agent in notify_winnerlist:
            #print("Auction: Notifying Winner Agent ID   "+ str(element[0].id) +  " For Bundle " + element[1].name)
                agent.recv_win_notification(self.price_list,self.agents_bid_list[agent][0][0],self)
        
        
        

    def notify_loosers(self):#notify all agents who lost the round
        notify_looserlist = copy.copy(self.looser_list)
        self.looser_list = []
        for agent in notify_looserlist:
            #print("Auction: Notifying Looser Agent ID :   "+ str(element[0].id) + " for Bundle " +  element[1].name )
            agent.recv_loss_notification(self.price_list,self.agents_bid_list[agent][0][0],self)
        
        
    def type_bundles(self):
        for bundle in self.bundle_list:
            self.type_bundle[bundle.type]
     

    def find_winner(self):
        for bundle in self.bundle_list:
            print("bundle: " +  bundle.name)

    def compatible(self, b1, b2):
       # print ("comparing bundle" + str(b1.name))
        #print ("with bundle" + str(b2.name))
       # print (str(b1.name) + str(b2.name) + str((str(b2.n) ame+ str(b1.jobs))))

        if (str(b1.name) in str(b2.name)) or (str(b2.name) in str(b1.name)) :
            return False
        else: 
            #print(b1.name + " and " + b2.name +" compatible")
            return True

    def print_price_list(self):
        print_str= "Auction: Prices: "
        for bundle in self.price_list:
            print_str += "[ " + bundle.name + " ] P: " + str(self.price_list[bundle])+"|"
        print(print_str)
        
    def print_agents_bid_list(self):
        print_str="Auction: Recieved bids: "
        for agent_it in self.agents_bid_list:
            print_str+="AG-ID " + str(agent_it.id) + "Bid (" +str(self.agents_bid_list[agent_it][0][1]) +") for B["+str(self.agents_bid_list[agent_it][0][0].name)+"]|"
        print (print_str)            
