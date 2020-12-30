# -*- coding: utf-8 -*-
import numpy as np
from Stage1 import stage1
from Stage2 import stage2
import matplotlib.pyplot as plt
import sys
import time;
from functions import FIRfilter, windowRemoveValues 
start_time = time.time()

data_path= 'breath_sound_1.npy'

Fs = 8000
isfig = False
# load data
data = np.load(data_path)

L = len(data)/Fs
print('长度：%.4f s'%(L))
# band pass filter
data = FIRfilter(data,Fs,200,2000)
# Remove outliers in the sliding window
data = windowRemoveValues(data,0.5,0.5,Fs,20)

# stage1：Get possible segments of apnea, namely PAS
start1, end1 = stage1(data,Fs,plen=5)
if len(start1) ==0:
    print('No Apnea')
    sys.exit(0)

# stage2：Get segments of apnea
start2, end2 = np.array([]),np.array([])
for i in range(len(start1)):
    PAS_data = data[start1[i]:end1[i]]
    s, e = stage2(PAS_data,Fs)
    start2 = np.append(start2,s)
    end2 = np.append(end2,e)

# Start and end points of apnea
Apnea_start = (start1+start2).astype(int)
Apnea_end = (start1+end2).astype(int)

# If the duration is less than 10s, it is considered that there is no apnea
Apnea_times = (Apnea_end-Apnea_start)/Fs
if len(np.argwhere(Apnea_times >= 10))>0:
    print('Time:',Apnea_times[np.argwhere(Apnea_times >= 10)])
else:
    print('No Apnea')
    sys.exit(0)

if isfig:
    data = np.load(data_path)

    data = FIRfilter(data,Fs,200,2000)
    l1, = plt.plot(data)
    for i in range(len(Apnea_start)):
        PAS_data = data[start1[i]:end1[i]]
        Apnea_data = data[Apnea_start[i]:Apnea_end[i]]
        Apnea_sample = np.array(list(range(Apnea_start[i],Apnea_end[i],1)))
        PAS_sample = np.array(list(range(start1[i],end1[i],1)))
        l2, = plt.plot(PAS_sample,PAS_data,color='g')
        l3, = plt.plot(Apnea_sample,Apnea_data,color='r')
        
    # set axis  
    plt.legend(handles=[l1, l2, l3], labels=['data','PAS','Apnea'])
    xticks = np.array(list(range(0,len(data),5*Fs)))
    xticks = np.append(xticks, max(xticks)+5*Fs)
    xticklabes =  [str(i) for i in range(0,len(xticks)*5,5)]
    plt.xticks(xticks, xticklabes)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.title('Apnea Segment')
    plt.show()

end_time = time.time()
print('The code run:{:.2f}s'.format(end_time-start_time))