from array import array
from math import *
import cPickle as pickle
import json

sd_conversion_factor = [9.59e-029, 2.12e-028,5.28e-028,1.25e-027,2.29e-027,8.07e-027]



x = [5,10,20,35,50,100]
x_5 = [10,20,35,50,100]
x_array = array("d",x)
x_5_array = array("d",x_5)

pico_x = [5,10,20,35,50,100]
pico_y = [2e-39,8.68e-41,3.68e-41,3.34e-41,3.68e-41,5.5e-41]

marcel_x_array = array("d",[20,35,50,100])
marcel_y_array = array("d",[4.85e-40,1.35e-40,7.9e-41,2.91e-41])


sk_x_array = array("d",[4,6,10,20,50,100])
sk_x_array_ch5 = array("d",[6,10,20,50,100])
sk_y_array = array("d",[2.22e-40,1.63e-40,1.31e-40,1.42e-40,1.28e-40,1.24e-40])
sk_y_array_ch5 = array("d",[17.2e-40,14.9e-40,14.3e-40,23.4e-40,31.9e-40])

livetime = 365.25*24*60*60

ch11_signal_event_sensitivity = []
#filename = "/data/user/mnisa/SolarDM/sensitivity/1D_median_upper_limit_36bins.txt" 
filename = "/data/user/mnisa/SolarDM/sensitivity/1D_median_upper_limit_674_optimized_erange.txt" 
with open(filename,"r") as f:
	tmp_list = json.load(f)
	tmp_list.reverse()
	ch11_signal_event_sensitivity = tmp_list

ch11_total_signal_weight = []
filename = "/data/user/mnisa/SolarDM/sensitivity/optimized_erange_total_weight_ch11.txt"
with open(filename,"r") as f:
	tmp_list = pickle.load(f)
	#tmp_list.reverse()
	ch11_total_signal_weight = tmp_list

ch11_sd_xsec = []
for j in range(0,len(ch11_signal_event_sensitivity)):
	annihilation_rate = ch11_signal_event_sensitivity[j]/(ch11_total_signal_weight[j]*livetime)
	time_factor = 7
	ch11_sd_xsec.append(annihilation_rate*sd_conversion_factor[j]*1e-36/sqrt(time_factor))

ch14_signal_event_sensitivity = []
filename = "/data/user/mnisa/SolarDM/sensitivity/1D_median_upper_limit_674_optimized_erange_ch14.txt" 
with open(filename,"r") as f:
	tmp_list = json.load(f)
	tmp_list.reverse()
	ch14_signal_event_sensitivity = tmp_list

ch14_total_signal_weight = []
filename = "/data/user/mnisa/SolarDM/sensitivity/optimized_erange_total_weight_ch14.txt"
with open(filename,"r") as f:
	tmp_list = pickle.load(f)
	ch14_total_signal_weight = tmp_list


ch14_sd_xsec = []
for j in range(0,len(ch14_signal_event_sensitivity)):
	annihilation_rate = ch14_signal_event_sensitivity[j]/(ch14_total_signal_weight[j]*livetime)
	time_factor = 7
	ch14_sd_xsec.append(annihilation_rate*sd_conversion_factor[j]*1e-36/sqrt(time_factor))

ch5_signal_event_sensitivity = []
filename = "/data/user/mnisa/SolarDM/sensitivity/3D_median_upper_limit_ch5.txt" 
with open(filename,"r") as f:
	tmp_list = json.load(f)
	tmp_list.reverse()
	ch5_signal_event_sensitivity = tmp_list

ch5_total_signal_weight = []
filename = "/data/user/mnisa/SolarDM/sensitivity/optimized_total_weight_ch5.txt"
with open(filename,"r") as f:
	tmp_list = pickle.load(f)
	ch5_total_signal_weight = tmp_list

ch5_sd_xsec = []
for j in range(0,len(ch5_signal_event_sensitivity)):
	annihilation_rate = ch5_signal_event_sensitivity[j]/(ch5_total_signal_weight[j]*livetime)
	time_factor = 7
	ch5_sd_xsec.append(annihilation_rate*sd_conversion_factor[j+1]*1e-36/sqrt(time_factor))


	
#Print and save limits
ofile = '../sensitivity/tautau.txt'
f = open(ofile,'w')
f.write('#Mass,  Lim \n')

print("tau tau")
print("Mass (GeV)","Sigma_sd (cm^2)")
for i,j in zip(x_array,ch11_sd_xsec):
    print(i,j)
    f.write('%s, %s  \n'%(i,j))
f.close()

ofile = '../sensitivity/nunu.txt'
f = open(ofile,'w')
f.write('#Mass,  Lim \n')

print("nu nu")
print("Mass (GeV)","Sigma_sd (cm^2)")
for i,j in zip(x_array,ch14_sd_xsec):
    print(i,j)
    f.write('%s, %s  \n'%(i,j))
f.close()

ofile = '../sensitivity/bb.txt'
f = open(ofile,'w')
f.write('#Mass,  Lim \n')


print("b b")
print("Mass (GeV)","Sigma_sd (cm^2)")
for i,j in zip(x_5_array,ch5_sd_xsec):
    print(i,j)
    f.write('%s, %s  \n'%(i,j))
f.close()

print("ok")


