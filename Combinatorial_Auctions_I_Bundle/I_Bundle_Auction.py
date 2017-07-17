
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
        

    def recv_bid_list(self, agent,bid_list):
        self.bids_recieved += 1 
        #recviece the bids of an agent and safe the bids until we have all bids recieved or Timeout
        self.agents_bid_list[agent] = bid_list# for Every Agent entry in DIct, there is a List of his XOR bids
        print("AUCTION: Recieved bid "+ str(bid_list[0][0].name) + "from agent" + str(agent.id) + "for price" + str(bid_list[0][1]))
        if self.bids_recieved == len(self.agent_list):
            print("recieved all bids , decidin..")
            self.find_revenue_maximizing_distribution()

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
            agentbund = self.agents_bid_list[agent][0][0]
            agentbid = self.agents_bid_list[agent][0][1]
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
                agentbund = self.agents_bid_list[agent][0][0]
                agentbid = self.agents_bid_list[agent][0][1]
                if self.compatible(agentbund, win_list[0][1]):
                    win_list.append ([agent, agentbund, agentbid])
                    i +=1
        #loser list erstellung
        lo_list = self.agent_list
        for i in range(len(win_list)):
            lo_list.remove(win_list[i][0])
        for i in range(len(lo_list)):
            loagent = lo_list[i]
            #loser Agent wir mit [loser agent, sein bundle] ersetzt
            print("loser agent print bundle: " + str(self.agents_bid_list[loagent][0][0].name))
            lo_list[i] = [loagent, self.agents_bid_list[loagent][0][0]]
        #print function
        for i in range(len(win_list)):
            print ("Winner: Agent ID: " + str(win_list[i][0].id) + " with bundle: " + str(win_list[i][1].name))
        for i in range (len(lo_list)):
            print("Loser: Agent ID: " + str(lo_list[i][0].id)  + " with bundle: " + lo_list[i][1].name)


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

    def create_subsets(self, bid_list):
        #alle möglichen kombinationen rausfinden und dann die kicken, die nicht kompatibel sind.
        bcomb = []

        pass
