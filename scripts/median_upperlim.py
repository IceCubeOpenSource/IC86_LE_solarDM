#Loops through the output txt files of 1D_signal_sensitivity and calculates the median signal events for all masses

import numpy as np
import glob

ch = 11

sensitivity = []

for i in range(0,6): #loop through all masses
    rank_list = []
    filename = '/data/user/mnisa/SolarDM/signal_events/sig_sensi_mass_%s_ch_%s.txt'%(i,ch)
    with open(filename) as file:
         for line in file:
             rank_list.append(float(line[:-1])) if line[-1] == '\n' else rank_list.append(float(line))
    sensitivity.append(np.percentile(np.asarray(rank_list),50))

ofile = '/data/user/mnisa/SolarDM/sensitivity/median_upper_limit_ch%s.txt' %ch

f = open(ofile,'w')
for x in sensitivity:
    f.write('%s\n'%x)
    
f.close()



