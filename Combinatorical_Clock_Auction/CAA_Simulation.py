import numpy as np
import math
from CAA_Agent import Agent
from CAA_Auction import Auction


# import I_Bundle_Render as render





class Bundle():
    # A bundle Containing a quantity of locations/Jobs, all of one Type
    # @param bundle_type, type of bundle,@param locations, the locations for this bundke,@param value, the value of this bundle

    instances = []
    id_counter = 0

    def __init__(self, name, bundle_type, jobs):
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

    def __str__(self):
        bundle_str = "Bundle : " + str(self.name) + "\n"
        for job in self.jobs:
            bundle_str += "job_id: " + str(job.id) + " location: " + str(job.location) + " + "
        bundle_str = bundle_str[:-3]
        return bundle_str

    __repr__ = __str__

class Job():
    # location in the World, with value and Type
    instances = []
    id_counter = 0

    def __init__(self, location, value, job_type):
        self.type = job_type
        #self.name = name
        self.id = Job.id_counter
        self.location = location
        self.value = value
        Job.instances.append(self)
        Job.id_counter += 1


# initialize all objects
def init_world():
    # location, Capacity
    agent_1 = Agent((0, 0), 3, 3)
    agent_2 = Agent((5, 5), 3, 3)
    agent_3 = Agent((4, 5), 3, 3)

    # job Location, Value,
    gut_0 = Job((2, 2), 5, "Cat")
    gut_1 = Job((2, 2), 5, "Cat")
    gut_2 = Job((3, 3), 5, "Cat")
    gut_3 = Job((3, 3), 5, "Cat")
    dog0 = Job((5, 5), 0, "Dog")

    # bundle Name, type, Jobs in bundle
    bundle_0 = Bundle("gut 1", "Cat", [gut_1])
    bundle_1 = Bundle("gut 2", "Cat", [gut_2])
    bundle_2 = Bundle("gut 1 und 2", "Cat", [gut_1, gut_2])
    bundle_3 = Bundle("gut dog0", "Dog", [dog0])#
    bundle_4 = Bundle("gut 0 und 1", "Cat", [gut_1, gut_0])
    bundle_5 = Bundle("gut 2 und 3", "Cat", [gut_2, gut_3])
    bundle_6 = Bundle("gut 0", "Cat", [gut_0])
    bundle_7 = Bundle("gut 3", "Cat", [gut_3])


    bundle_list = [bundle_0, bundle_1, bundle_2, bundle_3, bundle_4, bundle_5, bundle_6, bundle_7]
    agent_list = [agent_1, agent_2]
    auction = Auction(bundle_list, agent_list, 1)
    auction.start_auction()



init_world()