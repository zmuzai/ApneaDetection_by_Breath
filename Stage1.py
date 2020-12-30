# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from functions import start2end, inter, windowMean, envelope_extraction, windowRemoveValues
import warnings
warnings.filterwarnings("ignore")

def stage1(filter_data,Fs,plen=3,isfigure=False):
    # Select segments that may have apnea
    # 1、Calculate E1
    # （1）Calculate the average of the sliding window
    smooth_data, sample = windowMean(abs(filter_data),window=0.5,step=0.5,Fs=Fs)
    # （2）Perform cubic interpolation on the average to get the envelope
    inter_data = inter(sample,smooth_data,len(filter_data))
    
    if isfigure:
        # it_sample：Used to align the envelope and the mean point of the sliding window
        it_sample = np.array(list(range(sample[0],sample[-1],1)))
        plt.plot(it_sample,inter_data,label='out off E1',linestyle='-.', color='blue')
   
    # （3）Select the part of the above envelope that is lower than the mean value as E1
    mean_e1 = np.mean(inter_data)
    obj_index = np.argwhere(inter_data>mean_e1)
    inter_data[obj_index] = mean_e1
    
    if isfigure:
        plt.plot(it_sample,inter_data,label='E1', color='blue',lw=3)
    
    # (4)Determine the local maximum of E1 and interpolate it to get E2
    envelope_data = envelope_extraction(inter_data)
    
    if isfigure:
        plt.plot(it_sample,envelope_data,label='E2', color='red',lw=3)
    # （5）Calculate the average of E2
    mean_e2 = np.mean(envelope_data)
    start, end = start2end(envelope_data,mean_e2,5,Fs)
    start = start + sample[0]
    end = end + sample[0]
    
    if isfigure:
        for s in start:
            plt.axvline(s, color='grey', linestyle='--')
        for e in end:
            plt.axvline(e, color='grey', linestyle='--')
    
    # Get the start and end points of the PAS phase
    Lstart = start-(plen*Fs)
    Lend = end+(plen*Fs)
    
    # Remove the overlap between the start point and the end point
    if len(Lstart) >1:
        delidx = np.array([])
        for i in range(1,len(Lstart)):
            if Lstart[i] < Lend[i-1]:
                delidx = np.append(delidx,i)
        if len(delidx) != 0:
            Lstart = np.delete(Lstart, delidx)
            Lend = np.delete(Lend, (delidx-1))
    
    
    if isfigure:
        for s in Lstart:
            plt.axvline(s, color='grey', linestyle='--')
        for e in Lend:
            plt.axvline(e, color='grey', linestyle='--')
        
        for i in range(len(Lstart)):
            plt.axvspan(Lstart[i], Lend[i], alpha=0.3, color='grey')
        # set axis  
        plt.legend()
        xticks = np.array(list(range(0,len(filter_data),5*Fs)))
        xticks = np.append(xticks, max(xticks)+5*Fs)
        xticklabes =  [str(i) for i in range(0,len(xticks)*5,5)]
        plt.xticks(xticks, xticklabes)
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.title('Recognition of possible apnea phase')
        plt.show()
    
    return Lstart, Lend

# if __name__ == '__main__':
#     from functions import FIRfilter

#     data_path= 'data/breath_sound/breath_sound_5.npy'
#     Fs = 8000

#     # 加载数据
#     data = np.load(data_path)
#     L = len(data)/Fs
#     print('长度：%.4f s'%(L))

#     # 带通滤波
#     data = FIRfilter(data,Fs,200,2000)
#     X = windowRemoveValues(data,0.5,0.5,Fs,20)
#     start1, end1 = stage1(X,Fs,plen=5,isfigure=True)