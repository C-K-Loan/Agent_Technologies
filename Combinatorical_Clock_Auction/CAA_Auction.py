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
        self.sealed_bid_phase()


    def sealed_bid_phase(self):
        agents_bid_dict = {}
        print("Sealed Bid Phase: ")
        self.agents_done = 2
        for agent in self.agent_list:
            pass #agent.final_bids(self)
        while self.agents_done != len(self.agent_list):
            print("LOOOL NOT DONE YET")
        for agent in self.agent_list:
            for bundle in agent.own_prices:
                agents_bid_dict[Agent] = (bundle, agent.own_prices[bundle])

        #revenue
        #combos hast bundlelist and price
        bundle_winner = {}
        combos = []
        best_sum = 0
        for a in self.agent_list:
            for abundle in a.own_prices:
                #sum = a.own_prices[abundle] -1
                #if a.own_prices[abundle] > best_sum:
                    #combos.append(([abundle, a], sum))
                    #best_sum = sum
                    for b in self.agent_list:
                        if a != b:
                            for bbundle in b.own_prices:

                                if abundle.compatible(bbundle):

                                    sum = a.own_prices[abundle] + b.own_prices[bbundle] - 2
                                    if sum > best_sum:
                                        combos.append(([abundle,a,bbundle,b], sum))
                                        best_sum = sum
                                    for c in self.agent_list:
                                        if c != a and c != b:
                                            for cbundle in c.own_prices:
                                                if abundle.compatible(cbundle) and bbundle.compatible(cbundle):
                                                    sum = a.own_prices[abundle] + b.own_prices[bbundle] + b.own_prices[cbundle] - 3
                                                    if sum > best_sum:
                                                        combos.append(([abundle, a, bbundle, b, cbundle, c], sum))
                                                        best_sum = sum


        if len(combos[-1][0]) == 4:
            bundle_winner[combos[-1][0][0]] = combos[-1][0][1]
            bundle_winner[combos[-1][0][2]] = combos[-1][0][3]
            for b in bundle_winner:
                print("Agent " + str(bundle_winner[b].id) +  " won bundle " + b.name + " with price " +  str(bundle_winner[b].own_prices[b] -1) )
            print("summed cost" + str(combos[-1][1]))
        if len(combos[-1][0]) == 6:
            bundle_winner[combos[-1][0][0]] = combos[-1][0][1]
            bundle_winner[combos[-1][0][2]] = combos[-1][0][3]
            bundle_winner[combos[-1][0][4]] = combos[-1][0][5]
            for b in bundle_winner:
                print("Agent " + str(bundle_winner[b].id) +  " won bundle " + b.name + " with price " +  str(bundle_winner[b].own_prices[b] - 1) )
            print("summed cost: " + combos[-1][1])

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
    def print_agent_prices(self):
        for agent in self.agent_list:
            print(" Eligibility: " + str(agent.eligibility) + "   Prices for agent " +str(agent.id) + ":")
            for bundle in agent.own_prices:
                print("      " +bundle.name + " with Value " + str(agent.own_prices[bundle]))
    def chose_winners(self):
        for a in self.agent_list:
            a.print_bids()