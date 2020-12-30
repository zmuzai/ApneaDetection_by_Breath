# -*- coding: utf-8 -*
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from functions import start2end, Lowfilter


def stage2(PAS_data,Fs,isfigure=False):

    # # Calculate the envelope E3 according to the formula given in the paper
    e3_data = PAS_data**2
    e3_data = np.log(e3_data)
    
    
    # Perform band-pass filtering operation on envelope E3 with a cut-off frequency of 2Hz
    e3_data = Lowfilter(e3_data,Fs,2)
    if isfigure:
        plt.plot(e3_data,label='E3')
    
    # Calculate variable threshold
    e_PAS = np.log(sum(PAS_data**2)/len(PAS_data))
    mean_e3 = np.mean(e3_data)
    thr_e3 = np.mean(np.array([e_PAS, mean_e3]))
    

    # Segments below the threshold are apnea segments
    start, end = start2end(e3_data,thr_e3,10,Fs)
    
    if isfigure:
        for s in start:
            plt.axvline(s, color='grey', linestyle='--')
        for e in end:
            plt.axvline(e, color='grey', linestyle='--')
        
        for i in range(len(start)):
            plt.axvspan(start[i], end[i], alpha=0.3, color='grey')
        # set axis 
        plt.legend()
        xticks = np.array(list(range(0,len(PAS_data),5*Fs)))
        xticks = np.append(xticks, max(xticks)+5*Fs)
        xticklabes =  [str(i) for i in range(0,len(xticks)*5,5)]
        plt.xticks(xticks, xticklabes)
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.title('Apnea Segment')
        plt.show()

    return start, end


