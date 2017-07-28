from I_Bundle_Auction import Auction
import math


class Agent():
    instances = []
    id_counter = 0
    
#
    def __init__(self, x, k,bid_count):
        #V is the use vector for each bundle
        self.id = Agent.id_counter
        self.location = x
        self.max_capacity = k
        Agent.instances.append(self)
        Agent.id_counter += 1
        self.use_vector = {}#Key= Bundle, Value  = Use For That Bunlde (Bundle_Value - (Bundle Price+bundle_travel_distance))
        self.distance_vector = {}# A Dictonary with Keys = bundles, Value is Distance Agent has to Travel to Pick up all Jobs in that Bundle
        self.won_last_auction =False #implies if won last auction
        self.distance_vector_calculated= False 
        self.bid_count= bid_count#how many bids will the agent send max
        self.bid_vector = []#list of bids the agent is intrested to send
        self.price_list_debug = ""
    def hello_agent(self):
        print("Hello from Agent!")
        
        
    def recv_price_list(self,new_bundle_price_list,auctioneer):
        #recieve a new price list and formulate a new bid if possible or do nothing
        self.auctioneer = auctioneer
        if self.won_last_auction == True:
            self.repeat_bid()#todo
       # print("recieved new price list!")
        if self.distance_vector_calculated == False :
            self.calculate_distance_vector(new_bundle_price_list)

        self.price_list_debug = new_bundle_price_list
        self.update_use_vector(new_bundle_price_list)
        #print("AG-ID:" +str(self.id) + " updated Use Vector to " + self.print_use_vector())        
        self.update_bid_vector(new_bundle_price_list)
        print("AG-ID:" +str(self.id) +"Sending bid for bundle:[" + str(self.bid_vector[0][0].name) + "] and for bid " +str (self.bid_vector[0][1]) +" and Use " + str(self.use_vector[self.bid_vector[0][0]]))
        #print("DEBUG: should be " + str (new_bundle_price_list[self.bid_vector[0][0]]))
        #print("and bid Vector is : " + str(self.print_bid_vector()))
        self.auctioneer.recv_bid_list(self, self.bid_vector)
        #self.send_bid_list(self, bid_list)#TODO if there are no Profitable bids, send Stop bidding Signal to aucitoneer

    def recv_win_notification(self,new_bundle_price_list,bundle_won,auctioneer):#Notify API for Auctioneer, to tell Agent he won
        self.won_last_auction = True    
        self.repeat_bid()#repeat last bid, dont update anything
        

    def recv_loss_notification(self,new_bundle_price_list,bundle_lost, auctioneer):#Notify API for Auctioneer, to tell Agent he lost
        self.won_last_auction = False
        self.recv_price_list(new_bundle_price_list,auctioneer)
       

    def repeat_bid(self ):
        print("AG-ID:" +str(self.id) +"Sending REPEATED bid for bundle:[" + str(self.bid_vector[0][0].name) + "] and for bid " +str (self.bid_vector[0][1]) +" and NOT UPDATED Use " + str(self.use_vector[self.bid_vector[0][0]]))
        self.auctioneer.recv_bid_list(self, self.bid_vector,)

        
            


    def update_bid_vector(self,price_list):
        bid_list = []#list of most profitable bundles, [0] most profitable,[1] 2nd most profitable
        best_use = [0,"default"]# set to 0, if we only want to bid on things with profit >1, second element is the the bundle  or maybe -(math.inf)
        ret_dict = {}
        for i in range(self.bid_count):# how many bids to calculate, is described by i
            for bundle in self.use_vector:
                if self.use_vector[bundle] > best_use[0] and bundle not in bid_list:
                    best_use[0] = self.use_vector[bundle]
                    best_use[1] = bundle
           # print("AG-ID:" +str(self.id) +"DEBUG: DECIDED ON BIDDING : " + str(self.price_list_debug[ best_use[1]])+ " for bundle" + str(best_use[1].name))
           Bid(self,best_use[1],self.price_list_debug[ best_use[1]]) 
           bid_list.append([best_use[1], self.price_list_debug[ best_use[1]]])#apending bid element , first ele is Bundle, second one is bid price
            
            self.bid_vector = bid_list
           # print("Calc best bundle : " + str(self.bid_vector[0][0].name) + "and for bid " +str (self.bid_vector[0][1]) +"and Use " + str(self.use_vector[self.bid_vector[0][0]]))
            #ret_dict[bundle] = price_list[bundle]

    def calculate_distance_vector(self,bundle_price_list):
        for bundle in bundle_price_list:
            #print("AG-ID:" +str(self.id) + "update use Vector for bundle:" + bundle.name)
            self.distance_vector[bundle]=self.calc_bundle_distance(bundle)
        self.distance_vector_calculated = True
        

    def print_use_vector(self):
        print_string =""
        for bundle in self.use_vector:#key are bundles
            print_string+= str(bundle.name) + " U: " + str(self.use_vector[bundle] )+ "|"#values are the calculated Use Value for that key/bunde
        return print_string

    def print_best_use(self):
        print_string =""
        for bundle in self.use_vector:#key are bundles
            print_string+= str(bundle.name) 
            break
        return print_string



    def print_bid_vector(self):
        print_string =""
        for bundle in self.use_vector:#key are bundles
            print_string+="THIS FUNCTION IS BUGGY FIX ME!!!"+ str(bundle.name) + " U: " + str(self.use_vector[bundle] )+ "|"#values are the calculated Use Value for that key/bunde
        return print_string



    def print_distance_vector(self):
        print_string =""
        for bundle in self.distance_vector:#key are bundles
            print_string+= str(bundle.name) + " Distance: " + str(self.distance_vector[bundle] )+ "|"#values are the calculated Use Value for that key/bunde
        return print_string





    def update_use_vector(self,bundle_price_list):#U, NutzenVektor für den Agenten, wenn er ein Bundle zum gegeben Preis kauft, update use Vector für neue Preise
                         #TODO  Bundle Value - Distance To Bundle 
        for bundle in bundle_price_list:
            self.use_vector[bundle] = int(bundle.b_value) - (bundle_price_list[bundle] + self.distance_vector[bundle]) # wertschötzung eines bundles = bundleWert - (distanz + preis)


    def calc_bundle_distance(self,bundle_new):
        #calculate distance from angent, to locaiton 1 +  location 1 to location 2 + location n to locaiton n+1|||||  and maybe back also later..
        result = 0
#        print("bundle [0 ] is + "+ str(bundle_new.jobs[0].location)+ "self loc is"+ str(self.location))
        result += self.calculate_distance(self.location,bundle_new.jobs[0].location)
        if len(bundle_new.jobs)== 1: 
            # there is only 1 Location, calculate Distance from Agent to that locaiton
              return result
        
        i = 0
        for location in bundle_new.jobs:
            #calculate distance fron First to Sencond, Second to Third  etc
            if(i+1 < len(bundle_new.jobs)):
                #print("AG-ID:" +str(self.id) + "Result was " + str(result) + "now is")
                result += self.calculate_distance(bundle_new.jobs[i].location,bundle_new.jobs[i+1].location)
            i+=1
        return result
        
  
    
    
    def calculate_distance(self,a,b):
        # calculate using  |x1-x2| + |y1-y2| , for location a to location b (tuples (x,y))
        dist = abs(a[0] - b[0] )+ abs(a[1] -b[1])
        return dist
    
    def print_price_list(self):
        print_str= "AG-ID:" +str(self.id) +"Agent Pricelist is:: Prices are: "
        for bundle in self.price_list_debug:
            print_str += "Bundle[ " + bundle.name + " ] Price: " + str(self.price_list_debug[bundle])+"|"
        print(print_str)
        
        


class Bid():
    instances = []
    id_counter = 0
    def __init__(self, agent, bundle, value):
        self.id = Bid.id_counter
        self.agent = agent
        self.bundle = bundle
        self.value = value
        self.combo=false
        agent.bids.append(self)
        Bid.id_counter +=1
        Bid.instances.append(self)

    def __str__(self):

        ret = "Agent ID: " + str(self.agent.id) + " wants: " + self.bundle.name + " for " + str(self.value)
        return (ret)

    __repr__ = __str__
