import numpy as np
import math
import copy
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
        self.agents_bid_list = {}# dictonary with key= Agent, Value is the bid list from that agent
        self.init_price_list()
        self.bids_recieved = 0 
        self.epsilon = epsilon # by how much do we increase prices 
        self.iteration = 0
        

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
        self.agents_bid_list[agent] = bid_list# for Every Agent entry in DIct, there is a List of his XOR bids
        print("AUCTION: Recieved bid "+ str(bid_list[0][0].name) + "from agent" + str(agent.id) + "for price" + str(bid_list[0][1]))

        if self.bids_recieved == len(self.agent_list):
            input("Iteration:"+ str(self.iteration)+"--------------------ALL bids Recieved, Evalute them? ---------------------------------")
            self.iteration +=1
  
            self.bids_recieved= 0
            #print("Auction: recieved all bids , deciding on winner....")
            self.find_revenue_maximizing_distribution()
            self.calculate_new_price_list()
            print("AFTER CALC ne wPrice, NEW PRICE LIST ISSS :::")
            self.print_price_list()
      
            self.notify_loosers()
            self.notify_winners()
           
            
            
    def calculate_new_price_list(self):#copy Old list, increase the price for each Bundle by epsilon
        for element in self.looser_list:
            print("Auction: increasing bundle [: "+ element[1].name + "] by " + str(self.epsilon))
            self.price_list[element[1]] +=self.epsilon# the bundle, the agent wanted to win
        self.print_price_list()
        
        
        

        
 #    def recv_win_notification(self,new_bundle_price_list,bundle_won,auctioneer):#Notify API for Auctioneer, to tell Agent he won
       
    def notify_winners(self):#notify all agents, wo who the round
        for element in self.winner_list:
            print("WINNER IS : [: "+ str(element[0].id) +  "] for Agent " + element[1].name)
            element[0].recv_win_notification(self.price_list,element[1],self)
        
        
        

    def notify_loosers(self):#notify all agents who lost the round
        for element in self.winner_list:
            print("LOOSER IS : [: "+ str(element[0].id) + "] for Bundle " +  element[1].name )
            element[0].recv_loss_notification(self.price_list,element[1],self)
        
        
    def type_bundles(self):
        for bundle in self.bundle_list:
            self.type_bundle[bundle.type]
            
            
    def find_revenue_maximizing_distribution(self):
        #calc all possible combinations, check  revenue for all and pick most profitable and distribute evenly
        win_list = []
        first_agent = self.agent_list[0]
        highest_bidder = [self.agent_list[0], 0] #highest bidding agent and bid
        updated = False
        bidcount = 1
        for agent in self.agent_list:
            agentbund = copy.copy(self.agents_bid_list[agent][0][0])
            agentbid = copy.copy(self.agents_bid_list[agent][0][1])
            if agentbid > highest_bidder[1]:
                highest_bidder[0]= agent
                highest_bidder[1] = agentbid
                win_list.append([agent, agentbund, agentbid])
                updated = True
        if not updated:
            win_list.append([first_agent, self.agents_bid_list[first_agent][0][0], self.agents_bid_list[first_agent][0][1]])
        i = 1 # winlistindex
        for agent in self.agent_list:
            not_in = True
            for a in range (i):
                if agent in win_list[a]:
                    not_in = False
            if not_in:
                agentbund = copy.copy(self.agents_bid_list[agent][0][0])
                agentbid = copy.copy(self.agents_bid_list[agent][0][1])
                if self.compatible(agentbund, win_list[0][1]):
                    win_list.append ([agent, agentbund, agentbid])
                    i +=1
        #loser list erstellung

        lo_list = copy.copy(self.agent_list)
        #print("DEBUG: PRE laenge von lo_list:" + str(len(lo_list)) + " länge von agent_list: " + str(len(self.agent_list)))
        for i in range(len(win_list)):
         #   print("to remove: " + str(win_list[i][0].id) + "lo_list length: " +str(len(lo_list)))
            lo_list.remove(win_list[i][0])
        #print("DEBUG: after first loop, laenge von lo_list:" + str(len(lo_list)) + " länge von agent_list: " + str(len(self.agent_list)))
        for i in range(len(lo_list)):
            loagent = lo_list[i]
            #loser Agent wir mit [loser agent, sein bundle] ersetzt
            #print("loser agent print bundle: " + str(self.agents_bid_list[loagent][0][0].name))
            lo_list[i] = [loagent, self.agents_bid_list[loagent][0][0]]
        #print function
        #for i in range(len(win_list)):
          #  print ("Winner: Agent ID: " + str(win_list[i][0].id) + " with bundle: " + str(win_list[i][1].name))
       # for i in range (len(lo_list)):
           # print("Loser: Agent ID: " + str(lo_list[i][0].id)  + " with bundle: " + lo_list[i][1].name)


        self.looser_list = lo_list
        self.winner_list = win_list

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

    def update_price_list(self):
        pass
    def find_winner(self):
        for bundle in self.bundle_list:
            print("bundle: " +  bundle.name)

    def compatible(self, b1, b2):
        if (b1.jobs in b2.jobs) | (b2.jobs in b1.jobs) |(b1.type == b2.type):
            return False
        else: return True

    def print_price_list(self):
        for bundle in self.price_list:
            print("Auction: Price for Bundle[ " + bundle.name + " ] is " + str(self.price_list[bundle]))
