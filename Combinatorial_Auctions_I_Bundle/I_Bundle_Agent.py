#import I_Bundle_Auction.py

class Agent():
    instances = []
    id_counter = 0

    def __init__(self, x, k, p):
        self.id = Agent.id_counter
        self.location = x
        self.max_capacity = k
        self.preferences = p
        Agent.instances.append(self)
        Agent.id_counter += 1
   


    def hello_agent(self):
        print("Hello from Agent!")