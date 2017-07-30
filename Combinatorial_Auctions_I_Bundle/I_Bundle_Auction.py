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

    def start_auction(self):
        
        self.advertise_bundles()#start by sending all agent pricelist
        
 
    def advertise_bundles(self):
        for agent in self.agent_list:
            agent.recv_price_list(self.price_list,self)
        
        

    def hello_auction(self):
        print("Hello from Auction!")
        

    def recv_bid_list(self, agent,bid_list):
        self.bids_recieved += 1 
        #recviece the bids of an agent and safe the bids until we have all bids recieved or Timeout
        self.agents_bid_list[agent] = bid_list# for Every Agent entry in DIct, there is a List of his XOR bids, #[0] is bundle, [1] is bid value
        #print("AUCTION: Recieved bid "+ str(bid_list[0][0].name) + "from agent" + str(agent.id) + "for price" + str(bid_list[0][1]))

        if self.bids_recieved == len(self.agent_list):
            self.print_agents_bid_list()

            input("Iteration:"+ str(self.iteration)+"--------------------ALL bids Recieved,Press enter to evaluate... ---------------------------------")
            self.iteration +=1
  
            self.bids_recieved= 0
            #print("Auction: recieved all bids , deciding on winner....")
            combo_dict = self.calculate_all_possible_distributions()
            
            # self.calculate_new_price_list()
            #self.print_price_list()
            #self.agents_bid_list = {}#reset bid list, so we forget bids. we should do this, since not every Agent must send a new bid!
            input("Iteration:"+ str(self.iteration-1)+"--------------------Press Enter to Notify Agents ---------------------------------")
      
            self.notify_loosers()
            self.notify_winners()
           
            
    def calculate_new_price_list(self):#copy Old list, increase the price for each Bundle by epsilon
        for element in self.looser_list:
            print("Auction: increasing Price for bundle [: "+ element[1].name + "] by " + str(self.epsilon))
            self.price_list[element[1]] +=self.epsilon# the bundle, the agent wanted to win
        #self.print_price_list()
        
   

       
    def init_combo_dict(self,max_combo):
        #@param max_combo -> The amout of empty lists , for combos we will initilize in combo dict
        #initalize combo_list to size 1, just every bid we recieved
        init_combo_dict = {}
        for agent_it in self.agents_bid_list:
            #print("ele is " + str(self.agents_bid_list[agent_it][0][0].name))
            init_combo_dict[agent_it]= [([copy.copy(self.agents_bid_list[agent_it][0][0])],[agent_it])]#1 combo for every agent of size 1, his own bid
            
            for  i in range(max_combo):
                init_combo_dict[agent_it].append(([],[]))#initilize empty list, for the inner list of combos
        return init_combo_dict
            
      



     
    def find_compatible_bids_for_bundle(self,bundle, bundle_agents):
        #@param bundle_agents, the agents that belong to the bundle we want combinations for
        # given an N combo list, try to find N+1 Combo List
        #INPUT : list of compatible Bundles Size N  OUTPUT: List of compatible Bundles choosen self.agents_bid_list. So each Element in the Returnlist can make a compatible combo with input_bundle_list of size N+1 
        #IF no compatible bundles found, returns False! -> implies that we have tried out all possible combinations for that agent!
        combo_list = []
        print("input Bundle is " + str (bundle.name))
        return_list = [] # A LIST WITH MERGED COMPATIBLE BUNDLES OF SIZE N+1
        for agent_it in self.agents_bid_list:
            print("Try to match with bundle " + str (self.agents_bid_list[agent_it][0][0].name))    
            if self.compatible(bundle, self.agents_bid_list[agent_it][0][0]):
                print("was compatible!")
                combo_list.append((self.agents_bid_list[agent_it][0][0],[agent_it]))
        
        if combo_list != []: #only create new bundles if we found compatible stuff
            for combo in combo_list :
                new_b= bundle.merge_with_bundle(combo[0])
                
                return_list.append((new_b,bundle_agents+combo[1]))# we Append tupels (bundles|Agents belonging to bundle)
                print("merged new bundle" + str(new_b.name))
        input("continue?")    
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
        winner_list = []
        looser_list = []
        combination_dict = copy.copy(self.init_combo_dict(10))# A Dict with Bidding Agents as Key and as Value a list of every posible combination , initialized with size 1 Combos(only 1 bid)
        false_counter = 0
        combo_size= 0#
        new_combos = []
        x= 0 
        overall_combo_count= 0
        for agent_it in self.agents_bid_list:# calculate all possible combinations compatible with agents who send in bids. each bid agent has a combo list which is a list of all possible combination which are compatible
            print("Auction: Calculating Combos for Bidder Agent-ID-" +str(agent_it.id))
            #print("Combo dict for this agent is: " + str(combination_dict[agent_it][0]))
            #new_combos[combo_size] = copy.copy(combination_dict[agent_it][0])#initially , we only have 1 combo, the bid of each agent
            #print("new comboat [0] is " + str(new_combos[0]))

            while (len(combination_dict[agent_it][combo_size][0]) != 0):# TODO, stop if no more new combos, for agent_IT
                print("Calculating Combos for Input Size : " + str(combo_size +1))
                bid = self.agents_bid_list[agent_it][0][1]
                overall_combo_count+=1
                for bundle in combination_dict[agent_it][combo_size][0]:
                    print("Searching Combos for : AG-ID-"+ str(agent_it.id) + "and Bundle [" +str(bundle.name)+ "]")
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
            
        print("AUCTION: DONE COMPUTING ALL COMBINATIONS! Amount of Combos found: " + str(overall_combo_count))
        self.print_combo_dict(combination_dict)
        print("startung to Calculate Prices for All combos..")
              
        
        return combination_dict

    def find_biggest_revenue_in_combo_dict(self,combo_dict):
        combo_size = 0
        max_rev = -(math.inf)
        





    def print_combo_dict(self,combo_dict) :
        combo_size = 0
        bundle_str= ""
        agent_str=""
        for agent_it in self.agents_bid_list:
            print("for agent id : " +str(agent_it.id))
            while(len(combo_dict[agent_it][combo_size][0]) != 0 ):
                for bundle in combo_dict[agent_it][combo_size][0]:
                    bundle_str+= "|"+str(bundle.name)+"|"
                for agent_it in combo_dict[agent_it][combo_size][1]:
                    agent_str += "|"+str(agent_it.id)+"|"
                print("For Combo size " + str(combo_size)+" Found Combos and Agents ")
                combo_size +=1
                print(str(bundle_str))
                print(str(agent_str))
                bundle_str = ""
                agent_str = ""
            combo_size=0
            
    def update_combination_dict(self,combination_dict,agent_it,new_combos,combosize):
        for combo in new_combos:
            #print("cmbo is" + str(combo))
            #print("combo dict 0 is " + str(combination_dict[agent_it][combosize+1][0]))
            
            #print("combo dict 1 is " + str(combination_dict[agent_it][combosize+1][1]))
            combination_dict[agent_it][combosize+1][0].append(combo[0])#update bundle
            for ele in combo[1]:
                combination_dict[agent_it][combosize+1][1].append(ele)#update agents
            #print("AFTER UPDATE : " )
            #print("combo dict 0 is " + str(combination_dict[agent_it][combosize+1][0]))
            
            #print("combo dict 1 is " + str(combination_dict[agent_it][combosize+1][1]))
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
        for element in self.winner_list:
            #print("Auction: Notifying Winner Agent ID   "+ str(element[0].id) +  " For Bundle " + element[1].name)
            element[0].recv_win_notification(self.price_list,element[1],self)
        
        
        

    def notify_loosers(self):#notify all agents who lost the round
        for element in self.looser_list:
            #print("Auction: Notifying Looser Agent ID :   "+ str(element[0].id) + " for Bundle " +  element[1].name )
            element[0].recv_loss_notification(self.price_list,element[1],self)
        
        
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
            print_str += ">>>B[ " + bundle.name + " ] P: " + str(self.price_list[bundle])+"<<<|"
        print(print_str)
        
    def print_agents_bid_list(self):
        print_str="AUCTION RECIEVED BIDS:"
        for agent_it in self.agents_bid_list:
            print_str+=">AG-ID " + str(agent_it.id) + "Bid " +str(self.agents_bid_list[agent_it][0][1]) +" for B["+str(self.agents_bid_list[agent_it][0][0].name)+"]<|"
        print (print_str)            
