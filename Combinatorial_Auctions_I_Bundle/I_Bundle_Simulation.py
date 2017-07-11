

import numpy as np
import math
from I_Bundle_Agent import Agent
from I_Bundle_Auction import Auction


test_agent0= Agent((0,0),1,[0,1,])#he manager likes 0 >1
test_auction0= Auction((0,0),1,[0,1,])#he manager likes 0 >1

test_agent0.hello_agent()
test_auction0.hello_auction()