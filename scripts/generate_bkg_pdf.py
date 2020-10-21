#Generate background pdfs for the low-energy solar WIMP analysis
#Default channel is 5 (bb)

#!/usr/bin/env python
import numpy as np
import glob
from I3Tray import *
from icecube import icetray, dataclasses, dataio, astro
from math import *
from ROOT import TH1D, TFile, TRandom3, gStyle
from icecube.dataclasses import *
import os

from event_cuts_l5_plus import *

Infile_List1 = sorted(glob.glob("/data/ana/BSM/IC86_LE_solarDM/data/IC86_*/*i3.bz2"))

Infile_List = [os.readlink(f) for f in Infile_List1] #Read symlinks

tray = I3Tray()

out = "background_pdfs" #Path to output file
if not os.path.exists(out):
   os.makedirs(out)

y = 5 #WIMPSIM channel code (5: bb, 11: tau tau, 12:nue,13:numu,14:nutau) 

if y == 11:
	energy_list = ["5","10","20","35","50","100"]
	energy_range_list = [(0,9),(1,16),(3,30),(8,50),(15,69),(30,128)]
	nbins = 36
elif y == 5:
	energy_list = ["10","20","35","50","100"]
	energy_range_list = [(0,11),(0,18),(0,27),(3,38),(6,70)]
	nbins =36
elif y == 12 or y == 13 or y == 14 or y==15:
	energy_list = ["5","10","20","35","50","100"]
	energy_range_list = [(2,11),(0,23),(13,39),(25,70),(42,86),(83,167)]
	nbins = 180

#bg_hist_list = [TH1D("bg_hist_"+energy_list[i]+"_"+year,";angle (degs); Relative Frequency (a.u.)",nbins,0,180) for i in xrange(0,len(energy_list))]
bg_hist_list = [TH1D("bg_hist_"+energy_list[i],";angle (deg); Relative Frequency",nbins,0,180) for i in xrange(0,len(energy_list))]



gRandom = TRandom3()

def calculate_angle(recozen,recoazi,mczen,mcazi):
    return np.arccos(np.sin(recozen)*np.sin(mczen)*np.cos(recoazi-mcazi) + np.cos(recozen)*np.cos(mczen))

def calculate_background_pdf(frame):
#        print("Computing PDF")
	time = frame.Get("I3EventHeader").start_time
        t_y = int(str(time)[0:4])
	sun_direction = astro.I3GetSunDirection(time)
	sun_zenith = sun_direction.zenith
	sun_azimuth = sun_direction.zenith
	reco_neutrino = frame.Get("IC86_Dunkman_L6_PegLeg_MultiNest8D_NumuCC")
	reco_zenith = reco_neutrino.dir.zenith
	reco_energy = reco_neutrino.energy
	#if year >= 2015:
	if t_y >= 2015:
		reco_energy *= 1.04
	counter = 0
	for pair in energy_range_list: 
		if reco_energy >= pair[0] and reco_energy <= pair[1]:
			for j in xrange(0,30):
				random_azimuth = gRandom.Uniform(0,2*pi)
				solar_angle = calculate_angle(reco_zenith,random_azimuth, sun_zenith, sun_azimuth)*180/pi
				bg_hist_list[counter].Fill(solar_angle)
		counter += 1
tray.AddModule("I3Reader", "reader",
    filenamelist=Infile_List)


tray.AddModule(event_cuts, "event_cuts")
tray.AddModule(calculate_background_pdf, "calculate_background_pdf")

tray.AddModule( 'TrashCan' , 'Done' )

if (params.NEvents==-1):
    tray.Execute()
else:
    tray.Execute(params.NEvents)

tray.Finish()

gStyle.SetOptStat(0)

import cPickle as pickle

#file = TFile("/mnt/home/neergarr/icecube/solarWIMP_systematics/background_pdfs/1D_bg_histogram_ch"+str(y)+"_"+year+".root","RECREATE")
file = TFile(out+"/1D_bg_histogram_ch"+str(y)+".root","RECREATE")
for j in xrange(0,len(energy_list)):
	bg_hist_list[j].Write()
file.Close()


