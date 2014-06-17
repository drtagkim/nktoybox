'''
isd_adapter_plan.py

NK Landscape Model
Modularity x ISD

Jungpil and Taekyung

2014
'''

import numpy as np
from algorithm import linear_uncertainty
from simulator import AdapterPlan
from isd_agent import AgileDeveloper, WaterfallDeveloper

class AdapterPlanISD(AdapterPlan):
    """
|  ISD Simulation plan
|  Parameters: simulator object, behavior class, agent clan, focused agent, target time run
    """
    def __init__(self, simulator, adapter_behavior, agent_clan, agent, tick_end):
        AdapterPlan.__init__(self,
                             simulator = simulator, 
                             adapter_behavior = adapter_behavior, 
                             agent_clan = agent_clan, 
                             agent = agent, 
                             tick_end = tick_end)
    def my_profile(cls):
        return "\nPlan for ISD Development Simulation\n"
    profile = classmethod(my_profile)
    def run(self):
        """
|  Run a simulator
|  This contains a core algorithm for managing the entire simulation
        """
        agent = self.agent #assing to local reference
        agent.tick_end = self.tick_end
        current_behavior = self.adapter_behavior(self.agent_clan,agent) #define a behavior adapter
        break_marker = False #stop marker
        landscape = self.agent_clan.landscape
        ct = 0 #current time
        agent.IN = len(agent.plans) #for waterfall, anyway just one plan...
        #### INITIALIZATION ####
        agent.expected_performance = landscape.get_noised_score_of_location_by_id(
                                    agent.my_id,
                                    func = linear_uncertainty,
                                    uncertainty_base = self.uncertainty_base,
                                    tick = agent.I,
                                    total_tick = agent.agent.IN)
        # expected performance := true fitness value +- error (i.e., uncertainty ~ uniform(given range))
        # When a project starts, nobody knows feedback from customers. The team may rely on market research data.
        agent.true_performance = landscape.get_score_of_location_by_id(agent.my_id)
        agent.performance = agent.true_performance
        # But God knows a true performance.
        self.simulator.write_record(agent)
        # Let's write the true result as a record
        agent.visited_ids[agent.my_id]='v'
        # Since the starting point is already visited...
        agent.wanna_be_my_id = agent.my_id # not want to go anywhere at start
        # Do not want to go somewhere now...
        #### SEARCHING ####
        for plan in agent.plans: #per each plan
            while 1:
                agent.ct = ct # let him know the current tick(=time)
                (agent.my_id, agent.true_performance) = current_behavior.execute(agent, plan) #update
                agent.performance = agent.true_performance
                ct += 1 # increase time
                self.simulator.write_record(agent) # write a record after work
                if ct >= self.tick_end: # if ticks are over the target number,
                    break_marker = True # let the break mark true
                    break # stop improving
            # feedback
            if isinstance(agent,AgileDeveloper):
                agent.I = agent.I + 1 # reduce uncertainty if, an agile developer
            agent.expected_performance = agent.true_performance # let the agent know about the true performance
            # finalize
            if break_marker == True:
                break
# END OF PROGRAM #