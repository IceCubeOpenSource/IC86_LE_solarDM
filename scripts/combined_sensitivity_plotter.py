from ROOT import TGraph,TCanvas,TMultiGraph,TFile,kBlue,kGreen,kMagenta,kBlack,TLegend,gStyle,gPad
from array import array
from math import *
sd_conversion_factor = [9.59e-029, 2.12e-028,5.28e-028,1.25e-027,2.29e-027,8.07e-027]



x = [5,10,20,35,50,100]
x_5 = [10,20,35,50,100]
x_array = array("d",x)
x_5_array = array("d",x_5)

pico_x = [5,10,20,35,50,100]
pico_y = [2e-39,8.68e-41,3.68e-41,3.34e-41,3.68e-41,5.5e-41]
pico_gr = TGraph(len(pico_x),array("d",pico_x),array("d",pico_y))
pico_gr.SetLineStyle(3)
pico_gr.SetLineWidth(3)
pico_gr.SetLineColor(kBlack)

marcel_x_array = array("d",[20,35,50,100])
marcel_y_array = array("d",[4.85e-40,1.35e-40,7.9e-41,2.91e-41])
marcel_gr = TGraph(len(marcel_x_array),marcel_x_array,marcel_y_array)
marcel_gr.SetLineColor(kBlue+3)
marcel_gr.SetLineStyle(7)
marcel_gr.SetLineWidth(3)
marcel_x_array_ch5 = array("d",[35,50,100])
marcel_y_array_ch5 = array("d",[92.5e-40,63.9e-40,32.9e-40])
marcel_gr_ch5 = TGraph(len(marcel_x_array_ch5),marcel_x_array_ch5,marcel_y_array_ch5)
marcel_gr_ch5.SetLineColor(kBlue+1)
marcel_gr_ch5.SetLineStyle(7)
marcel_gr_ch5.SetLineWidth(3)


sk_x_array = array("d",[4,6,10,20,50,100])
sk_x_array_ch5 = array("d",[6,10,20,50,100])
sk_y_array = array("d",[2.22e-40,1.63e-40,1.31e-40,1.42e-40,1.28e-40,1.24e-40])
sk_y_array_ch5 = array("d",[17.2e-40,14.9e-40,14.3e-40,23.4e-40,31.9e-40])
sk_gr = TGraph(len(sk_x_array),sk_x_array,sk_y_array)
sk_gr.SetLineColor(kMagenta+3)
sk_gr.SetLineStyle(2)
sk_gr.SetLineWidth(3)
sk_gr_ch5 = TGraph(len(sk_x_array_ch5),sk_x_array_ch5,sk_y_array_ch5)
sk_gr_ch5.SetLineColor(kMagenta+1)
sk_gr_ch5.SetLineStyle(2)
sk_gr_ch5.SetLineWidth(3)

livetime = 365.25*24*60*60

import json
ch11_signal_event_sensitivity = []
#filename = "/data/user/mnisa/SolarDM/sensitivity/1D_median_upper_limit_36bins.txt" 
filename = "/data/user/mnisa/SolarDM/sensitivity/1D_median_upper_limit_674_optimized_erange.txt" 
with open(filename,"r") as f:
	tmp_list = json.load(f)
	tmp_list.reverse()
	ch11_signal_event_sensitivity = tmp_list

import cPickle as pickle
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


	
color_array = [kGreen+2, kGreen+3, kGreen+1, kMagenta+2,kBlue+2, kMagenta+4, kBlue+4]

sd_graph_list = []
sd_graph_list.append(TGraph(len(x),x_array,array("d",ch11_sd_xsec)))
sd_graph_list[-1].SetLineWidth(3)
sd_graph_list[-1].SetLineColor(color_array[0])
sd_graph_list.append(TGraph(len(x),x_array,array("d",ch14_sd_xsec)))
sd_graph_list[-1].SetLineWidth(3)
sd_graph_list[-1].SetLineColor(color_array[1])
sd_graph_list.append(TGraph(len(x_5),x_5_array,array("d",ch5_sd_xsec)))
sd_graph_list[-1].SetLineWidth(3)
sd_graph_list[-1].SetLineColor(color_array[2])

print("tau tau")
print("Mass (GeV)","Sigma_sd (cm^2)")
for i,j in zip(x_array,ch11_sd_xsec):
    print(i,j)

print("nu nu")
print("Mass (GeV)","Sigma_sd (cm^2)")
for i,j in zip(x_array,ch14_sd_xsec):
    print(i,j)


print("b b")
print("Mass (GeV)","Sigma_sd (cm^2)")
for i,j in zip(x_5_array,ch5_sd_xsec):
    print(i,j)

print("ok")
exit()	
mg = TMultiGraph()
for i in range(0,len(sd_graph_list)):
	mg.Add(sd_graph_list[i])
mg.Add(marcel_gr)
mg.Add(marcel_gr_ch5)
mg.Add(sk_gr)
mg.Add(sk_gr_ch5)
mg.Add(pico_gr)

mg.SetTitle(";WIMP Mass (GeV/c^{2}); #sigma_{S.D.} (cm^{2})")
gStyle.SetLegendBorderSize(0)

c1 = TCanvas()
c1.SetLogy()



mg.Draw("al")
mg.GetYaxis().SetTitleOffset(1.3)
mg.GetXaxis().SetTitleOffset(1.2)
mg.GetYaxis().SetTitleSize(0.04)
mg.GetXaxis().SetTitleSize(0.04)
mg.GetYaxis().SetLabelSize(0.04)
mg.GetXaxis().SetLabelSize(0.04)
mg.GetYaxis().SetRangeUser(5e-42,5e-37);
gPad.Update()

l1 = TLegend(0.11,0.7,0.89,0.89)
l1.SetNColumns(4)
l1.AddEntry(sd_graph_list[0],"#tau^{+}#tau^{-}","l")
l1.AddEntry(sd_graph_list[1],"#nu#bar{#nu}","l")
l1.AddEntry(sd_graph_list[2],"b#bar{b}","l")
l1.AddEntry(marcel_gr,"IC 2017 #tau^{+}#tau^{-}","l")
l1.AddEntry(marcel_gr_ch5,"IC 2017 b#bar{b}","l")
l1.AddEntry(sk_gr,"SK 2015 #tau^{+}#tau^{-}","l")
l1.AddEntry(sk_gr_ch5,"SK 2015 b#bar{b}","l")
l1.AddEntry(pico_gr,"PICO-60 2017","l")
l1.Draw("sames")
c1.Update()
c1.SaveAs("sensitivity_comparison_new.png")
#c1.BuildLegend()
#raw_input()


