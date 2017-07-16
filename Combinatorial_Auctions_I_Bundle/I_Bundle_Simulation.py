

import numpy as np
import math
from I_Bundle_Agent import Agent
from I_Bundle_Auction import Auction
#import I_Bundle_Render as render





class Bundle():
#A bundle Containing a quantity of locations/Jobs, all of one Type  
#@param bundle_type, type of bundle,@param locations, the locations for this bundke,@param value, the value of this bundle

    instances = []
    id_counter = 0

    def __init__(self, name, bundle_type,jobs):
        self.id = Bundle.id_counter
        self.jobs = jobs
        self.name = name
        self.b_value = self.calc_and_set_bundle_value()
        self.type = bundle_type  
        Bundle.instances.append(self)
        Bundle.id_counter += 1
        
    def calc_and_set_bundle_value(self):
        value = 0
        for job in self.jobs:
            value += int(job.value)
        return value
   
    
class Job():
    #location in the World, with value and Type
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
    agent0= Agent((0,0),1,1) 
    agent1= Agent((6,0),1,1)
    agent2= Agent((1,5),1,1)
    
    
    #job Location, Value, type
    cat0 = Job((1,3),15,"Cat")
    cat1 = Job((2,2),10,"Cat")
    dog0 = Job((5,5),20,"Dog")

    #bundle Name, type, Jobs in bundle
    bundle_0 = Bundle( "Cat 0","Cat",[cat0])
    bundle_1 = Bundle( "Cat 1","Cat",[cat1])
    bundle_2 = Bundle( "Cat 0 and Cat 1","Cat",[cat0,cat1])
    bundle_3 = Bundle( "dog0","Dog",[dog0])



    bundle_list = [bundle_0,bundle_1,bundle_2,bundle_3]
    agent_list = [agent0,agent1,agent2]
    auction= Auction(bundle_list,agent_list)    
    auction.start_auction()
    
    
def print_bundle(bundle_list):
    for bundle in bundle_list:
        bundle_str = str(bundle.name)
        
        for job in bundle.jobs:
            print ("Bundle : " + bundle_str + str(job.location ))


init_world()
