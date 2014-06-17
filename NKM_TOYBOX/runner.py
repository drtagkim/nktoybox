#runner
import test_case as TC
plans_agile = [[0,1,2,3],[4,5,6,7],[8,9,10,11]]
plans_wf = [[0,1,2,3,4,5,6,7,8,9,10,11]]


def sim_water(cid,number_of_simulation):
    land = TC.factory_landscape('inf/n12k4_m3_%s.txt'%cid,calculation_now=False)
    for uc in [0.0,0.2,0.4,0.6,0.8]:
        print "---------- %f" % uc
        clan_water = TC.factory_wf_clan(land,plans_wf)
        clan_water.uncertainty_base = uc
        output_fname="wf/wf_%s_%f" % (cid,uc,)
        TC.run_simulation(clan_water,number_of_simulation,TC.AdapterBehaviorWaterfallTeam,output_fname,run_time=35)
def sim_agile(cid,number_of_simulation):
    land = TC.factory_landscape('inf/n12k4_m3_%s.txt'%cid,calculation_now=False)
    for uc in [0.0,0.2,0.4,0.6,0.8]:
        print "---------- %f" % uc
        clan_agile = TC.factory_agile_clan(land,plans_agile)
        clan_agile.uncertainty_base = uc
        output_fname="agile/agile_%s_%f" % (cid,uc,)
        TC.run_simulation(clan_agile,number_of_simulation,TC.AdapterBehaviorAgileTeam,output_fname,run_time=35)
if __name__ == "__main__":
    sim_water('a',20)
    sim_water('b',20)
    sim_water('c',20)
    sim_agile('a',20)
    sim_agile('b',20)
    sim_agile('c',20)
    