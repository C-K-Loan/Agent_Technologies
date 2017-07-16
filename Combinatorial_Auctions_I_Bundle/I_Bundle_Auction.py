
import numpy as np
import math
#from I_Bundle_Agent import Agent

class Auction():
    instances = []
    id_counter = 0

    def __init__(self,bundle_list,agent_list ):
        self.id = Auction.id_counter
        self.agent_list = agent_list
        self.bundle_list = bundle_list
        Auction.instances.append(self)
        Auction.id_counter += 1
        self.agents_bid_list = {}# dictonary with key= Agent, Value is the bid list from that agent
        self.init_price_list()
        self.bids_recieved = 0 
        
        

    def start_auction(self):
        
        self.advertise_bundles()#start by sending all agent pricelist
        
 
    def advertise_bundles(self):
        for agent in self.agent_list:
            agent.recv_price_list(self.price_list,self)
        
        

       
    def hello_auction(self):
        print("Hello from Auction!")
        

    def recv_bid_list(agent,bid_list,self):
        self.bids_recieved += 1 
        #recviece the bids of an agent and safe the bids until we have all bids recieved or Timeout
        self.agents_bid_list[agent] = bid_list# for Every Agent entry in DIct, there is a List of his XOR bids
        print("AUCTION: Recieved bid "+ str(bid_list[0].name) + "from agent" + str(agent.id) + "for price" + str(self.price_list[bid_list[0]]))
        if self.bids_recieved == len(self.agent_list):
            print("recieved all bids , decidin..")
            
    def find_revenue_maximizing_distribution(self):
        #calc all possible combinations, check  revenue for all and pick most profitable and distribute evenly
        1+1



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
