import numpy as np
import matplotlib as mpl
mpl.use('Agg')
mpl.rc('text',usetex = True)
mpl.rc('font',family = 'serif',size = '20')
import matplotlib.pyplot as plt

ch = ['tautau','bb','nunu']

masses = []
limits = []

for c in ch:
  files = '../sensitivity/%s.txt'%c
  data = np.genfromtxt(files,delimiter = ',')
  masses.append(data[:,0])
  limits.append(data[:,1])

#PICO Results
pico_x = [5,10,20,35,50,100]
pico_y = [2e-39,8.68e-41,3.68e-41,3.34e-41,3.68e-41,5.5e-41]
    
#IC2017
ic_2017_tt_mass = [20,35,50,100]
ic_2017_tt_lim = [4.85e-40,1.35e-40,7.9e-41,2.91e-41]

ic_2017_bb_mass = [35,50,100]
ic_2017_bb_lim =  [92.5e-40,63.9e-40,32.9e-40]

#Super-K
sk_bb_mass = [6,10,20,50,100]
sk_bb_lim = [17.2e-40,14.9e-40,14.3e-40,23.4e-40,31.9e-40]

sk_tt_mass = [4,6,10,20,50,100]
sk_tt_lim = [2.22e-40,1.63e-40,1.31e-40,1.42e-40,1.28e-40,1.24e-40]

fig,ax = plt.subplots(figsize  = (12,8))

ax.plot(pico_x,pico_y,label = 'PICO-60 2017',lw = 2,ls = '-.')

ax.plot(ic_2017_tt_mass,ic_2017_tt_lim, label = r'IC 2017 $\tau\bar{\tau}$',ls = ':',color = 'm')
ax.plot(ic_2017_bb_mass,ic_2017_bb_lim, label = r'IC 2017 $b\bar{b}$',ls = ':',lw = 2,color = 'y')

ax.plot(sk_tt_mass,sk_tt_lim, label = r'Super-K 2015 $\tau\bar{\tau}$',ls = '--',lw = 2,color = 'm')
ax.plot(sk_bb_mass,sk_bb_lim, label = r'Super-K 2015 $b\bar{b}$',ls = '--',lw = 2,color = 'y')

label = [r'$\tau\bar{\tau}$',r'$b\bar{b}$',r'$\nu\bar{\nu}$']
color = ['m','y','b']

for m,s,l,c in zip(masses,limits,label,color):
    ax.plot(m,s,lw = 2,color = '%s'%c,label = '%s'%l)

ax.set(ylabel = r"$\sigma^{\rm SD}_{\chi \rm p}$ [cm$^2$]",
       xlabel = r"m$_{\chi}$ [GeV]",yscale='log')
ax.legend(bbox_to_anchor=(1, 0.5, 0.1, 0.1))
fig.tight_layout()
ax.grid()
plt.savefig('sensi_all_ch.png')
#plt.show()



