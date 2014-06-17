'''
simulator.py

NK Landscape Model
Modularity x ISD

Jungpil and Taekyung

2014
'''
import numpy as np
import csv, time, gzip, copy, sqlite3, gzip, os
import RandomGenerator
from landscape import LandscapeAdaptive

class SimRecord:
    def __init__(self, my_id, plan, ct, performance, sim_code, random_seed):
        self.location_id = my_id
        self.plan = self.str_plan(plan)
        self.ct = ct
        self.performance = performance
        self.sim_code = sim_code
        self.random_seed = random_seed
    def str_plan(self,plan_as_list):
        rv = "-".join(map(str,plan_as_list))
        return rv
class Simulator:
    def __init__(self,agent_clan):
        self.agent_clan = agent_clan
        self.current_record = []
        self.simulation_record = []
        self.sim_code = 0
        self.random_seed = -1
        self.note="" #for database recording
    def run(self, tick_end, adapter_plan, adapter_behavior):
        #
        self.current_record = []
        self.random_seed = self.agent_clan.landscape.fitness_contribution_table.random_seed
        self.sim_code += 1
        agent_clan = self.agent_clan
        agent_clan.refresh_clan()
        self.adapter_plan_profile = adapter_plan.profile()
        self.adapter_behavior_profile = adapter_behavior.profile()
        for agent in agent_clan.tribe:
            my_plan = adapter_plan(self, adapter_behavior, agent_clan, agent, tick_end)
            my_plan.run()
        if isinstance(agent_clan.landscape, LandscapeAdaptive):
            agent_clan.landscape.standardize()
            for record in self.current_record:
                record.performance = agent_clan.landscape.get_standardized_value(record.performance)
        self.simulation_record.extend(copy.deepcopy(self.current_record))
    def write_record(self,agent):
        sr = SimRecord(agent.my_id, agent.plans, agent.ct, agent.performance, self.sim_code, self.random_seed)
        self.current_record.append(sr)
    def export_record(self,file_name):
        #for plot
        simple_simulation_record = [(sr.ct,sr.performance) for sr in self.simulation_record]
        nrow = len(simple_simulation_record)
        ncol = 2
        a = np.zeros(nrow*ncol,dtype='f').reshape(nrow,ncol)
        for k,l in enumerate(simple_simulation_record):
            a[k,0] = l[0]
            a[k,1] = l[1]
        file_name_plot = "%s_spreadsheet_plot.txt" % file_name
        np.savetxt(file_name_plot,a,fmt=['%d','%.4f'],delimiter=',')
        #for record
        processing_power,land_n,land_k = self.agent_clan.my_profile()
        db_fname = "%s_record.sqlite3.db" % file_name
        conn = sqlite3.connect(db_fname)
        cursor = conn.cursor() #cursor
        # create schema
        sql = """CREATE TABLE IF NOT EXISTS nk_record 
            (location_id NUMBER,
            tick NUMBER,
            plan TEXT,
            performance NUMBER,
            simulation_code NUMBER,
            random_seed NUMBER, 
            processing_power NUMBER,
            N NUMBER,
            K NUMBER,
            note TEXT);""" #no index
        cursor.execute(sql)
        conn.commit()
        sql = """INSERT INTO nk_record 
                (location_id,tick,plan,performance,simulation_code,random_seed,processing_power,N,K,note) 
                VALUES (?,?,?,?,?,?,?,?,?,?);"""
        for sr in self.simulation_record:
            cursor.execute(sql,(sr.location_id, sr.ct, sr.plan, sr.performance, sr.sim_code, sr.random_seed,processing_power,land_n,land_k,self.note))
        conn.commit()
        conn.close()
        # compress the file
        fin = open(db_fname,'rb')
        fout = open("%s.gz"%db_fname,'wb')
        fout.writelines(fin)
        fout.close()
        fin.close()
        # remove the db file
        os.remove(db_fname)
        #for profile
        plan_profile = self.adapter_plan_profile
        clan_data =  self.agent_clan.__str__()
        behavior_profile = self.adapter_behavior_profile
        time_stamp = time.ctime()
        file_name_profile = "%s_profile.txt" % file_name
        f_profile = open(file_name_profile,'wb')
        f_profile.write("=========================================\n")
        f_profile.write("NK Landscape Simuation\n")
        f_profile.write("=========================================\n")
        f_profile.write("\nRandom seed:%d\n"%RandomGenerator.get_current_seed())
        f_profile.write("\n%s\n"%time_stamp)
        f_profile.write("\n%s\n"%plan_profile)
        f_profile.write("\n%s\n"%clan_data)
        f_profile.write("\n%s\n"%behavior_profile)
        f_profile.close()
class AdapterPlan:
    def __init__(self, simulator, adapter_behavior, agent_clan, agent, tick_end):
        self.simulator = simulator
        self.adapter_behavior = adapter_behavior
        self.agent_clan = agent_clan
        self.agent = agent
        self.tick_end = tick_end
        self.fix_plan = self.agent_clan.fix_plan
        self.uncertainty_base = agent_clan.uncertainty_base
    def run(self):
        agent = self.agent
        current_behavior = self.adapter_behavior(self.agent_clan,agent)
        break_marker = False
        ct = 0
        agent.my_performance = self.agent_clan.landscape.get_score_of_location_by_id(agent.my_id)
        self.simulator.write_record(agent)
        while 1:
            for plan in agent.plans:
                agent.ct = ct
                (agent.my_id, agent.my_performance) = current_behavior.execute(agent, plan)
                ct += 1
                self.simulator.write_record(agent)
                if ct >= self.tick_end: # if ticks are over the target number,
                    break_marker = True
                    break
            if break_marker == True:
                break
    def my_profile(cls):
        pass
    profile = classmethod(my_profile)
class AdapterBehavior:
    def __init__(self, agent_clan, agent):
        self.agent_clan = agent_clan
    def execute(self, agent, plan):
        pass
    def my_profile(cls):
        pass
    profile = classmethod(my_profile)
# END OF PROGRAM #