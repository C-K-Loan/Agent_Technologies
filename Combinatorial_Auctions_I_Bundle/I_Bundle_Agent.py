from I_Bundle_Auction import Auction

class Agent():
    instances = []
    id_counter = 0
    
#
    def __init__(self, x, k,):
        #V is the use vector for each bundle
        self.id = Agent.id_counter
        self.location = x
        self.max_capacity = k
        Agent.instances.append(self)
        Agent.id_counter += 1
        self.use_vector = {}#Key= Bundle, Value  = Use For That Bunlde (Bundle_Value - (Bundle Price+bundle_travel_distance))
        self.distance_vector = {}# A Dictonary with Keys = bundles, Value is Distance Agent has to Travel to Pick up all Jobs in that Bundle
        self.won_last_auction=False #implies if won last auction
        self.distance_vector_calculated= False 

    def hello_agent(self):
        print("Hello from Agent!")
        
        
    def recv_price_list(self,new_bundle_price_list):
        #recieve a new price list and formulate a new bid if possible or do nothing
        
        print("recieved price list!")
        if self.distance_vector_calculated == False :
            
            self.calculate_distance_vector(new_bundle_price_list)
        print("AG-ID:" +str(self.id) + " updated Distance Vector to " + self.print_distance_vector())


        self.update_use_vecotr(new_bundle_price_list)
        print("AG-ID:" +str(self.id) + " updated Use Vector to " + self.print_use_vector())        
        
        #print(str(new_price_list))
        #for bundle in new_bundle_price_list:
        #    print("AG-ID:" +str(self.id) + "  Bundle ["+ str(bundle.name) +  "]and price " +str (new_bundle_price_list[bundle]))
        
        #self.update_use_vecotr(new_bundle_price_list)
 

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


    def print_distance_vector(self):
        print_string =""
        for bundle in self.distance_vector:#key are bundles
            print_string+= str(bundle.name) + " Distance: " + str(self.distance_vector[bundle] )+ "|"#values are the calculated Use Value for that key/bunde
        return print_string
        
    
    def calc_bid(self,bundle_price_list):  
        1+1
        #B , Gebote eines Agenten, zu einem Gegebenen Bundle Vektor
        
        
        
    def update_use_vecotr(self,bundle_price_list):#U, NutzenVektor für den Agenten, wenn er ein Bundle zum gegeben Preis kauft, update use Vector für neue Preise 
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
                print("AG-ID:" +str(self.id) + "Result was " + str(result) + "now is")
                result += self.calculate_distance(bundle_new.jobs[i].location,bundle_new.jobs[i+1].location)
            i+=1
            print(str(result))
        return result
        
      
    def calculate_distance(self,a,b):
        # calculate using  |x1-x2| + |y1-y2| , for location a to location b (tuples (x,y))
        dist = abs(a[0] - b[0] )+ abs(a[1] -b[1])
        return dist
    

