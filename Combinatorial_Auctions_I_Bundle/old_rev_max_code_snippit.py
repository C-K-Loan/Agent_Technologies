        
"""        
        win_list = []
        first_agent = self.agent_list[0]
        highest_bidder = [self.agent_list[0], 0] #highest bidding agent and bid
        updated = False
        bidcount = 1
        for agent in self.agent_list:
            agentbund = copy.copy(self.agents_bid_list[agent][0][0])
            agentbid = copy.copy(self.agents_bid_list[agent][0][1])
            if agentbid > highest_bidder[1]:
                highest_bidder[0]= agent
                highest_bidder[1] = agentbid
                win_list.append([agent, agentbund, agentbid])
                updated = True
        
        if not updated:
            win_list.append([first_agent, self.agents_bid_list[first_agent][0][0], self.agents_bid_list[first_agent][0][1]])
        i = 1 # winlistindex
        print(">>>>DEBUG: DETECTED winner len: "+ str(len(win_list)))
        for agent in self.agent_list:#BUG, wir iterieren durch alle AGenten und nehmen deren gebote, aber wenn ein agent KEIN gebot schickt, wird trozdem sein altes benutzt!
            not_in = True
            for a in range (i):
                if agent in win_list[a]:
                    not_in = False
            if not_in:
                agentbund = copy.copy(self.agents_bid_list[agent][0][0])
                agentbid = copy.copy(self.agents_bid_list[agent][0][1])
                if self.compatible(agentbund, win_list[0][1]):
                    win_list.append ([agent, agentbund, agentbid])
                    i +=1
        #loser list erstellung

        lo_list = copy.copy(self.agent_list)
        #print("DEBUG: PRE laenge von lo_list:" + str(len(lo_list)) + " länge von agent_list: " + str(len(self.agent_list)))
        for i in range(len(win_list)):
         #   print("to remove: " + str(win_list[i][0].id) + "lo_list length: " +str(len(lo_list)))
             if win_list[i][0] in lo_list:
                 lo_list.remove(win_list[i][0])
        #print("DEBUG: after first loop, laenge von lo_list:" + str(len(lo_list)) + " länge von agent_list: " + str(len(self.agent_list)))
        for i in range(len(lo_list)):
            loagent = lo_list[i]
            #loser Agent wir mit [loser agent, sein bundle] ersetzt
            #print("loser agent print bundle: " + str(self.agents_bid_list[loagent][0][0].name))
            lo_list[i] = [loagent, self.agents_bid_list[loagent][0][0]]
        #print function
        for i in range(len(win_list)):
            print ("Winner: Agent ID: " + str(win_list[i][0].id) + " with bundle: [" + str(win_list[i][1].name)+ "] and bid :" +str(self.agents_bid_list[win_list[i][0]][0][1])+"and lo liist len + " +str(len(lo_list)))
        for i in range (len(lo_list)):
            print("Loser: Agent ID: " + str(lo_list[i][0].id)  + " with bundle: [" + lo_list[i][1].name+ "] and bid :" +str(self.agents_bid_list[lo_list[i][0]][0][1]))


        self.looser_list = lo_list
        self.winner_list = win_list
"""
