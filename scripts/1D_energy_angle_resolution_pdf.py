from I3Tray import *
from icecube import icetray, dataclasses, dataio
import glob
from ROOT import TH1D, TCanvas, TFile
import numpy as np
from icecube.dataclasses import *
from math import *
from event_cuts_l5_plus import *


dataset = 674
numu_list = glob.glob("/data/ana/BSM/IC86_LE_solarDM/MC/numu/14"+dataset+"/*.i3.bz2")
nue_list = glob.glob("/data/ana/BSM/IC86_LE_solarDM/MC/nue/12"+dataset+"/*.i3.bz2")
nutau_list = glob.glob("/data/ana/BSM/IC86_LE_solarDM/MC/nutau/14"+dataset+"/*.i3.bz2")
Infile_List = numu_list + nue_list + nutau_list

reco_mc_energy_histogram_list = [[TH1D("mc_energy_reco_"+str(i+1)+"_"+str(j),";neutrino energy (GeV);counts",200,0,200) for i in xrange(0,99)] for j in xrange(0,12)]
angle_mc_energy_histogram_list = [[TH1D("angle_mc_"+str(i)+"_"+str(j),";angle (degs);counts",180,0,180) for i in xrange(0,200)] for j in xrange(0,12)]


def calculate_angle(recozen,recoazi,mczen,mcazi):
	return np.arccos(np.sin(recozen)*np.sin(mczen)*np.cos(recoazi-mcazi) + np.cos(recozen)*np.cos(mczen))

def fill_histograms(frame):
	mctree = frame["I3MCTree"]
	mcparticle = get_most_energetic_primary(mctree)
	mcweightdict = frame["I3MCWeightDict"]
	if abs(mcparticle.type) == 14:
		ftype = 0
	if abs(mcparticle.type) == 12:
		ftype = 1
	if abs(mcparticle.type) == 16:
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
	mc_zenith = mcparticle.dir.zenith
	mc_azimuth = mcparticle.dir.azimuth
	mc_energy = mcparticle.energy
	pegleg_neutrino = frame["IC86_Dunkman_L6_PegLeg_MultiNest8D_NumuCC"]
	reco_zenith = pegleg_neutrino.dir.zenith
	reco_azimuth = pegleg_neutrino.dir.azimuth
	reco_energy = pegleg_neutrino.energy
	total_space_angle = calculate_angle(reco_zenith,reco_azimuth,mc_zenith,mc_azimuth)
	mc_energy_bin = reco_mc_energy_histogram_list[0][0].FindBin(mc_energy)-2
	if mc_energy_bin >= 0 and mc_energy_bin < 99:
		reco_mc_energy_histogram_list[ntype][mc_energy_bin].Fill(reco_energy, typeweight)
	reco_energy_bin = reco_mc_energy_histogram_list[ntype][0].FindBin(reco_energy)-1
	if reco_energy_bin >= 0 and reco_energy_bin < 200:
		angle_mc_energy_histogram_list[ntype][reco_energy_bin].Fill(float(total_space_angle*180/pi), typeweight)


tray = I3Tray()

tray.AddModule("I3Reader", "reader", filenamelist=Infile_List)
tray.AddModule(event_cuts, "event_cuts")
tray.AddModule(fill_histograms, "fill_histograms")

tray.AddModule( 'TrashCan' , 'Done' )

if (params.NEvents==-1):
    tray.Execute()
else:
    tray.Execute(params.NEvents)

tray.Finish()



file1 = TFile("/data/user/mnisa/SolarDM/energy_angle_resolutions/1D_energy_angle_resolution_"+dataset+".root","RECREATE")
for i in xrange(0,12):
	for j in xrange(0,99):
		reco_mc_energy_histogram_list[i][j].Write()
	for j in xrange(0,200):
		angle_mc_energy_histogram_list[i][j].Write()
file1.Close()
