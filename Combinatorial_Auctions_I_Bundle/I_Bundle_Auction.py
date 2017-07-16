
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
        self.init_price_list()
        
        

    def start_auction(self):
        
        self.advertise_bundles()#start by sending all agent pricelist
        
 
    def advertise_bundles(self):
        for agent in self.agent_list:
            agent.recv_price_list(self.price_list,self)
        
        

       
    def hello_auction(self):
        print("Hello from Auction!")
        

    def recv_bid_list(x,bid_list,agent):
        #recviece the bids of an agent
        print("AUCTION: Recieved bid "+ str(bid_list[0].name) + "from agent" + str(x.id))
        
  

    def find_
      
        
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
