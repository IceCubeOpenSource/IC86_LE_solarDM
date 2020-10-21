"""
Title: solarWIMP pdfs
Author: Garrett Neer
Date Created: 11-5-15
Last Modified: 7-25-18
Purpose: Create the signal probability distribution functions for a solar WIMP analysis. 
The signal distribution is estimated by using the total space angle distribution between mc particles and reco particles,
where events are reweighted using the solar WIMP flux calculated using DarkSUSY.
There will be a different signal pdf for every wimp mass and annihilation channel considered.
"""

#!/usr/bin/env python
import numpy as np
import glob
from I3Tray import *
from icecube import icetray, dataclasses, dataio
from math import *
from ROOT import TH1D, TFile
from icecube.dataclasses import *

from event_cuts_l5_plus import *

out = 'signal_pdfs'

if not os.path.exists(out):
   os.makedirs(out)


dataset = '674' #baseline genie dataset number is 674
numu_list = glob.glob("/data/ana/BSM/IC86_LE_solarDM/MC/numu/14"+dataset+"/*.bz2")
nue_list = glob.glob("/data/ana/BSM/IC86_LE_solarDM/MC/nue/12"+dataset+"/*.bz2")
nutau_list = glob.glob("/data/ana/BSM/IC86_LE_solarDM/MC/nutau/16"+dataset+"/*.bz2")
numu_files = len(numu_list)
nue_files = len(nue_list)
nutau_files = len(nutau_list)
Infile_List = numu_list + nue_list + nutau_list

tray = I3Tray()

masschan = [(10, 5), (20, 5), (35, 5), (50, 5), (100, 5)]

signal_weight_array = [0.0 for x in range(len(masschan))]

n_bins = 36

energy_range_list = [(0,11),(0,18),(0,27),(3,38),(6,70)]

index_1_name = ["cascade","track"]
index_2_name = ["10","20","35","50","100"]
signal_histogram_list = []
for i in xrange(0,len(index_2_name)):
	signal_histogram_list.append(TH1D("signal_hist_"+index_2_name[i],";angle (degs);Relative Frequency (a.u.)",n_bins,0,180))


zen_pdf = []
flux_width = 0.01
zenith_width = pi/180
wimpsim_fluxes = []

file = TFile("/data/user/mnisa/SolarDM/wimpsim_fluxes/wimpsim_fluxes_ch5.root")
zenith_pdf = file.Get("zenith_pdf")
wimpsim_flux_names = ["numuCC","numubarCC","nueCC","nuebarCC","nutauCC","nutaubarCC","numuNC","numubarNC","nueNC","nuebarNC","nutauNC","nutaubarNC"]
for x in range(0,len(masschan)):
	for i in range(0,len(wimpsim_flux_names)):
		histogram_name = wimpsim_flux_names[i]+"_m"+str(masschan[x][0])+"_ch"+str(masschan[x][1])
		wimpsim_fluxes.append(file.Get(histogram_name))



def calculate_angle(recozen,recoazi,mczen,mcazi):
	return np.arccos(np.sin(recozen)*np.sin(mczen)*np.cos(recoazi-mcazi) + np.cos(recozen)*np.cos(mczen))

def calculate_signal_pdfs(frame):
	mctree = frame["I3MCTree"]
	mcparticle = get_most_energetic_primary(mctree)
	mcweightdict = frame["I3MCWeightDict"]
	if abs(mcparticle.type) == 14:
		infile_list_length = numu_files
		ftype = 0
	if abs(mcparticle.type) == 12:
		infile_list_length = nue_files
		ftype = 1
	if abs(mcparticle.type) == 16:
		infile_list_length = nutau_files
		ftype = 2
	if mcparticle.type > 0:
		typeweight = 0.7
		qtype = 0
	if mcparticle.type < 0:
		qtype = 1
		typeweight = 0.3
	if mcweightdict["InteractionType"] == 1.0:
		itype = 0
	if mcweightdict["InteractionType"] == 2.0:
		itype = 1
	if mcweightdict["InteractionType"] == 0.0:
		return False
	ntype = 6*itype + 2*ftype + qtype
	pegleg_neutrino = frame["IC86_Dunkman_L6_PegLeg_MultiNest8D_NumuCC"]
	reco_zenith = pegleg_neutrino.dir.zenith
	reco_azimuth = pegleg_neutrino.dir.azimuth
	reco_energy = pegleg_neutrino.energy
	mc_zenith = mcparticle.dir.zenith
	mc_azimuth = mcparticle.dir.azimuth
	total_space_angle = calculate_angle(reco_zenith,reco_azimuth,mc_zenith,mc_azimuth)
	mc_energy = mcparticle.energy
	for x in xrange(len(masschan)):
		z = mc_energy/masschan[x][0]
		if z <= 1 and reco_energy >= energy_range_list[x][0] and reco_energy <= energy_range_list[x][1]:
			bin = wimpsim_fluxes[12*x+ntype].FindBin(z)
			flux = wimpsim_fluxes[12*x+ntype][bin]
			bin = zenith_pdf.FindBin(mc_zenith*180/pi)
			exposure = zenith_pdf[bin]
			bin_center = zenith_pdf.GetBinCenter(bin)
			bin_edge_left = bin_center - 0.5
			bin_edge_right = bin_center + 0.5
			solid_angle = 2*pi*(cos(bin_edge_left*pi/180)-cos(bin_edge_right*pi/180))
			weight = flux*exposure*mcweightdict["OneWeight"]/(solid_angle*masschan[x][0]*mcweightdict["NEvents"]*infile_list_length*typeweight)
			signal_weight_array[x] += weight
			signal_histogram_list[x].Fill(float(total_space_angle*180/pi),weight)

tray.AddModule("I3Reader", "reader",
    filenamelist=Infile_List)


tray.AddModule(event_cuts, "event_cuts")
tray.AddModule(calculate_signal_pdfs, "calculate_signal_pdfs")

tray.AddModule( 'TrashCan' , 'Done' )
tray.Execute()


tray.Finish()




file = TFile(out+"/1D_signal_histograms_ch5_"+str(n_bins)+"bins.root","RECREATE")
for i in xrange(0,len(masschan)):
        scale = 1/(signal_histogram_list[i].Integral())
        signal_histogram_list[i].Scale(scale)
	signal_histogram_list[i].Write()

file.Close()
