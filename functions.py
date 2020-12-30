# -*- coding: utf-8 -*-
import numpy as np
from scipy.interpolate import interp1d



# Calculate the average of the sliding window
def windowMean(data,window,step,Fs):
    timestep = round(((len(data)/Fs)-window)/step)+1 # Number of sliding windows
    for i in range(0,timestep):
        if i==0:
            X = np.mean(data[round((i*step)*Fs):round((i*step+window)*Fs)])
            Y = round(((i*step+window)*Fs)/2)
        else:
            b = np.mean(data[round(i*step*Fs):round((i*step+window)*Fs)])
            X = np.hstack((X,b))
            y = round(((i*step+window)*Fs-i*step*Fs)/2)+round(i*step*Fs)
            Y = np.hstack((Y,y))
    return X,Y

# Remove outliers in the sliding window
def windowRemoveValues(data,window,step,Fs,nmax=10,cut_amp=2000,mul=15):
    timestep = round(((len(data)/Fs)-window)/step)+1  # Number of sliding windows
    for i in range(0,timestep):
        sp = round((i*step)*Fs)
        ep = round((i*step+window)*Fs)
        if i==0:
            X = data[sp:ep]
            n_temp = nmax
            if np.mean(abs(X)) < cut_amp:
                n_temp = nmax*mul
            temp = np.sort(abs(X))[-n_temp]
            idx = np.argwhere(abs(X)>temp)
            X[idx] = np.mean(abs(X))
            
        else:
            b = data[sp:ep]
            n_temp = nmax
            if np.mean(abs(X)) < cut_amp:
                n_temp = nmax*mul
            temp = np.sort(abs(b))[-n_temp]
            idx = np.argwhere(abs(b)>temp)
            b[idx] = np.mean(abs(b))
            X = np.hstack((X,b))
    return X





def envelope_extraction(signal):
    s = signal.astype(float)
    u_x = [0] 
    u_y = [s[0]] 

    for k in range(1,len(s)-1):
        if (s[k]>=s[k-1]) and (s[k]>=s[k+1]):
            u_x.append(k)
            u_y.append(s[k])


    u_x.append(len(s)-1)
    u_y.append(s[-1])

    u_x = np.array(u_x)
    u_y = np.array(u_y)
    inter_data = inter2(u_x,u_y,len(s))
    
    return inter_data




# Interpolation function
def inter(x,y,n,kind="cubic"):
    xnew = np.array(list(range(0,n,1)))
    f = interp1d(x,y,kind=kind,fill_value="extrapolate")
    # ‘slinear’, ‘quadratic’ and ‘cubic’ refer to a spline interpolation of first, second or third order)
    ynew=f(xnew)
    ynew = ynew[x[0]:x[-1]]
    return ynew

def inter2(x,y,n,kind="cubic"):
    xnew = np.array(list(range(0,n,1)))
    f = interp1d(x,y,kind=kind,fill_value="extrapolate")
    # ‘slinear’, ‘quadratic’ and ‘cubic’ refer to a spline interpolation of first, second or third order)
    ynew=f(xnew)
    return ynew

# Find the start and end points that meet a certain threshold
def start2end(data,thr,length,Fs):
    index = np.argwhere(data<thr)[:,0]
    start = np.array([])
    end = np.array([])
    
    start = np.append(start, index[0])
    
    temp1 = index[:-1]
    temp2 = index[1:]
    gap = temp2 - temp1
    inter_idx = np.argwhere(gap>1)
    
    for i in range(len(inter_idx)):
        start = np.append(start, temp2[inter_idx[i]])
        end = np.append(end, temp1[inter_idx[i]])
    
    if len(start) > len(end) and index[-1]!=start[-1]:
        end = np.append(end, index[-1])
    if len(start) > len(end) and index[-1]==start[-1]:
        start = np.delete(start, -1)
    
    gap_new = end-start
    idx = np.argwhere(gap_new >= length*Fs)[:,0]
    
    start = start[idx]
    end = end[idx]

    return start.astype(int), end.astype(int)



import biosppy.signals.tools as st


def FIRfilter(data, fs, low, high):
    res, _, _ = st.filter_signal(data, 
                                     ftype='FIR', 
                                     band='bandpass', 
                                     order=int(0.3 * fs),
                                     frequency=[low, high], 
                                     sampling_rate=fs)
    
    return res




def Lowfilter(data, fs, low):
    res, _, _ = st.filter_signal(data, 
                                     ftype='FIR', 
                                     band='lowpass', 
                                     order=int(0.3 * fs),
                                     frequency=low, 
                                     sampling_rate=fs)
    
    return res

