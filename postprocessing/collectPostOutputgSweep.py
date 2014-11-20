#!/usr/bin/env python
"""
collectPostOutput.py

collect output from different runs & reps into single 
"""

import sys
import os
import numpy as np
import scipy.io
import matplotlib.pyplot as plt

#### config here
projName = "random_fine_g_sweep"
outFn = os.path.join(os.environ['HOME'], 'work', 'prebotc', 
                      'data', projName, 'post/collected.mat')

## setup variables
srcDir = os.path.join(os.environ['HOME'], 'work', 'prebotc', 'src')
iputFn = os.path.join(srcDir, 'pipeline', projName + "_collect_control")
postFn = os.path.join(srcDir, 'pipeline', projName + "_post")
errFn = os.path.join(srcDir, 'pipeline', projName + "_post_err")
## load
f = open(iputFn, 'r')
lines = f.readlines()
splitLines = np.array([ line.split() for line in lines ])
fp = open(postFn, 'r')
postLines = fp.readlines()
## casting as numpy array allows slicing
f.close()
fErr = open(errFn, 'w')
## get the parameters for which we will collect
ks = np.array(np.unique(splitLines[:,3]), dtype=np.float)
ks = np.sort(ks)
print "ks: " + str(ks)
pIs = np.array(np.unique(splitLines[:,4]), dtype=np.float)
pIs = np.sort(pIs)
print "pIs: " + str(pIs)
gEs = np.array(np.unique(splitLines[:,6]), dtype=np.float)
gEs = np.sort(gEs)
print "gEs: " + str(gEs)
gIs = np.array(np.unique(splitLines[:,7]), dtype=np.float)
gIs = np.sort(gIs)
print "gIs: " + str(gIs)
numk = len(ks)
numpI = len(pIs)
numgE = len(gEs)
numgI = len(gIs)
numRep = len(np.unique(splitLines[:,5]))
print "num k: " + str(numk)
print "num pI: " + str(numpI)
print "num gE: " + str(numgE)
print "num gI: " + str(numgI)
print "num rep: " + str(numRep)


## setup the collected arrays
chiArray = np.zeros((numk, numpI, numgE, numgI), dtype=np.float)
# dutyCycle = np.zeros((numk, numpI, numgE, numgI), dtype=np.float)
# muIBI = np.zeros((numk, numpI, numgE, numgI), dtype=np.float)
# cvIBI = np.zeros((numk, numpI, numgE, numgI), dtype=np.float)
# muB = np.zeros((numk, numpI, numgE, numgI), dtype=np.float)
# cvB = np.zeros((numk, numpI, numgE, numgI), dtype=np.float)
fMax = np.zeros((numk, numpI, numgE, numgI), dtype=np.float)
lag = np.zeros((numk, numpI, numgE, numgI), dtype=np.float)
op_angle_mean = np.zeros((numk, numpI, numgE, numgI), dtype=np.float)
op_angle_std = np.zeros((numk, numpI, numgE, numgI), dtype=np.float)
for i in range(len(splitLines)):
    run = splitLines[i,:]
    postFile = run[2]
    k = float(run[3])
    pI = float(run[4])
    gE = float(run[6])
    gI = float(run[7])
    idx = (np.where(ks == k), np.where(pIs == pI),
           np.where(gEs == gE), np.where(gIs == gI))
    try:
        M = scipy.io.loadmat(postFile)
        chiArray[idx] += float(M['chi'])
        # dutyCycle[idx] += float(M['duty_cycle'])
        # muIBI[idx] += float(M['ibi_mean'])
        # cvIBI[idx] += float(M['ibi_cv'])
        # muB[idx] += float(M['burst_length_mean'])
        # cvB[idx] += float(M['burst_length_cv'])
        fMax[idx] += float(M['peak_freq'])
        lag[idx] += float(M['peak_lag'])
        op_angle_mean[idx] += float(M['op_angle_mean'])
        op_angle_std[idx] += float(M['op_angle_std'])
    except IOError, KeyError:
        # simOutFn = run[1]
        # cmd = "./doPost.py " + simOutFn + " " + postFile + "\n"
        print postFile + " is missing, writing command:"
        cmd = postLines[i]
        print cmd
        fErr.write(cmd)

chiArray = np.divide(chiArray, numRep)
# dutyCycle = np.divide(dutyCycle, numRep)
# muIBI = np.divide(muIBI, numRep)
# cvIBI = np.divide(cvIBI, numRep)
# muB = np.divide(muB, numRep)
# cvB = np.divide(cvB, numRep)
fMax = np.divide(fMax, numRep)
lag = np.divide(lag, numRep)
op_angle_mean = np.divide(op_angle_mean, numRep)
op_angle_std = np.divide(op_angle_std, numRep)
X = np.transpose(np.tile(ks, (numpI, 1)))
Y = np.tile(pIs, (numk, 1))

fErr.close()

scipy.io.savemat(outFn,
                 mdict={'X':X,
                        'Y':Y,
                        'chiArray':chiArray,
                        # 'dutyCycle':dutyCycle,
                        # 'muIBI': muIBI,
                        # 'cvIBI': cvIBI,
                        # 'muB': muB,
                        # 'cvB': cvB,
                        'fMax': fMax,
                        'lag': lag,
                        'op_angle_mean': op_angle_mean,
                        'op_angle_std': op_angle_std,
                        'ks': ks,
                        'pIs': pIs,
                        'gEs': gEs,
                        'gIs': gIs})
