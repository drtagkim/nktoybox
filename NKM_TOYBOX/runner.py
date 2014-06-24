#runner
import test_case as TC
plans_agile = [[0,1,2,3],[4,5,6,7],[8,9,10,11]]
plans_wf = [[0,1,2,3,4,5,6,7,8,9,10,11]]

def main(cid,number_of_simulation,uncertainty_list,note):
    """
|  cid: influence_matrix index (modularity level)
|  number_of_simulation: the number of simulations
|  uncertainty_list: a list of uncertainty levels
|  note: this string data will be added on result data
    """
    land = TC.factory_landscape('inf/n12k4_m3_%s.txt'%cid,calculation_now=False)
    # compute fitness values when the landscape is created (-> calculation_now = True; o.w., False).
    for uc in uncertainty_list:
        print "---------- %f" % uc
        # clan
        clan_water = TC.factory_wf_clan(land,plans_wf)
        clan_agile = TC.factory_agile_clan(land,plans_agile)
        clan_water.uncertainty_base = uc
        clan_agile.uncertainty_base = uc
        # output
        output_fname_wf="wf/wf_%s_%f" % (cid,uc,)
        output_fname_ag="agile/agile_%s_%f" % (cid,uc,)
        # simulation
        TC.run_simulation_group(clan_water, 
                          clan_agile,
                          number_of_simulation,
                          TC.AdapterBehaviorWaterfallTeam,
                          TC.AdapterBehaviorAgileTeam,
                          output_fname_wf,
                          output_fname_ag,
                          note,
                          run_time=35) # time tick
        
if __name__ == "__main__":
    uncertainty_list = [0.0,0.5]
    note = "m_full"
    main('a', 20, uncertainty_list,note)
    note = "m_partial"
    main('b', 20, uncertainty_list,note)
    note = "m_none"
    main('c', 20, uncertainty_list,note)
    #sim_water('a',20)
    #sim_water('b',20)
    #sim_water('c',20)
    #sim_agile('a',20)
    #sim_agile('b',20)
    #sim_agile('c',20)
    