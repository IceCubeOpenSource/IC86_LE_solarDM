# IC86_LE_solarDM
Code for the low-energy SolarDM analysis (2020) using the modified DRAGON sample.

Requirements:Icetray Environment with ROOT.

Suggested setup:
`/cvmfs/icecube.opensciencegrid.org/py2-v3.1.1/setup.sh`
=======

Requirements:Icetray Environment with ROOT.

`/cvmfs/icecube.opensciencegrid.org/py2-v3.1.1/RHEL_7_x86_64/metaprojects/combo/stable/env-shell.sh`

Paths to the genie mc and dragon data files are hard-coded in the scripts and should be edited accordingly.

## Analysis Wiki [https://wiki.icecube.wisc.edu/index.php/IC86_MSU_Solar_WIMP_Search]

The analysis scripts are located in the ```scripts``` directory

Background and signal pdfs have already been generated and located under their corresponding directories: ```background_pdfs``` and ```signal_pdfs```. However, the steps to generate them from data/MC from scratch are described below.

# Generating background and signal pdfs


* generate_bkg_pdf.py is used to produce the background pdf for a given input channel. Edit channel in line 26.

* solarWIMP_pdfs_ch11(5).py produce the signal pdfs for bb and tau tau for all masses.

* For the nu-nu channel, the signal pdf generation is a two-step process: 1) Run 1D_energy_angle_resolution_pdf.py 2) Use the root output of 1) as input for solarWIMP_pdfs_nunu.py

# Sensitivity calculation:
* 1D_signal_sensitivity.cpp is used to sample from background pdf to calculate sensitivity.
See compilation instructions at the top of the file. Change NPseudoexperiments to a small value (< 100) for testing. Otherwise submit as jobs on the cluster.

compile with: ```g++ -std=c++0x -O3 -o 1D_signal_sensitivity 1D_signal_sensitivity.cpp `root-config --cflags --glibs````

Input arguments are: output text file name, mass index, dataset number
mass indices key is [0:100 GeV, 1:50,2:35,3:20,4:10,5:5 GeV]

Run with: ```./1D_signal_sensitivity signal_sensi_mass_0_ch_11.txt 0 11 674```

* Run median_upperlim.py on the output of the previous step to calculate median signal events.

Finally,

* combined_sensitivity_plotter.py is used to calculate the cross-section upper limits. This script can be run directly to print the pre-unblinding sensitivity for all channels.

* plot_limits.py is used to plot the pre-saved sensitivities/upperlimits
