# SETTING
NUMBER_OF_AGILE_AGENTS = 100
NUMBER_OF_WF_AGENTS = 100
INFLUENCE_MATRIX_MARK = '1'

# PROGRAM
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
def run_simulation(clan,n,adapter,output_file_name,
                   run_time = 35,
                   time_box = False,
                   fix_plan_on = False):
    """
|  default time tick = 35
|  for testing
    """
    sim1 = simulator.Simulator(clan)
    # SIMULATION SETTING
    sim1.time_box = time_box # time boxing
    sim1.fix_plan_on = fix_plan_on # fix model
    # RUN SIMULATIONS
    for i in xrange(n):
        sim1.run(run_time,AdapterPlanISD,adapter)
        sys.stdout.write("%04d ... " % i)
        sys.stdout.flush()
        if i > 0 and i % 10 == 0:
            print ""
        #refresh random status
        fitness_contribution_table = clan.landscape.fitness_contribution_table
        fitness_contribution_table.refresh(i + 1) #increase random seed by 1
        clan.landscape.compute_all_locations_id(fix_plan = clan.landscape.fix_plan)
        if isinstance(clan.landscape,LandscapeAdaptive):
            clan.landscape.fitness_value_dict = {}
            clan.landscape.fitness_correction_item = {}
    sim1.export_record(output_file_name)
    print "OK"
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



