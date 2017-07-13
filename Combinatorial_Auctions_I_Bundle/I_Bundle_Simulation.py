

import numpy as np
import math
from I_Bundle_Agent import Agent
from I_Bundle_Auction import Auction






#A bundle Containing a quantity of locations/Jobs, all of one Type  
#@param bundle_type, type of bundle
#@param locations, the locations for this bundke
#@param value, the value of this bundle
class Bundle():
    instances = []
    id_counter = 0

    def __init__(self, name, bundle_type,jobs):
        self.id = Bundle.id_counter
        self.jobs = jobs
        self.name = name
        self.calc_and_set_bundle_value()
        self.type = bundle_type  
        Bundle.instances.append(self)
        Bundle.id_counter += 1
        
    def calc_and_set_bundle_value(self):
        value = 0
        for job in self.jobs:
            value += int(job.value)
        self.value=job    
        
   
    
class Job():
    instances = []
    id_counter = 0

    def __init__(self, location, value, job_type):
        self.type = job_type
        self.id = Job.id_counter
        self.location = location
        self.value = value
        Job.instances.append(self)
        Job.id_counter += 1
   
    
    












#initialize all objects
def init_world():
    #location, Capacity    
    test_agent0= Agent((0,0),1)


    test_auction0= Auction()#he manager likes 0 >1

    test_agent0.hello_agent()
    test_auction0.hello_auction()
    test_auction0.recv_test_agent(test_agent0)

    #job Location, Value, type
    cat0 = Job((0,4),10,"Cat")
    cat1 = Job((1,3),10,"Cat")
    dog0 = Job((4,0),10,"Dog")

    #bundle Name, type, Jobs in bundle
    bundle_0 = Bundle( "Cat 0","Cat",[cat0])
    bundle_1 = Bundle( "Cat 1","Cat",[cat1])
    bundle_2 = Bundle( "Cat 0 and Cat 1","Cat",[cat0,cat1])
    bundle_3 = Bundle( "dog0","Dog",[dog0])



    bundle_list = [bundle_0,bundle_1,bundle_2,bundle_3]
    print_bundle(bundle_list)

def print_bundle(bundle_list):
    for bundle in bundle_list:
        bundle_str = str(bundle.name)
        
        for job in bundle.jobs:
            print ("Bundle : " + bundle_str + str(job.location ))


init_world()
