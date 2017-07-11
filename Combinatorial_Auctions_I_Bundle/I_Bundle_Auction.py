
import numpy as np
import math
#import encp_agent as agent
from I_Bundle_Agent import Agent

class Auction():
    instances = []
    id_counter = 0

    def __init__(self, x, k, p):
        self.id = Auction.id_counter
        self.location = x
        self.max_capacity = k
        self.preferences = p
        Auction.instances.append(self)
        Auction.id_counter += 1
   


    def hello_auction(self):
        print("Hello from Auction!")


