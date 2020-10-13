/*
compile with: g++ -std=c++0x -O3 -o 1D_signal_sensitivity 1D_signal_sensitivity.cpp `root-config --cflags --glibs`
If using array class: -std=c++0x
Input arguments are output text file name, mass index, dataset number
mass indices key is [0:100 GeV, 1:50,2:35,3:20,4:10,5:5 GeV]

Run with: ./1D_signal_sensitivity signal_sensi_mass_0_ch_11.txt 0 11 674

*/

#include <cmath>
#include <algorithm>
#include <vector>
//#include <array>
#include <fstream>
#include "TH1D.h"
#include "TCanvas.h"
#include "TFile.h"
#include <iostream>
#include "TRandom3.h"
#include "limits"
#include <sstream>
using namespace std;

char const *bg_hist_names[6] = {"bg_hist_100","bg_hist_50","bg_hist_35","bg_hist_20","bg_hist_10","bg_hist_5"};
char const *signal_histogram_names[6] = {"signal_hist_100","signal_hist_50","signal_hist_35","signal_hist_20","signal_hist_10","signal_hist_5"};

char const *critical_region_histogram_names[6] = {"critical_region_0","critical_region_1","critical_region_2","critical_region_3","critical_region_4","critical_region_5"};


const int NPseudoexperiments = 10000;
vector<int> ch11_events{7305,11800,13904,11697,6083,2284};
vector<int> ch5_events{16749,13699,10785,7158,3480};
vector<int> ch12_events{8710,25628,51703,66400,65433,24102};

bool sort_function (double a,double b) { return (a<b); }

int main(int argc, char* argv[])
{
	ofstream myfile;
	myfile.open (argv[1]);
	gRandom = new TRandom3(0);
    int channel = atoi(argv[3]);
    vector<int> NSamples;
    if(channel == 5)
    {
     	NSamples = ch5_events;
    }
    if(channel == 11)
    {
     	NSamples = ch11_events;
    }
    if(channel == 12)
    {
     	NSamples = ch12_events;
    }
    string nbins = "";
    if(channel == 5 || channel == 11)
    {
     	nbins = "_36bins";
    }
    stringstream bg_file_name;
    bg_file_name << "/data/user/mnisa/SolarDM/background_pdfs/1D_bg_histogram_ch"<<argv[3]<<".root";
    TFile *bg_pdf_file = new TFile(bg_file_name.str().c_str());
    stringstream signal_filename;
    signal_filename<<"/data/user/mnisa/SolarDM/signal_pdfs/1x674/1D_signal_histograms_ch"<<argv[3]<<nbins<<".root";
    TFile *signal_file = new TFile(signal_filename.str().c_str());
    TH1D *signal_pdf = (TH1D*)signal_file->Get(signal_histogram_names[atoi(argv[2])]);

    double norm = 1;
    double scale = norm/(signal_pdf->Integral());
    signal_pdf->Scale(scale);
    TH1D *background_pdf = (TH1D*)bg_pdf_file->Get(bg_hist_names[atoi(argv[2])]);
    scale = norm/(background_pdf->Integral());
    background_pdf->Scale(scale);
	stringstream critical_region_filename;
	critical_region_filename << "/data/user/mnisa/SolarDM/critical_region/1D_critial_region_"<<argv[3]<<"_"<<argv[4]<<".root";
    TFile *critical_region_file = new TFile(critical_region_filename.str().c_str());
    TH1D *critical_region_histogram = (TH1D*)critical_region_file->Get(critical_region_histogram_names[atoi(argv[2])]);
    vector<double> critical_value_vector;

	for(int i = 0; i < 1; i++)
	{
		vector<double> rank_vector;
		for(int j = 0; j < NPseudoexperiments; j++)
		{
			cout<<j<<endl;
			vector<double> angle_vector;

			for(int m = 0; m < NSamples[atoi(argv[2])];m++)
			{
				angle_vector.push_back(background_pdf->GetRandom());
			}

			vector<double> likelihood_vector;
			double max_likelihood = -numeric_limits<double>::infinity();
			double tmp_likelihood = max_likelihood;
			double event_counter = 0;
            double upper_bound = 250;
            int buffer_counter = 0;
            int buffer = 10;

            while((max_likelihood == tmp_likelihood) || (buffer_counter < buffer) || ((event_counter-buffer) <= upper_bound))
            {
				double likelihood = 0;
				int sample_counter = 0;
				for(int l = 0; l < (NSamples[atoi(argv[2])]); l++)
				{
					double angle = angle_vector[l];
					double background_probability = background_pdf->GetBinContent(background_pdf->FindBin(angle));
					double signal_probability = signal_pdf->GetBinContent(signal_pdf->FindBin(angle));
					double combined_probability = (double(event_counter)/NSamples[atoi(argv[2])])*signal_probability + (1-(double(event_counter)/NSamples[atoi(argv[2])]))*background_probability;
					likelihood += log(combined_probability);
				}

				//cout<<event_counter<<"\t"<<likelihood<<endl;
				tmp_likelihood = likelihood;
				likelihood_vector.push_back(likelihood);
				if(tmp_likelihood >= max_likelihood)
				{
					max_likelihood = tmp_likelihood;
					buffer_counter = 0;
				}
				else
				{
					buffer_counter++;
				}
				event_counter += 1;
			}
            bool found_critical_value = false;
            double likelihood_vector_size = likelihood_vector.size();
            for(int l = upper_bound; l >= 0; l--)
            {
             	double rank = likelihood_vector[l] - max_likelihood;
                if(rank >= critical_region_histogram->GetBinContent(critical_region_histogram->FindBin(l)))
                {
                    critical_value_vector.push_back(l);
                    found_critical_value = true;
                    break;
                }
            }
            if(found_critical_value == false)
            {
             	critical_value_vector.push_back(upper_bound);
            }


        }

    }
    for(int i = 0; i < critical_value_vector.size(); i++)
    {
     	myfile<<critical_value_vector[i]<<endl;
    }

	myfile.close();
	return 0;
}


