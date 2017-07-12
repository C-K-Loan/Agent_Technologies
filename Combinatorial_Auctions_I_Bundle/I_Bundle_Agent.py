from I_Bundle_Auction import Auction

class Agent():
    instances = []
    id_counter = 0

    def __init__(self, x, k, p, v):
        #V is the use vector for each bundle
        self.id = Agent.id_counter
        self.location = x
        self.max_capacity = k
        self.preferences = p
        Agent.instances.append(self)
        Agent.id_counter += 1
        self.won_last_auction=false #implies if won last auction


    def hello_agent(self):
        print("Hello from Agent!")
        
        
    #recieve a new price list and formulate a new bid if possible or do nothing
    def recv_price_list(new_price_list):
        if self.won_last_auction:
            1+1#repeat old bild
        
        else:#calculate new bid
        #TODO
        
        
    def calc_evaluation(price_list):
        #todo
       #aka V Wertschätzung des Agenten

        
        
    def calc_bid(price_list):      
        #B , Gebote eines Agenten, zu einem Gegebenen Bundle Vektor
        #todo
        
        
    def calc_use:(price_list):
        #todo
        #U, NutzenVektor für den Agenten, wenn er ein Bundle zum gegeben Preis kauft
