'''
isd_strategy.py

NK Landscape Model
Modularity x ISD

Jungpil and Taekyung

2014
'''

import numpy as np
from simulator import AdapterBehavior
from algorithm import linear_uncertainty

class AdapterBehaviorAgileTeam(AdapterBehavior):
    """
|  Behavior of developers who adopts the agile methodology
    """
    def __init__(self, agent_clan, agent):
        AdapterBehavior.__init__(self, agent_clan,agent)
    def execute(self,agent, plan):
        #rewrite from here
        landscape = self.agent_clan.landscape
        new_id = agent.my_id
        new_performance = agent.true_performance
        current_score = agent.expected_performance #casue agile gets feedback right away
        # an incremental experiential search
        neighbors = set(landscape.who_are_neighbors(agent.my_id,plan,self.agent_clan.myProcessingPower,False)) #except me
        neighbors_np = np.array(list(neighbors),dtype=np.int)
        np.random.shuffle(neighbors_np) #randomly select configuration (by luck)
        for neighbor_id in np.nditer(neighbors_np):
            neighbor_id_int = int(neighbor_id)
            new_score = landscape.get_noised_score_of_location_by_id(
                                neighbor_id_int,
                                uncertainty_base = self.agent_clan.uncertainty_base,
                                func = linear_uncertainty,
                                tick = agent.I,
                                total_tick = agent.IN)
            if current_score < new_score and not agent.visited_ids.has_key(int(neighbor_id)):
                agent.wanna_be_my_id = neighbor_id_int
                new_id = neighbor_id_int # jump to the location, no feedback
                agent.visited_ids[new_id]='v'
                new_performance = landscape.get_score_of_location_by_id(new_id)
                agent.expected_performance = new_score
        return (new_id,new_performance)
    def my_profile(cls):
        rv = "----------------------------\n%s\n----------------------------\n" % ("Agile Development Team")
        return rv
    profile = classmethod(my_profile)
class AdapterBehaviorWaterfallTeam(AdapterBehavior):
    """
|  Behavior of developers who adopt the waterfall methodology
    """
    def __init__(self, agent_clan, agent):
        AdapterBehavior.__init__(self, agent_clan,agent)
    def execute(self,agent, plan):
        # base
        landscape = self.agent_clan.landscape
        new_id = agent.my_id
        new_performance = agent.true_performance
        # requirement collection
        current_score = agent.expected_performance # exact information from the start
        neighbors = set(landscape.who_are_neighbors(agent.my_id,plan,self.agent_clan.myProcessingPower,False)) #except me
        neighbors_np = np.array(list(neighbors),dtype=np.int)
        np.random.shuffle(neighbors_np) #randomly select configuration (by luck)
        for neighbor_id in np.nditer(neighbors_np):
            neighbor_id_int = int(neighbor_id)
            new_score = landscape.get_noised_score_of_location_by_id(
                                neighbor_id_int,
                                uncertainty_base = self.agent_clan.uncertainty_base,
                                func = linear_uncertainty,
                                tick = agent.I,
                                total_tick = agent.IN)            
            if current_score < new_score and not agent.visited_ids.has_key(int(neighbor_id)):
                agent.wanna_be_my_id = neighbor_id_int
                new_id = neighbor_id_int # jump to the location, no feedback
                agent.visited_ids[new_id]='v'
                new_performance = landscape.get_score_of_location_by_id(new_id)
                agent.expected_performance = new_score
        return (new_id,new_performance)
    def my_profile(cls):
        rv = "----------------------------\n%s\n----------------------------\n" % ("Waterfall Development Team")
        return rv
    profile = classmethod(my_profile)
# END OF PROGRAM #