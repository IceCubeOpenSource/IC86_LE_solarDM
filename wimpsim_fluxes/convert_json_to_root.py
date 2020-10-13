from ROOT import TFile, TH1D
import simplejson

masschan = [(1000, 11),
            (500,11),
            (250,11),
            (100,11),
            (50,11),
            (35, 11),
            (20, 11),
            (10, 11),
			(5, 11)
        		]

neutrino_flux_names = ["numu","numubar","nue","nuebar","nutau","nutaubar"]
neutrino_weight_names = ["numuCC","numubarCC","nueCC","nuebarCC","nutauCC","nutaubarCC","numuNC","numubarNC","nueNC","nuebarNC","nutauNC","nutaubarNC"]
neutrino_weights_root = [[TH1D(neutrino_weight_names[i]+"_m"+str(masschan[j][0])+"_ch"+str(masschan[j][1]),";z (E_{#nu}/m_{#chi});dN/dz (cm^{-3}ann^{-1})",100,0,1) for i in range(0,12)] for j in range(0,len(masschan))]
zen_pdf_root = TH1D("zenith_pdf",";sun zenith (degs);dN/d#theta",180,0,180)

for x in range(0,len(masschan)):
	mass = masschan[x][0]
	channel = masschan[x][1]
	with open("/mnt/home/neergarr/icecube/solarWIMP/wimpsim_fluxes/wimpsim_neutrino_fluxes_cc_m%d_ch%d.simplejson" %(mass,channel),"r") as f:
		data = simplejson.load(f)
		for i in range(0,len(neutrino_flux_names)):
			flux = data[neutrino_flux_names[i]]
			for j in range(0,len(flux)):
				neutrino_weights_root[x][i].Fill(j*0.01+0.005,flux[j])
		if x == 0:
			zen_pdf = data["zen_pdf"]
			for i in range(0,len(zen_pdf)):
				zen_pdf_root.Fill(i,zen_pdf[i])
	with open("/mnt/home/neergarr/icecube/solarWIMP/wimpsim_fluxes/wimpsim_neutrino_fluxes_nc_m%d_ch%d.simplejson" %(mass,channel),"r") as f:
		data = simplejson.load(f)
		for i in range(0,len(neutrino_flux_names)):
			flux = data[neutrino_flux_names[i]]
			for j in range(0,len(flux)):
				neutrino_weights_root[x][i+6].Fill(j*0.01+0.005,flux[j])

file = TFile("wimpsim_fluxes.root","RECREATE")
for x in range(0,len(masschan)):
	for i in range(0,len(neutrino_weights_root[x])):
		neutrino_weights_root[x][i].Write()
zen_pdf_root.Write()
file.Close()
