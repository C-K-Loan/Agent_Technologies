import numpy as np
import math
import copy
from CAA_Agent import Agent, Bid

class Auction():
    instances = []
    id_counter = 0

    def __init__(self, bundle_list, agent_list, epsilon):
        self.id = Auction.id_counter
        self.agent_list = agent_list
        self.bundle_list = bundle_list
        Auction.instances.append(self)
        Auction.id_counter += 1
        self.agents_bid_list = {}  # dictonary with key= Agent, Value is the bid list from that agent
        self.bids_recieved = 0
        self.agents_done = 0
        self.epsilon = epsilon  # by how much do we increase prices
        self.prices = {} #dictionaty with key = bundle
        self.init_prices()
        self.iteration = 1

    def init_prices(self):
        #init all bundle prices to 0
        self.prices = {}
        for bundle in self.bundle_list:
            self.prices[bundle]= 0

    def start_auction(self):
        self.start_clock_phase()

        self.print_prices()


    def start_clock_phase(self):
        self.done = False
        while not self.done:
            print(" ITERATION: " + str(self.iteration))
            self.agents_done = 0
            self.advertise_bundles()  # start by sending all agent pricelist
            while self.agents_done != len(self.agent_list):
                print("LOOOL NOT DONE YET")
            self.print_agent_prices()
            self.iteration += 1
            if self.increase_prices():
                self.done = True
                return

            Bid.instances = []
    def advertise_bundles(self):
        for agent in self.agent_list:
            agent.get_prices(self.prices, self)

    def print_bids(self):
        for agent in self.agent_list:
            agent.print_bids()

    def increase_prices(self):
        if Bid.instances == []: #no price increase, Gleichgewicht
            return True
        increase = {}
        for bundle in self.bundle_list:
            increase[bundle] = False
        for bid in Bid.instances:
            if increase[bid.bundle] == False:
                self.prices[bid.bundle] += 1
            increase[bid.bundle] = True

    def print_prices(self):
        for bundle in self.prices:
            print("Auction: Price for Bundle[ " + bundle.name + " ] is " + str(self.prices[bundle]))
        #for bid in Bid.instances:
         #   print (str(bid.agent.id) + " won bundle " + bid.bundle.name)
    def print_agent_prices(self):
        for agent in self.agent_list:
            print("   Prices for agent " +str(agent.id) + ":")
            for bundle in agent.own_prices:
                print("      " +bundle.name + " with Value " + str(agent.own_prices[bundle]))