from tkinter import *
#import I_Bundle_Agent as agent
from I_Bundle_Agent import Agent
import I_Bundle_Auction as auction

from I_Bundle_Simulation import Bundle
import tkinter as tk
import I_Bundle_Simulation as simulation
#for agent in Agent.instances:

#for manager in Encp_manager.instances

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #agent_count = Agent.id_counter
       # bundle_count = simulation.Bundle.id_counter
 #       print("renderer, agent Count = " + str(agent_count) + "Bundle_Count" + str(bundle_count))
#        print("Row Count " + str(simulation.Bundle.id_counter+ Agent.id_counter+3))
        t = SimpleTable(self, 10,simulation.Bundle.id_counter+ Agent.id_counter+3)#
        t.pack(side="top", fill="x")
#
class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        
        self.render_head()
#        self.render_bids()
        #TODO self.render_manager_decision
        
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)


#generate head row
    def render_head(self):
        #generate Iter Num
        current_row = []
        label = tk.Label(self,text="Iter",borderwidth=10, width=10)
        label.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        current_row.append(label)
        
        col = 1
        #GEN Bundle Heading
        for bundle in Bundle.instances:
            print("adding bundle")
            label = tk.Label(self,text="B: : " + str(bundle.name),borderwidth=10, width=10)
            label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
            col += 1
            current_row.append(label)
        
        self._widgets.append(current_row)

        #GEN Agent Heading
        for agent_it in Agent.instances:
            label = tk.Label(self,text="AG-ID: " + str(agent_it.id),borderwidth=10, width=15)
            label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
            col += 1
            current_row.append(label)
        
        self._widgets.append(current_row)


        current_row = []
        label = tk.Label(self,text="Winner:",borderwidth=10, width=25)
        label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
        current_row.append(label)
        col+=1
        self._widgets.append(current_row)
    
        current_row = []
        label = tk.Label(self,text="Erlös:",borderwidth=10, width=25)
        label.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
        current_row.append(label)
        col+=1
        self._widgets.append(current_row)
    

    def update_GUI(self):#todo, maybe auctioneer gives all parameter
        #uodate a row, after an Agent Decided on WHO won Auction
        1+1
init_world()

app = ExampleApp()


app.mainloop()
