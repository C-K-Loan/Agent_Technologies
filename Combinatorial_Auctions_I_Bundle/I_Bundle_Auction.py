
import numpy as np
import math
#from I_Bundle_Agent import Agent

class Auction():
    instances = []
    id_counter = 0

    def __init__(self, ):
        self.id = Auction.id_counter
        Auction.instances.append(self)
        Auction.id_counter += 1
   


    def hello_auction(self):
        print("Hello from Auction!")
        
    
    def recv_test_agent(self,test_agent):
        test_agent.hello_agent()


