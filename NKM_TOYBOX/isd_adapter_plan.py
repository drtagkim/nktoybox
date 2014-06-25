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
    def my_profile(cls):
        return "\nPlan for ISD Development Simulation\n"
    profile = classmethod(my_profile)
    def run(self):
        """
|  Run a simulator
|  This contains a core algorithm for managing the entire simulation
        """
        # REFERENCE
        agent = self.agent #assing to local reference
        landscape = self.agent_clan.landscape
        # EDUCATION
        agent.tick_end = self.tick_end
        current_behavior = self.adapter_behavior(self.agent_clan,agent) #define a behavior adapter
        agent.IN = len(agent.plans) #for waterfall, anyway just one plan...
        agent.visited_ids[agent.my_id]='v'
        agent.wanna_be_my_id = agent.my_id # not want to go anywhere at start
        agent.expected_performance = landscape.get_noised_score_of_location_by_id(
                                    agent.my_id,
                                    func = linear_uncertainty,
                                    uncertainty_base = self.uncertainty_base,
                                    tick = agent.I,
                                    total_tick = agent.IN)
        agent.true_performance = landscape.get_score_of_location_by_id(agent.my_id)
        agent.performance = agent.true_performance
        # CONTROL VARIABLES
        break_marker = False #stop marker
        ct = 0 #current time
        plan_length = len(agent.plans)
        q = agent.tick_end / plan_length
        plan_history = []
        plan_idx = 0
        # PRECONDITION
        assert isinstance(agent.plans,list),""
        assert len(agent.plans) > 0, "At least one plan!"
        assert self.simulator.fix_plan_on == True or self.simulator.fix_plan_on == False, ""
        # DESIGN PROCESS BEGINS
        while 1:
            try:
                plan = agent.plans[plan_idx]
            except:
                assert False, "You have a problem on planning!"
            # fixplan
            if self.simulator.fix_plan_on:
                plan_history.extend(plan)
                fix_plan = list(set(plan_history)) # learned
                landscape.fix_plan = copy.deepcopy(fix_plan) #copy the fix_plan
            # set initial location
            location_before = agent.my_id
            while 1:
                # TIME GOES
                agent.ct = ct # let him know the current tick(=time)
                (agent.my_id, agent.true_performance) = current_behavior.execute(agent, plan) #update
                agent.performance = agent.true_performance
                self.simulator.write_record(agent) # write a record after work
                # FINITE LOOPING
                if ct >= self.tick_end:
                    break_marker = True # exit the outer loop
                    break # exit search process
                # CHECK OUT
                ct += 1 # increase time
                # AGILE PROCESSING
                if isinstance(agent, AgileDeveloper):
                    # TIME BOXING
                    if self.simulator.time_box:
                        if ct != 0 and ct % q == 0: #break point
                            #feedback
                            if agent.I < agent.IN and agent.I != agent.IN:
                                agent.I += 1 # reduce uncertainty if, an agile developer
                                agent.expected_performance = agent.true_performance
                            #proceeding to the next plan
                            if plan_idx < plan_length and (plan_idx + 1 ) != plan_length:
                                plan_idx += 1
                                break # for next plan
                    else: # no time boxing
                        if agent.my_id == location_before: # if nowhere to go (i.e., no improvement) 
                            if agent.I < agent.IN and agent.I != agent.IN:
                                agent.I += 1 # reduce uncertainty if, an agile developer
                                agent.expected_performance = agent.true_performance
                            #proceeding to the next plan
                            if plan_idx < plan_length and (plan_idx + 1) != plan_length:
                                plan_idx += 1
                                break
                        else:
                            location_before = agent.my_id #update location
            # finalize
            if break_marker == True:
                break            
            if self.simulator.fix_plan_on:
                landscape.clear() # reset simplifiability and uncertainty effects for next iteration
# END OF PROGRAM #