'''
isd_adapter_plan.py

NK Landscape Model
Modularity x ISD

Jungpil and Taekyung

2014
'''

import numpy as np
import copy
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
        #self.simulator.time_box = True #default setting
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
                                    total_tick = agent.IN)
        # expected performance := true fitness value +- error (i.e., uncertainty ~ uniform(given range))
        # When a project starts, nobody knows feedback from customers. The team may rely on market research data.
        agent.true_performance = landscape.get_score_of_location_by_id(agent.my_id)
        agent.performance = agent.true_performance
        # But God knows a true performance.
        #self.simulator.write_record(agent)
        # Let's write the true result as a record
        agent.visited_ids[agent.my_id]='v'
        # Since the starting point is already visited...
        agent.wanna_be_my_id = agent.my_id # not want to go anywhere at start
        # Do not want to go somewhere now...
        #### SEARCHING ####
        plan_length = len(agent.plans)
        q = agent.tick_end / plan_length
        plan_history = []
        plan_idx = 0
        while 1:
            plan = agent.plans[plan_idx]
        #for k,plan in enumerate(agent.plans): #per each plan
            # fixplan
            if self.simulator.fix_plan_on:
                plan_history.extend(plan)
                fix_plan = list(set(plan_history))
                landscape.fix_plan = copy.deepcopy(fix_plan)
            location_before = agent.my_id
            while 1:
                agent.ct = ct # let him know the current tick(=time)
                (agent.my_id, agent.true_performance) = current_behavior.execute(agent, plan) #update
                agent.performance = agent.true_performance
                self.simulator.write_record(agent) # write a record after work
                # for agile
                if ct >= self.tick_end:
                    break_marker = True
                    break
                ct += 1 # increase time
                if isinstance(agent, AgileDeveloper):
                    if self.simulator.time_box:
                        if ct != 0 and ct % q == 0: #break point
                            #feedback
                            if agent.I < agent.IN:
                                agent.I = agent.I + 1 # reduce uncertainty if, an agile developer
                                agent.expected_performance = agent.true_performance # let the agent know about the true performance
                            if plan_idx < plan_length and (plan_idx + 1 ) != plan_length:
                                plan_idx += 1
                                break # for next plan
                    else: # no time box
                        if agent.my_id == location_before: # 
                            if agent.I < agent.IN:
                                agent.I = agent.I + 1 # reduce uncertainty if, an agile developer
                                agent.expected_performance = agent.true_performance # let the agent know about the true performance
                            if plan_idx < plan_length and (plan_idx + 1) != plan_length:
                                plan_idx += 1
                                break # just go out... get out of this plan
                        else:
                            location_before = agent.my_id
            # finalize
            if break_marker == True:
                break            
            if self.simulator.fix_plan_on:
                landscape.clear() # reset simplifiability and uncertainty effects for next iteration

# END OF PROGRAM #