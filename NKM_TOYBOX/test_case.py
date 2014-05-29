#Testing
import simulator
from landscape import FitnessContributionTable
from landscape import construct_influence_matrix_from_file
from isd_agent import AgileDeveloper
from isd_agent import AgileDeveloperClan
from landscape import Landscape
from isd_adapter_plan import AdapterPlanISD
from isd_strategy import AdapterBehaviorAgileTeam
from isd_agent import WaterfallDeveloper
from isd_agent import WaterfallDeveloperClan
from isd_adapter_plan import AdapterPlanISD
from isd_strategy import AdapterBehaviorWaterfallTeam

def factory_landscape(file_name,uncertainty):
    inf = construct_influence_matrix_from_file(file_name,markchr='x')
    fit = FitnessContributionTable(inf)
    land = Landscape(fitness_contribution_matrix=fit,uncertainty=uncertainty)
    land.compute_all_locations_id()
    return land
def factory_agile_clan(land,plans):
    agile_clan = AgileDeveloperClan(land,1,AgileDeveloper,100)
    agile_clan.set_iteration_plan(plans)
    agile_clan.hatch_members()
    return agile_clan
def factory_wf_clan(land,plans):
    wf_clan = WaterfallDeveloperClan(land,1,WaterfallDeveloper,100)
    wf_clan.set_iteration_plan(plans)
    wf_clan.hatch_members()
    return wf_clan
def run_simulation(clan,n,adapter,output_file_name):
    sim1 = simulator.Simulator(clan)
    for i in xrange(n):
        sim1.run(30,AdapterPlanISD,adapter)
        print "%04d ..." % i
    sim1.export_record(output_file_name)
    print "OK"



    