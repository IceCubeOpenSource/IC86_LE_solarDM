from ROOT import TFile,TH1D
import sys

out = 'signal_pdfs'
if not os.path.exists(out):
   os.makedirs(out)

dataset = 674
reco_mc_energy_histogram_list = []
angle_mc_energy_histogram_list = []
file1 = TFile("/data/user/mnisa/SolarDM/energy_angle_resolutions/1D_energy_angle_resolution_"+dataset+".root")
for j in xrange(0,12):
	for i in xrange(0,99):
		reco_mc_energy_histogram_name = "mc_energy_reco_"+str(i+1)
		reco_mc_energy_histogram_list.append(file1.Get(reco_mc_energy_histogram_name))
	for i in xrange(0,200):
		angle_mc_energy_histogram_name = "angle_mc_"+str(i+1)
		angle_mc_energy_histogram_list.append(file1.Get(angle_mc_energy_histogram_name))

masschan = [(5,12),(10,12),(20,12),(35,12),(50,12),(100,12)]


energy_range_list = [(2,11),(0,23),(13,39),(25,70),(42,86),(83,167)]

wimpsim_fluxes = []

file2 = TFile("/data/user/mnisa/SolarDM/wimpsim_fluxes/wimpsim_fluxes_ch12.root")
wimpsim_flux_names = ["numuCC","numubarCC","nueCC","nuebarCC","nutauCC","nutaubarCC","numuNC","numubarNC","nueNC","nuebarNC","nutauNC","nutaubarNC"]

for x in range(0,len(masschan)):
    for i in range(0,len(wimpsim_flux_names)):
        histogram_name = wimpsim_flux_names[i]+"_m"+str(masschan[x][0])+"_ch"+str(masschan[x][1])
        wimpsim_fluxes.append(file2.Get(histogram_name))

index_2_name = ["5","10","20","35","50","100"]
signal_histogram_list = [TH1D("signal_hist_"+index_2_name[j],";angle (degs);Relative Frequency (a.u.)",180,0,180) for j in xrange(0,6)]


events = [287.2672032950843*744.0/10, 124.61986741903713*744.0/10, 177.77639100702692*300.0/10, 78.05075885214798*300.0/10, 153.43032264600362*60.0/10, 75.39439102892796*60.0/10, 34.962108010527096*744.0/10, 11.575085013911819*744.0/10, 8.308757479455354*300.0/10, 2.4817701025399392*300.0/10, 51.88500460784535*60.0/10, 15.244591601276232*60.0/10]
for i in range(0,12):
	print(i)
	for j in range(0,10*int(events[i])):
		for k in xrange(0,6):
			energy = wimpsim_fluxes[i].GetRandom()
			flux = wimpsim_fluxes[i].GetBinContent(wimpsim_fluxes[i].FindBin(energy))
			energy = energy*masschan[k][0]
			mc_energy_bin = reco_mc_energy_histogram_list[0].FindBin(energy)-1
			if mc_energy_bin >= 0 and mc_energy_bin < 99:
				reco_energy = reco_mc_energy_histogram_list[mc_energy_bin].GetRandom()
			if reco_energy >= energy_range_list[k][0] and reco_energy <= energy_range_list[k][1]:
				reco_energy_bin = reco_mc_energy_histogram_list[0].FindBin(reco_energy)-1
				if reco_energy_bin >= 0 and reco_energy_bin < 200:
					angle = angle_mc_energy_histogram_list[reco_energy_bin].GetRandom()					
					signal_histogram_list[k].Fill(angle,flux)

file3 = TFile(out+"sig_pdf_ch12_"+dataset+".root","RECREATE")
for i in xrange(0,len(masschan)):
	signal_histogram_list[i].Write()

file3.Close()
file1.Close()
file2.Close()

