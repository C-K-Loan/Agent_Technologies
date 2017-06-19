from tkinter import *
import encp_agent as agent
from encp_agent import Agent
import encp_manager as manager
from encp_manager import Encp_manager
import tkinter as tk
#from encp_simulation import init_world

#for agent in Agent.instances:

#for manager in Encp_manager.instances

class Encp_animation(tk.Tk,):
    def __init__(self,):
        tk.Tk.__init__(self)
        agent_count = Agent.id_counter
        for manager_it in Encp_manager.instances :
            table = Encp_table(self,10,agent_count+2,manager_it) 
            table.pack(side="top", fill="x")

    def update_bids(self):
        for table in Encp_table.instances:
            table.render_bids()
 
    def update_def_bids(self):
        for table in Encp_table.instances:
            table.render_def_bids()
        
    def update_reactions(self):
        for table in Encp_table.instances:
            table.render_reactions()
        



#   
class Encp_table(tk.Frame):

    instances = []
    id_counter = 0

    def __init__(self, parent, rows, columns,manager_to_render):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        self.manager_to_render = manager_to_render
        Encp_table.instances.append(self)
        self.id = manager_to_render.id
        self.rows_rendered=0        
        self.render_head()
        self.iteration = 0
        #self.render_bids()
        #TODO self.render_manager_decision
        
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
        


#generate head row
    def render_head(self):
        #generate "ITERATION" head col
        current_row = []
        label = tk.Label(self,text="Iteration",borderwidth=10, width=25)
        label.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        current_row.append(label)
        
        #generate for each Agent a col
        for agent_it in Agent.instances:
            label = tk.Label(self,text="AGENT ID: " + str(agent_it.id)+ " Location:"+str(agent_it.location),borderwidth=10, width=25)
            label.grid(row=0, column=agent_it.id+1, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
        
        
        #generate for Manager a Col
        self._widgets.append(current_row)
        current_row = []
        print("MANAGER TO RENDER_"+str(self.manager_to_render))
        label = tk.Label(self,text="ENCP MANAGER ID: "+str(self.manager_to_render.id)+" Location:"+str(self.manager_to_render.x),borderwidth=10, width=25)
        label.grid(row=self.rows_rendered, column=Agent.id_counter+2, sticky="nsew", padx=1, pady=1)
        current_row.append(label)
        self._widgets.append(current_row)
        self.rows_rendered+=1
        

#generate one row, except encp reacitons
#generate all the bids
    def render_bids(self):

        # Dictionary for Key:Agent Value:Tuple (BID,ID of agent)
        #fill rows >0 with bid values and reaction of encp manager
    
        current_row = []
        
        self.render_iteration_num()

        for agent_it in self.manager_to_render.bids:
            print(str(self.manager_to_render.bids[agent_it]))
            label = tk.Label(self,text="Pre Bid: "+ str(self.manager_to_render.bids[agent_it][0]),borderwidth=10, width=25)
            label.grid(row=self.rows_rendered, column=agent_it.id+1, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
        #self.rows_rendered+=1
        self.iteration+=1
        self._widgets.append(current_row)

#dosent take care of increasing the iteration number
    def render_iteration_num(self):
        current_row = []
        #self.rows_rendered+=1
            #iteration num
        label_it_num = tk.Label(self,text="#"+ str(self.iteration),borderwidth=10, width=25)
        label_it_num.grid(row=self.rows_rendered, column=0, sticky="nsew", padx=1, pady=1)
        current_row.append(label_it_num)
         

    def render_def_bids(self):

        # Dictionary for Key:Agent Value:Tuple (BID,ID of agent)
        #fill rows >0 with bid values and reaction of encp manager
    
        current_row = []
    
        self.render_iteration_num()
        for agent_it in self.manager_to_render.bids:
            print(str(self.manager_to_render.bids[agent_it]))
            label = tk.Label(self,text="Pre Bid: "+ str(self.manager_to_render.bids[agent_it][0]),borderwidth=10, width=25)
            label.grid(row=self.rows_rendered, column=agent_it.id+1, sticky="nsew", padx=1, pady=1)
            current_row.append(label)

#        self.rows_rendered+=1
        self._widgets.append(current_row)
        self.iteration+=1
#make empty row
    def render_phase_reset(self):
        current_row = []
    
        self.render_iteration_num()
        for agent_it in self.manager_to_render.bids:
            print(str(self.manager_to_render.bids[agent_it]))
            label = tk.Label(self,text="PHASE RESET TO 1 : "+ str(self.manager_to_render.bids[agent_it][0]),borderwidth=10, width=25)
            label.grid(row=self.rows_rendered, column=agent_it.id+1, sticky="nsew", padx=1, pady=1)
            current_row.append(label)

#        self.rows_rendered+=1
        self._widgets.append(current_row)
        

    def render_reactions(self):
        render_string=""
        current_row = []

        for agent_it in self.manager_to_render.last_reaction_to_manager:
                render_string +="|"+self.manager_to_render.last_reaction_to_manager[agent_it]
        if render_string == "":
            render_string="NO REACTIONS YET SEND"            
            
        label = tk.Label(self,text=render_string,borderwidth=10, width=100)
        label.grid(row=self.rows_rendered, column=Agent.id_counter+2, sticky="nsew", padx=1, pady=1)
        current_row.append(label)
            
        self.rows_rendered+=1

    #render the decision of manager in top right coorner for is col and iteration num
    def render_manager_decision(self,decision_type,value,was_was_resett):

        
#        if decision_type =="pre_acc":
 #       if decision_type =="pre_rej":
  #      if decision_type =="def_acc":
   #     if decision_type =="def_acc":


            
        
        #TODO
        x=1


"""
init_world(h,w)
agent_count = Agent.id_counter
#print("ID COUNTER IS "+ str(agent_count))
app = ExampleApp()
app.mainloop()
"""
