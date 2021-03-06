cd C:\Users\workshop\Documents\GitHub\nktoybox\NKM_TOYBOX

from landscape import construct_influence_matrix_from_list
from landscape import FitnessContributionTable
from landscape import Landscape
from landscape import count_local_peak

k0 = [[1,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,0,0],[0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,0,1]]
k1 = [[1,1,0,0,0,0,0,0,0,0],[0,1,1,0,0,0,0,0,0,0],[0,0,1,1,0,0,0,0,0,0],[0,0,0,1,1,0,0,0,0,0],[0,0,0,0,1,1,0,0,0,0],[0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,0,1,1,0,0],[0,0,0,0,0,0,0,1,1,0],[0,0,0,0,0,0,0,0,1,1],[1,0,0,0,0,0,0,0,0,1]]
k2 = [[1,1,1,0,0,0,0,0,0,0],[0,1,1,1,0,0,0,0,0,0],[0,0,1,1,1,0,0,0,0,0],[0,0,0,1,1,1,0,0,0,0],[0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,1,1,1,0,0],[0,0,0,0,0,0,1,1,1,0],[0,0,0,0,0,0,0,1,1,1],[1,0,0,0,0,0,0,0,1,1],[1,1,0,0,0,0,0,0,0,1]]
k3 = [[1,1,1,1,0,0,0,0,0,0],[0,1,1,1,1,0,0,0,0,0],[0,0,1,1,1,1,0,0,0,0],[0,0,0,1,1,1,1,0,0,0],[0,0,0,0,1,1,1,1,0,0],[0,0,0,0,0,1,1,1,1,0],[0,0,0,0,0,0,1,1,1,1],[1,0,0,0,0,0,0,1,1,1],[1,1,0,0,0,0,0,0,1,1],[1,1,1,0,0,0,0,0,0,1]]
k4 = [[1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0],[0,0,1,1,1,1,1,0,0,0],[0,0,0,1,1,1,1,1,0,0],[0,0,0,0,1,1,1,1,1,0],[0,0,0,0,0,1,1,1,1,1],[1,0,0,0,0,0,1,1,1,1],[1,1,0,0,0,0,0,1,1,1],[1,1,1,0,0,0,0,0,1,1],[1,1,1,1,0,0,0,0,0,1]]
k5 = [[1,1,1,1,1,1,0,0,0,0],[0,1,1,1,1,1,1,0,0,0],[0,0,1,1,1,1,1,1,0,0],[0,0,0,1,1,1,1,1,1,0],[0,0,0,0,1,1,1,1,1,1],[1,0,0,0,0,1,1,1,1,1],[1,1,0,0,0,0,1,1,1,1],[1,1,1,0,0,0,0,1,1,1],[1,1,1,1,0,0,0,0,1,1],[1,1,1,1,1,0,0,0,0,1]]
k6 = [[1,1,1,1,1,1,1,0,0,0],[0,1,1,1,1,1,1,1,0,0],[0,0,1,1,1,1,1,1,1,0],[0,0,0,1,1,1,1,1,1,1],[1,0,0,0,1,1,1,1,1,1],[1,1,0,0,0,1,1,1,1,1],[1,1,1,0,0,0,1,1,1,1],[1,1,1,1,0,0,0,1,1,1],[1,1,1,1,1,0,0,0,1,1],[1,1,1,1,1,1,0,0,0,1]]
k7 = [[1,1,1,1,1,1,1,1,0,0],[0,1,1,1,1,1,1,1,1,0],[0,0,1,1,1,1,1,1,1,1],[1,0,0,1,1,1,1,1,1,1],[1,1,0,0,1,1,1,1,1,1],[1,1,1,0,0,1,1,1,1,1],[1,1,1,1,0,0,1,1,1,1],[1,1,1,1,1,0,0,1,1,1],[1,1,1,1,1,1,0,0,1,1],[1,1,1,1,1,1,1,0,0,1]]
k8 = [[1,1,1,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,1,1,1],[1,0,1,1,1,1,1,1,1,1],[1,1,0,1,1,1,1,1,1,1],[1,1,1,0,1,1,1,1,1,1],[1,1,1,1,0,1,1,1,1,1],[1,1,1,1,1,0,1,1,1,1],[1,1,1,1,1,1,0,1,1,1],[1,1,1,1,1,1,1,0,1,1],[1,1,1,1,1,1,1,1,0,1]]
k9 = [[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1]]

plan0 = None
plan2= [0,1]
plan3 = [0,1,2]
plan4 = [0,1,2,3]
plan5 = [0,1,2,3,4]
plan6 = [0,1,2,3,4,5]
plan7 = [0,1,2,3,4,5,6]
plan8 = [0,1,2,3,4,5,6,7]
plan9 = [0,1,2,3,4,5,6,7,8]
plan10 = [0,1,2,3,4,5,6,7,8,9]

def testing(input_a,plan,itern=10):
    sum = 0.0
    for _ in range(itern):
        im_list = input_a
        inf = construct_influence_matrix_from_list(im_list)
        fit1 = FitnessContributionTable(inf)
        land1 = Landscape(fitness_contribution_matrix = fit1)
        land1.compute_all_locations_id(plan)
        land1.standardize()
        sum+= count_local_peak(land1,False) 
    return sum / float(itern)
    
kset = [k0,k1,k2,k3,k4,k5,k6,k7,k8,k9]
planset = [plan0,plan3,plan5,plan7,plan9]

for iks, ks in enumerate(kset):
    for ips,ps in enumerate(planset):
        print "ks=%d, ps=%d, peak=%f" % (iks,ips,testing(ks,ps,1))
