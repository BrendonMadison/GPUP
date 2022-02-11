from random import seed,gauss
from math import sqrt
from ROOT import gROOT,TFile,TH1D,TMath
from sys import version,argv
from histUtils import histInfo
import csv

print("Python version info: ",version)
print("ROOT version info: ",gROOT.GetVersion())


#Convert the values of the csv to a list of floats that can be manipulated
dm = []
dc = []
dmunc = []
dcunc = []
tmp = []
#arrays to keep the names of these columns
nm = []
nc = []
#row count variables
rc = 0
trc = 0.0
uncc = 0
#The correction factor from Cureton, Gurland, Tripathi
kn = 0.0

mname = str(argv[5])+'/Datm.csv'
cname = str(argv[5])+'/Datc.csv'
#Open it the first time to get the correction factor for these events
with open(mname) as mfile:
    reader = csv.reader(mfile,delimiter=',')
    trc = sum(1.0 for row in reader)
    kn = float(2.0 * (TMath.Gamma(trc/2.0) / TMath.Gamma((trc-1.0)/2.0))**2)
    print("Number of runs: ",trc," ",kn)

#Open second time to calculate the average value
with open(mname) as mfile:
    reader = csv.reader(mfile,delimiter=',')
    for row in reader:
        if rc == 0:
            for i in range(len(row)):
                if i%2 == 1:
                    val = row[i]
                    val = float(val.replace('D','E'))
                    dm.append(val)
                    #print(val)
                else:
                    nm.append(row[i])
            tmp.append(dm)
        else:
            tl = []
            for i in range(len(row)):
                if i%2 == 1:
                    val = row[i]
                    val = float(val.replace('D','E'))
                    tl.append(val)
                    #print(val)
            dm = [dm[j] + tl[j] for j in range(len(dm))]
            tmp.append(tl)
        rc += 1

#print(tmp)
dmave = [dm[i]/float(rc) for i in range(len(dm))]
#print(dmave)
#read through the rows again now that we know the average
rc = 0
tl = []
for row in tmp:
    if rc ==0:
        for i in range(len(row)):
            dmunc.append((row[i] - dmave[i])**2 / kn)
    else:
        tl = []
        for i in range(len(row)):
            tl.append((row[i] - dmave[i])**2 / kn)
        dmunc = [dmunc[i] + tl[i] for i in range(len(dmunc))]
    rc += 1

dmunc = [sqrt(dmunc[i]) for i in range(len(dmunc))]

rc = 0
tmp = []
#Open correlations to calculate the average value
with open(cname) as cfile:
    reader = csv.reader(cfile,delimiter=',')
    for row in reader:
        if rc == 0:
            for i in range(len(row)):
                if i%3 == 2:
                    val = row[i]
                    val = float(val.replace('D','E'))
                    dc.append(val)
                    #print(val)
                else:
                    nc.append(row[i])
            tmp.append(dc)
        else:
            tl = []
            for i in range(len(row)):
                if i%3 == 2:
                    val = row[i]
                    val = float(val.replace('D','E'))
                    tl.append(val)
                    #print(val)
            dc = [dc[j] + tl[j] for j in range(len(dc))]
            tmp.append(tl)
        rc += 1

#print(tmp)
dcave = [dc[i]/float(rc) for i in range(len(dc))]
#print(dmave)
#read through the rows again now that we know the average
rc = 0
tl = []
for row in tmp:
    if rc ==0:
        for i in range(len(row)):
            dcunc.append((row[i] - dcave[i])**2 / kn)
    else:
        tl = []
        for i in range(len(row)):
            tl.append((row[i] - dcave[i])**2 / kn)
        dcunc = [dcunc[i] + tl[i] for i in range(len(dcunc))]
    rc += 1

dcunc = [sqrt(dcunc[i]) for i in range(len(dcunc))]

print("Name of columns from Means",nm)
print("Sum of numbered columns: ",dm)
print("Average of numbered columns: ",dmave)
print("Uncertainies of columns: ",dmunc)

print("Name of columns from Corrs",nc)
print("Sum of numbered columns: ",dc)
print("Average of numbered columns: ",dcave)
print("Uncertainies of columns: ",dcunc)

print("Latex row code \n")

#format follows this:
#\multicolumn{1}{|c|}{Run Number} & \multicolumn{1}{l|}{Input Energy} & \multicolumn{1}{l|}{E1 Corr,E2 Corr} & \multicolumn{1}{c|}{Average E1/Eb} & \multicolumn{1}{l|}{Average E2/Eb} & \multicolumn{1}{l|}{z_pv (um)} & \multicolumn{1}{l|}{time} & \multicolumn{1}{l|}{\# of Events} & \multicolumn{1}{l|}{E1 E2 Corr.} & \multicolumn{1}{l|}{E1 z Corr.} & \multicolumn{1}{l|}{E2 z Corr.}  \\ \hline

ltable = "\multicolumn{1}{|c|}{"+str(argv[1])+"}         & \multicolumn{1}{c|}{"+str(argv[2]) + "}          & \multicolumn{1}{c|}{"+str(argv[3])+","+str(argv[4])+"}        & \multicolumn{1}{c|}{"+str("{:.4e}".format(dmave[0]))+"\pm"+str("{:.2e}".format(dmunc[0]))+"}     & \multicolumn{1}{c|}{"+str("{:.4e}".format(dmave[1]))+"\pm"+str("{:.2e}".format(dmunc[1]))+"}     & \multicolumn{1}{c|}{"+str("{:.4e}".format(dmave[4]))+"\pm"+str("{:.2e}".format(dmunc[4]))+"}     & \multicolumn{1}{c|}{"+str("{:.4e}".format(dmave[5]))+"\pm"+str("{:.2e}".format(dmunc[5]))+"}   & \multicolumn{1}{c|}{"+str("{:.4e}".format(dmave[12]))+"\pm"+str("{:.2e}".format(dmunc[12]))+"}    & \multicolumn{1}{c|}{"+str("{:.4e}".format(dcave[0]))+"\pm"+str("{:.2e}".format(dcunc[0]))+"}       & \multicolumn{1}{l|}{"+str("{:.4e}".format(dcave[3]))+"\pm"+str("{:.2e}".format(dcunc[3]))+"}   & \multicolumn{1}{l|}{"+str("{:.4e}".format(dcave[12]))+"\pm"+str("{:.2e}".format(dcunc[12]))+"} \\ \hline"

print(ltable)
