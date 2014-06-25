'''
==================================================
            NK LANDSCAPE SIMULATION
                  2014.SUMMER
        
                 JUNGPIL HAHN
                 TAEKYUNG KIM
    
              INFORMATION SYSTEMS
              SCHOOL OF COMPUTING
        NATIONAL UNIVERSITY OF SINGAPORE
==================================================
'''


# SETTING
NUMBER_OF_AGILE_AGENTS = 30
NUMBER_OF_WF_AGENTS = 30
RUN_TIME = 30
NUM_SIM = 2
INFLUENCE_MATRIX_MARK = '1'
TIME_BOX_ON = False
SIMPLIFIABLE = True

plans_agile = [[0,1,2,3],[4,5,6,7],[8,9,10,11]]
plans_wf = [[0,1,2,3,4,5,6,7,8,9,10,11]]


# MODULE
import simulator
import sys
from landscape import FitnessContributionTable
from landscape import construct_influence_matrix_from_file
from isd_agent import AgileDeveloper
from isd_agent import AgileDeveloperClan
from landscape import Landscape,LandscapeAdaptive
from isd_adapter_plan import AdapterPlanISD
from isd_strategy import AdapterBehaviorAgileTeam
from isd_agent import WaterfallDeveloper
from isd_agent import WaterfallDeveloperClan
from isd_adapter_plan import AdapterPlanISD
from isd_strategy import AdapterBehaviorWaterfallTeam

# HELPER
def factory_landscape(file_name,calculation_now):
    inf = construct_influence_matrix_from_file(file_name,markchr = INFLUENCE_MATRIX_MARK)
    fit = FitnessContributionTable(inf)
    land = LandscapeAdaptive(fitness_contribution_matrix=fit)
    sys.stdout.write("Landscape creation...")
    land.compute_all_locations_id(calculate_now=calculation_now)
    sys.stdout.write("OK\n")
    return land
def factory_agile_clan(land,plans):
    agile_clan = AgileDeveloperClan(land,1,AgileDeveloper,NUMBER_OF_AGILE_AGENTS)
    agile_clan.set_iteration_plan(plans)
    agile_clan.hatch_members()
    return agile_clan
def factory_wf_clan(land,plans):
    wf_clan = WaterfallDeveloperClan(land,1,WaterfallDeveloper,NUMBER_OF_WF_AGENTS)
    wf_clan.set_iteration_plan(plans)
    wf_clan.hatch_members()
    return wf_clan

def run_simulation_group(clan_wf,
                         clan_ag,
                         n,
                         adapter_wf,
                         adapter_ag,
                         output_file_name_wf,
                         output_file_name_ag,
                         note,                         
                         run_time = 35,
                         time_box = False,
                         fix_plan_on = False):
    """
|  simulator
    """
    # REFERENCE
    landscape = clan_wf.landscape
    # SIMULATORS
    sim1 = simulator.Simulator(clan_wf)
    sim2 = simulator.Simulator(clan_ag)
    # SIMULATION SETTINGS
    sim1.time_box = time_box
    sim2.time_box = time_box
    sim1.fix_plan_on = fix_plan_on
    sim2.fix_plan_on = fix_plan_on
    sim1.note = "%s_waterfall"%note # note appendix (waterfall)
    sim2.note = "%s_agile"%note # note appendix (agile)
    # RUN SIMULATIONS
    for i in xrange(n):
        sys.stdout.write(".WF.")
        sys.stdout.flush()
        sim1.run(run_time,AdapterPlanISD,adapter_wf)
        sys.stdout.write(".AG.")
        sys.stdout.flush()
        sim2.run(run_time,AdapterPlanISD,adapter_ag)
        sys.stdout.write("%04d ... " % i)
        sys.stdout.flush()
        if i > 0 and i % 10 == 0:
            print ""
        #refresh random status
        fitness_contribution_table = landscape.fitness_contribution_table
        fitness_contribution_table.refresh(i + 1) #increase random seed by 1
        landscape.compute_all_locations_id(fix_plan = landscape.fix_plan)
        if isinstance(landscape,LandscapeAdaptive):
            landscape.fitness_value_dict = {}
            landscape.fitness_correction_item = {}
    sim1.export_record(output_file_name_wf)
    sim2.export_record(output_file_name_ag)
    print "OK"


def main(cid,number_of_simulation,uncertainty_list,note):
    """
|  cid: influence_matrix index (modularity level)
|  number_of_simulation: the number of simulations
|  uncertainty_list: a list of uncertainty levels
|  note: this string data will be added on result data
    """
    land = factory_landscape('inf/n12k4_m3_%s.txt'%cid,calculation_now=False)
    # compute fitness values when the landscape is created (-> calculation_now = True; o.w., False).
    for uc in uncertainty_list:
        print "---------- %f" % uc
        # clan
        clan_water = factory_wf_clan(land,plans_wf)
        clan_agile = factory_agile_clan(land,plans_agile)
        clan_water.uncertainty_base = uc
        clan_agile.uncertainty_base = uc
        # output
        output_fname_wf="wf/wf_%s_%f" % (cid,uc,)
        output_fname_ag="agile/agile_%s_%f" % (cid,uc,)
        # simulation
        run_simulation_group(clan_water, 
                          clan_agile,
                          number_of_simulation,
                          AdapterBehaviorWaterfallTeam,
                          AdapterBehaviorAgileTeam,
                          output_fname_wf,
                          output_fname_ag,
                          note,
                          run_time = RUN_TIME,
                          time_box = TIME_BOX_ON,
                          fix_plan_on = SIMPLIFIABLE) # time tick
        
if __name__ == "__main__":
    uncertainty_list = [0.0]
    note = "m_full"
    main('a', NUM_SIM, uncertainty_list,note)
    #note = "m_partial"
    #main('b', NUM_SIM, uncertainty_list,note)
    #note = "m_none"
    #main('c', NUM_SIM, uncertainty_list,note)
    #sim_water('a',20)
    #sim_water('b',20)
    #sim_water('c',20)
    #sim_agile('a',20)
    #sim_agile('b',20)
    #sim_agile('c',20)