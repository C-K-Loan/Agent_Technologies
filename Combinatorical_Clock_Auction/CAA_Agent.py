import math
import collections
import copy

class Agent():
    instances = []
    id_counter = 1

    #
    def __init__(self, x, k, bid_count):
        # V is the use vector for each bundle
        self.id = Agent.id_counter
        self.location = x
        self.start_location = x
        self.capacity = k
        self.max_capacity = k
        self.bid_count = bid_count  # how many bids will the agent send max
        #Berechtigungspunkte
        self.eligibility = min(bid_count, 4) # min(eligibility,3))
        self.pref = {} # preferences
        self.use_vector = {}  # Key= Bundle, Value  = Use For That Bunlde (Bundle_Value - (Bundle Price+bundle_travel_distance))
        self.distance_vector = {}  # A Dictonary with Keys = bundles, Value is Distance Agent has to Travel to Pick up all Jobs in that Bundle
    #    self.won_last_auction = False  # implies if won last auction
    #    self.distance_vector_calculated = False
        self.own_prices = {}
        self.bids = []
        self.bid_vector = []
        self.bid_type = ""
        Agent.instances.append(self)
        Agent.id_counter += 1

    def get_prices(self, prices, auctioneer):
        # recieve a new price list and formulate a new bid if possible or do nothing
        self.auctioneer = auctioneer
        self.distance_vector = {}
        self.use_vector = {}
        self.capacity = self.max_capacity
       # print("juhu")

        #self.calculate_distance_vector(prices)
        #self.update_use_vector(prices)
        #print("AG-ID:" +str(self.id) + " updated Use Vector to " + self.print_use_vector())

        self.set_bids(prices)
        auctioneer.agents_done += 1
        return

    def calculate_distance_vector(self, prices):
            for bundle in prices:
                # print("AG-ID:" +str(self.id) + "update use Vector for bundle:" + bundle.name)
                self.distance_vector[bundle] = self.calc_bundle_distance(bundle)
            self.distance_vector_calculated = True

    def update_use_vector(self, prices):  # U, NutzenVektor für den Agenten, wenn er ein Bundle zum gegeben Preis kauft, update use Vector für neue Preise
            for bundle in prices:
                self.use_vector[bundle] = int(bundle.b_value) - (prices[bundle] + self.distance_vector[bundle])  # wertschötzung eines bundles = bundleWert - (distanz +
                if len(bundle.jobs) > self.capacity: #Kapazität beachten
                    self.use_vector[bundle] = -1000
                if self.bid_type != "":
                    if bundle.jobs[0].type != self.bid_type:
                        self.use_vector[bundle] = -1000


    def calc_bundle_distance(self, bundle_new):
        # calculate distance from angent, to locaiton 1 +  location 1 to location 2 + location n to locaiton n+1|||||  and maybe back also later..
        result = 0
        #        print("bundle [0 ] is + "+ str(bundle_new.jobs[0].location)+ "self loc is"+ str(self.location))
        result += self.calculate_distance(self.location, bundle_new.jobs[0].location)
        if len(bundle_new.jobs) == 1:
            # there is only 1 Location, calculate Distance from Agent to that locaiton
            return result

        i = 0
        for location in bundle_new.jobs:
            # calculate distance fron First to Sencond, Second to Third  etc
            if (i + 1 < len(bundle_new.jobs)):
                # print("AG-ID:" +str(self.id) + "Result was " + str(result) + "now is")
                result += self.calculate_distance(bundle_new.jobs[i].location, bundle_new.jobs[i + 1].location)
            i += 1
        return result
    def calculate_distance(self,a,b):
        # calculate using  |x1-x2| + |y1-y2| , for location a to location b (tuples (x,y))
        dist = abs(a[0] - b[0] )+ abs(a[1] -b[1])
        return dist
    def final_bids(self, auction):
        #generate XOR bids
        self.distance_vector = {}
        self.use_vector = {}
        self.capacity = self.max_capacity
        for bundle in self.own_prices:
            print("Auction: Price for Bundle[ " + bundle.name + " ] is " + str(self.own_prices[bundle]))
        print("another agent")
        prices_copy = copy.copy(self.own_prices)

        self.calculate_distance_vector(prices_copy)
        self.update_use_vector(prices_copy)

        sorted_uses = sorted(self.use_vector.items(), key=lambda x: x[1], reverse=True)
        #self.print_sorted_uses(sorted_uses)
        for i in range (len(sorted_uses)):
            if len(sorted_uses) < 1:
                break
            best_bundle = sorted_uses[i][0]
            best_use = sorted_uses[i][1]
            self.bid_type = best_bundle.jobs[0].type
            if best_use > 0:
                self.bids.append(Bid(self, best_bundle, prices_copy[best_bundle] ))


        auction.agents_done += 1
    def set_bids(self,prices):
        prices_copy = copy.copy(prices)
        self.calculate_distance_vector(prices_copy)
        self.update_use_vector(prices_copy)
        print("for Agent: " + str(self.id))
        for e in range (self.eligibility):
            sorted_uses = sorted(self.use_vector.items(), key=lambda x: x[1], reverse=True)  # usevektor absteigend nach use sortieren
            self.print_sorted_uses(sorted_uses)
            if len(sorted_uses) < 1:
                self.location = self.start_location
                return
            best_bundle = sorted_uses[0][0]
            #print("Best bundle: " + str(best_bundle))
            best_use = sorted_uses[0][1]
            self.bid_type = best_bundle.jobs[0].type
            if best_use > 0:
                Bid(self, best_bundle, prices[best_bundle])
                self.own_prices[best_bundle] = prices[best_bundle]
                self.update_location(best_bundle)
           #     print("updated location: " + str(self.location))

                #Remove unfitting bundles
                prices_copy.pop(best_bundle)
                if len(best_bundle.jobs) > 1:
                    for j in best_bundle.jobs:
                        for b in list(prices_copy):
                            if j in b.jobs:
                                prices_copy.pop(b)




                # for b in prices_copy:  # dict mit bundlepreisen
                #     if b.jobs[0].type != self.bid_type:
                #         prices_copy[b] = math.inf

           #     print(len(prices_copy))
                self.capacity -= len(best_bundle.jobs)
                self.distance_vector = {}
                self.use_vector = {}
                self.calculate_distance_vector(prices_copy)
                self.update_use_vector(prices_copy)
            else:
                print("ELIGIBILITY DECREASED")
                self.eligibility -= 1
                break
        self.bid_type = ""
        self.location = self.start_location
        #print (sorted_uses)
        #sorted_bundles = sorted(prices.items(), key=lambda x: x[1])

            #ret_dict[bundle] = price_list[bundle]
    def update_location(self, bundle):
        self.location = bundle.jobs[-1].location


    def print_sorted_uses(self, uses):
        ret = ""
        for use in uses:
            ret += str(use[0]) + ", USE: " + str(use[1]) + "\n"
            return print(ret)
    def print_use_vector(self):
        print_string =""
        for bundle in self.use_vector:#key are bundles
            print_string+= str(bundle.name) + " U: " + str(self.use_vector[bundle] )+ "|"#values are the calculated Use Value for that key/bunde
        return print_string
    def print_distance_vector(self):
        print_string =""
        for bundle in self.distance_vector:#key are bundles
            print_string+= str(bundle.name) + " Distance: " + str(self.distance_vector[bundle] )+ "|"#values are the calculated Use Value for that key/bunde
        return print_string
    def print_bids(self):
        for bid in self.bids:
            print("AGENT ID, BUNDLE, VALUE: "+ str(bid.agent.id) + ", " + bid.bundle.name + ", " + str(bid.value))
class Bid():
    instances = []
    id_counter = 0
    def __init__(self, agent, bundle, value):
        self.id = Bid.id_counter
        self.agent = agent
        self.bundle = bundle
        self.value = value
        agent.bids.append(self)
        Bid.id_counter +=1
        Bid.instances.append(self)

    def __str__(self):

        ret = "Agent ID: " + str(self.agent.id) + " wants: " + self.bundle.name + " for " + str(self.value)
        return (ret)

    __repr__ = __str__
