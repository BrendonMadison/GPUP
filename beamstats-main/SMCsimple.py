import numpy as np
import math
import random
from scipy.special import comb
from scipy import stats
import statistics as st
from math import sqrt
from scipy.special import gamma
from sys import version,argv
from itertools import combinations
import csv

print("Python version info: ",version)

#Convert the values of the csv to a list of floats that can be manipulated
dm,dm1,dm2 = [],[],[]
dc,dc1,dc2 = [],[],[]
dmunc = []
dcunc = []
tmp = []
#-value lists
pvm, pvc = [],[]
#arrays to keep the names of these columns
nm = []
nc = []
#row count variables
rc = 0
trc = 0.0
uncc = 0
#The correction factor from Cureton, Gurland, Tripathi
kn = 0.0

#These are the run values you are computing for
mname = str(argv[5])+'/Datm.csv'
cname = str(argv[5])+'/Datc.csv'
mout = str(argv[5])+'/'+str(argv[1])+'m.csv'
cout = str(argv[5])+'/'+str(argv[1])+'c.csv'
lout = str(argv[5])+'/'+str(argv[1])+'LatexTables.txt'
#These are the run values that you are comparing to
mname1 = str(argv[6])+'/Datm.csv'
cname1 = str(argv[6])+'/Datc.csv'

#Open it the first time to get the correction factor for these events
with open(mname) as mfile:
    reader = csv.reader(mfile,delimiter=',')
    trc = sum(1.0 for row in reader)
    kn = float(2.0 * (gamma(trc/2.0) / gamma((trc-1.0)/2.0))**2)
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

dmunc = [sqrt(dmunc[i] / float(len(dmunc))) for i in range(len(dmunc))]

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

dcunc = [sqrt(dcunc[i] / float(len(dcunc))) for i in range(len(dcunc))]

print("Name of columns from Means",nm)
print("Sum of numbered columns: ",dm)
print("Average of numbered columns: ",dmave)
print("Uncertainies of columns: ",dmunc)

print("Name of columns from Corrs",nc)
print("Sum of numbered columns: ",dc)
print("Average of numbered columns: ",dcave)
print("Uncertainies of columns: ",dcunc)

####BEGIN PERMUTATION TEST SECTION####

#First we need to read in the second (reference) values

#Open original file to import and format their values
with open(mname) as mfile:
    reader = csv.reader(mfile,delimiter=',')
    for row in reader:
        rowval = []
        for i in range(len(row)):
            if i%2 == 1:
                val = row[i]
                val = float(val.replace('D','E'))
                rowval.append(val)
        dm1.append(rowval)

with open(cname) as cfile:
    readerc = csv.reader(cfile,delimiter=',')
    for row in readerc:
        rowval = []
        for i in range(len(row)):
            if i%3 == 2:
                val = row[i]
                val = float(val.replace('D','E'))
                rowval.append(val)
        dc1.append(rowval)

#Write the values to output files
with open(mout,'w') as mfout:
    writer = csv.writer(mfout,delimiter=',')
    for item in dm1:
        writer.writerow(item)

with open(cout,'w') as cfout:
    writerc = csv.writer(cfout,delimiter=',')
    for item in dc1:
        writerc.writerow(item)

#Open reference file to import and format their values
with open(mname1) as mfile:
    reader = csv.reader(mfile,delimiter=',')
    for row in reader:
        rowval = []
        for i in range(len(row)):
            if i%2 == 1:
                val = row[i]
                val = float(val.replace('D','E'))
                rowval.append(val)
        dm2.append(rowval)

with open(cname1) as cfile:
    reader = csv.reader(cfile,delimiter=',')
    for row in reader:
        rowval = []
        for i in range(len(row)):
            if i%3 == 2:
                val = row[i]
                val = float(val.replace('D','E'))
                rowval.append(val)
        dc2.append(rowval)

print(dm1)
print(dm2)
print(dc1)
print(dc2)

#Addresses of mean values we care about
madds = [0,1,4,5,6,7,8]
#Addresses of correlation values we care about
cadds = [0,3,9,5,11,24]

for k in range(int(len(madds)+len(cadds))):
 # Read data from two separate files.
 if k < len(madds):
     xnp = np.array([item[madds[k]] for item in dm1])
     ynp = np.array([item[madds[k]] for item in dm2])
 else:
     xnp = np.array([item[cadds[int(k-len(madds))]] for item in dc1])
     ynp = np.array([item[cadds[int(k-len(madds))]] for item in dc2])
 znp = np.append(xnp,ynp)

 print(xnp,ynp)
 
 x = []; y = []; z = []
 x = xnp.tolist()
 y = ynp.tolist()
 z = znp.tolist()

 print('x:',x)
 print('y:',y)
 print('z:',z)
 print('x, N:',len(x),'mean:',st.mean(x),'median:',st.median(x),'var:',st.variance(x))
 print('y, N:',len(y),'mean:',st.mean(y),'median:',st.median(y),'var:',st.variance(y))
 print('z, N:',len(z),'mean:',st.mean(z),'median:',st.median(z),'var:',st.variance(z))
 zcopy = z.copy()
 zcopy.sort()
 print('z sorted ',zcopy)
 nx = len(x); ny = len(y); N = nx+ny
 print('N,nx,ny:',N,nx,ny)
 print('Combinations (N_choose_nx):',comb(N,nx,exact=True))
 Nperms = comb(N,nx,exact=True)

 # First let's apply classic tests. Both implemented as 2-sided.
 print('Students t-test: ',stats.ttest_ind(x,y))                    # Student's t-test
 print('Welchs t-test:   ',stats.ttest_ind(x,y,equal_var=False))    # Welch's t-test
 print('Wilcoxon rank-sum test:  ',stats.ranksums(x,y))             # Wilcoxon rank-sum test
 print('Mann-Whitney U-test:  ',stats.mannwhitneyu(x,y))             # Mann-Whitney U-test

 # Redo these as exact tests using all combinations of potential partitions
 #The below do not work because HPC doesn't have scipy v1.7
 dp=1/Nperms
 print('Single occurrence p-value quantization = ',dp)
 #print('Exact version of Students t-test: ',stats.ttest_ind(x,y,permutations=Nperms))        # Exact Student's t-test
 #print('Exact version of Welchs t-test  : ',stats.ttest_ind(x,y,equal_var=False,permutations=Nperms))  # Exact Welch's t-test
 #print('Exact version of Mann-Whitney U-test:  ',stats.mannwhitneyu(x,y,method='exact'))             # Exact Mann-Whitney U-test

 # Calculate the 3 observed statistics
 T1Obs = st.mean(x)   - st.mean(y)
 T2Obs = st.median(x) - st.median(y)
 T3Obs = T1Obs/math.sqrt( (st.variance(x)/float(len(x))) + (st.variance(y)/float(len(y))) )

 print('mean(x) - mean(y)  T1Obs:',T1Obs)
 print(' med(x) -  med(y)  T2Obs:',T2Obs)
 print(' Welch t           T3Obs:',T3Obs)

 # Now let's look more carefully at these definitions.
 # https://en.wikipedia.org/wiki/Student%27s_t-test 
 # They differ for sure when nx != ny. 

 spB = math.sqrt( ((nx-1)*st.variance(x) + (ny-1)*st.variance(y))/(nx+ny-2) )
 sDelta = math.sqrt( ( st.variance(x)/nx ) + ( st.variance(y)/ny ) )

 # Equal variance version (Student's t-test)
 t1 = (st.mean(x) - st.mean(y)) / (spB*math.sqrt((1/nx) + (1/ny)))
 print('nx,ny,spB,Student t1:',nx,ny,spB,t1)

 # Unequal variance version (Welch's t-test)
 t2 = (st.mean(x) - st.mean(y)) / sDelta
 print('nx,ny,sDelta,Welch t2:',nx,ny,sDelta,t2)

 T1List = []
 T2List = []
 T3List = []
 n1 = 0
 n2 = 0
 n3 = 0
 ntot = comb(N,nx,exact=True)
 EPS = 1.0e-12                  # Allow for machine precision issues 

 debug = False

 icombo=0
 for i in combinations(z,nx):   # Enumerate all combinations of partitions into two groups of size nx and ny
     icombo +=1
     ilist = list(i)            # make the permuted version for x
     jlist = z.copy()           # make the complementary permuted list for y
     for element in ilist:
         if element in jlist:
             jlist.remove(element)
     T1 = st.mean(ilist)   - st.mean(jlist)
     T1List.append(T1)
 # note we use abs below to do 2-sided tests    
     T2 = st.median(ilist) - st.median(jlist)
     T2List.append(T2)
     T3 = T1/math.sqrt( (st.variance(ilist)/nx) + (st.variance(jlist)/ny) )
     T3List.append(T3)
     if abs(T1) >= abs(T1Obs)-EPS:
        n1 += 1
        if debug:
           print('Significant T1 ',T1,'for icombo ',icombo,ilist,jlist)             
     if abs(T2) >= abs(T2Obs)-EPS: n2 += 1
     if abs(T3) >= abs(T3Obs)-EPS: 
        n3 += 1
        if debug:
           print('Significant T3 ',T3,'for icombo ',icombo,ilist,jlist)       

 # Range checks
 print('min values ',min(T1List),min(T2List),min(T3List))
 print('max values ',max(T1List),max(T2List),max(T3List)) 
 print('length     ',len(T1List),len(T2List),len(T3List)) 

 print('p-value for T1 ',n1/ntot,n1,ntot)
 print('p-value for T2 ',n2/ntot,n2,ntot)
 print('p-value for T3 ',n3/ntot,n3,ntot)

 if k < len(madds):
     _, temppval = stats.ttest_ind(x,y,equal_var=False)
     pvm.append([n3/ntot,temppval])
 else:
     _, temppval = stats.ttest_ind(x,y,equal_var=False)
     pvc.append([n3/ntot,temppval])
 
 #Generate a table of statistical values:

 print("Stats table below")
 print("")
 print("\multicolumn{1}{|c|}{"+str(argv[1])+"}         &")
 print("\multicolumn{1}{|c|}{"+str(argv[6]) + "}          &")
 print("\multicolumn{1}{|c|}{"+str(Nperms)+"}        &")
 _, pvalprint = stats.ttest_ind(x,y)
 print("\multicolumn{1}{|c|}{"+str(pvalprint)+"}        &")
 _, pvalprint = stats.ttest_ind(x,y,equal_var=False)
 print("\multicolumn{1}{|c|}{"+str(pvalprint)+"}        &")
 _, pvalprint = stats.ranksums(x,y)
 print("\multicolumn{1}{|c|}{"+str(pvalprint)+"}        &")
 _, pvalprint = stats.mannwhitneyu(x,y)
 print("\multicolumn{1}{|c|}{"+str(pvalprint)+"}        &")
 print("\multicolumn{1}{|c|}{"+str(dp)+"}        &")

#Writing latex table code to separate file
with open(lout, 'w') as lf:
    lf.write('Latex row code\n')
    lf.write('For reference, pvalues are the permutation test p-value and Welch t-test p-value\n') 
    lf.write('Format follows the following. For means table:\n')
    lf.write('\begin{tabular}{|ccccccccccll}\n\n \hline \n\multicolumn{10}{|c|}{Guinea Pig Means Table} \\ \hline \n')
    lf.write('\multicolumn{1}{|c|}{Run \#} &\n')
    lf.write('\multicolumn{1}{|c|}{Input Energy} &\n')
    lf.write('\multicolumn{1}{|c|}{$E_1$ Corr,$E_2$ Corr} &\n')
    lf.write('\multicolumn{1}{|c|}{Average $\frac{E_1}{E_b}$} &\n')
    lf.write('\multicolumn{1}{|c|}{Average $\frac{E_2}{E_b}$} &\n')
    lf.write('\multicolumn{1}{|c|}{$z_{pv}$ (um)} &\n')
    lf.write('\multicolumn{1}{|c|}{Time} &\n')
    lf.write('\multicolumn{1}{|c|}{$\frac{\sqrt{s}}{\sqrt{s}_b}$} &\n')
    lf.write('\multicolumn{1}{|c|}{$\frac{E_1-E_2}{E_b}$} &\n')
    lf.write('\multicolumn{1}{|c|}{\# of Events} & \\ \hline\n')
    lf.write('For means p-value table:\n')
    lf.write('\begin{tabular}{|ccccccccll}\n\n \hline \n\multicolumn{8}{|c|}{Guinea Pig Means p-values Table} \\ \hline\n')
    lf.write('\multicolumn{1}{|c|}{Run \# 1, Run \# 2} &\n')
    lf.write('\multicolumn{1}{|c|}{$\frac{E_1}{E_b}$ p-values} &\n')
    lf.write('\multicolumn{1}{|c|}{$\frac{E_2}{E_b}$ p-values} &\n')
    lf.write('\multicolumn{1}{|c|}{$z_{pv}$ p-values} &\n')
    lf.write('\multicolumn{1}{|c|}{Time p-values} &\n')
    lf.write('\multicolumn{1}{|c|}{$\frac{\sqrt{s}}{\sqrt{s}_b}$ p-values} &\n')
    lf.write('\multicolumn{1}{|c|}{$\frac{E_1-E_2}{E_b}$ p-values} &\n')
    lf.write('\multicolumn{1}{|c|}{\# of Events p-values} & \\ \hline\n')
    lf.write('For correlations table:\n')
    lf.write('\begin{tabular}{|cccccccll}\n\n \hline \n\multicolumn{7}{|c|}{Guinea Pig Correlations Table} \\ \hline \n')
    lf.write('\multicolumn{1}{|c|}{Run \#} &\n')
    lf.write('\multicolumn{1}{|c|}{$E_1 E_2$ Corr.} &\n')
    lf.write('\multicolumn{1}{|c|}{$E_1 z_{pv}$ Corr.} &\n')
    lf.write('\multicolumn{1}{|c|}{$E_2 z_{pv}$ Corr.} &\n')
    lf.write('\multicolumn{1}{|c|}{$E_1$ $\sqrt{s}$ Corr.} &\n')
    lf.write('\multicolumn{1}{|c|}{$E_2$ $\sqrt{s}$ Corr.} &\n')
    lf.write('\multicolumn{1}{|c|}{$E_1 - E_2$ $z_{pv}$ Corr.}  \\ \hline\n')
    lf.write('For correlations p-value table:\n')
    lf.write('\begin{tabular}{|cccccccll}\n\n \hline \n\multicolumn{7}{|c|}{Guinea Pig Correlations p-values Table} \\ \hline \n')
    lf.write('\multicolumn{1}{|c|}{Run \# 1, Run \# 2} &\n')
    lf.write('\multicolumn{1}{|c|}{$E_1 E_2$ Corr. p-values} &\n')
    lf.write('\multicolumn{1}{|c|}{$E_1 z_{pv}$ Corr. p-values} &\n')
    lf.write('\multicolumn{1}{|c|}{$E_2 z_{pv}$ Corr. p-values} &\n')
    lf.write('\multicolumn{1}{|c|}{$E_1$ $\sqrt{s}$ Corr. p-values} &\n')
    lf.write('\multicolumn{1}{|c|}{$E_2$ $\sqrt{s}$ Corr. p-values} &\n')
    lf.write('\multicolumn{1}{|c|}{$E_1 - E_2$ $z_{pv}$ Corr. p-values}  \\ \hline\n')
    lf.write('\n')
    lf.write("Means table below\n")
    lf.write("\n")
    lf.write("\multicolumn{1}{|c|}{"+str(argv[1])+"}         &\n")
    lf.write("\multicolumn{1}{|c|}{"+str(argv[2]) + "}          &\n")
    lf.write("\multicolumn{1}{|c|}{"+str(argv[3])+","+str(argv[4])+"}        &\n")
    lf.write("\multicolumn{1}{|c|}{"+str("{:.4e}".format(dmave[0]))+"$\pm$"+str("{:.2e}".format(dmunc[0]))+"}     &\n")
    lf.write("\multicolumn{1}{|c|}{"+str("{:.4e}".format(dmave[1]))+"$\pm$"+str("{:.2e}".format(dmunc[1]))+"}     &\n")
    lf.write("\multicolumn{1}{|c|}{"+str("{:.4e}".format(dmave[4]))+"$\pm$"+str("{:.2e}".format(dmunc[4]))+"}     &\n")
    lf.write("\multicolumn{1}{|c|}{"+str("{:.4e}".format(dmave[5]))+"$\pm$"+str("{:.2e}".format(dmunc[5]))+"}     &\n")
    lf.write("\multicolumn{1}{|c|}{"+str("{:.4e}".format(dmave[6]))+"$\pm$"+str("{:.2e}".format(dmunc[6]))+"}     &\n")
    lf.write("\multicolumn{1}{|c|}{"+str("{:.4e}".format(dmave[7]))+"$\pm$"+str("{:.2e}".format(dmunc[7]))+"}     &\n")
    lf.write("\multicolumn{1}{|c|}{"+str("{:.4e}".format(dmave[8]))+"$\pm$"+str("{:.2e}".format(dmunc[8]))+"}     \\ \hline \n")    
    lf.write('\n')
    lf.write('Means p-value table below\n')
    lf.write('\n')
    lf.write('\multicolumn{1}{|c|}{'+str(argv[1])+','+str(argv[6])+'} &\n')
    lf.write('\multicolumn{1}{|c|}{'+str("{:.4e}".format(pvm[0][0]))+','+str("{:.4e}".format(pvm[0][1]))+'} &\n')
    lf.write('\multicolumn{1}{|c|}{'+str("{:.4e}".format(pvm[1][0]))+','+str("{:.4e}".format(pvm[1][1]))+'} &\n')
    lf.write('\multicolumn{1}{|c|}{'+str("{:.4e}".format(pvm[2][0]))+','+str("{:.4e}".format(pvm[2][1]))+'} &\n')
    lf.write('\multicolumn{1}{|c|}{'+str("{:.4e}".format(pvm[3][0]))+','+str("{:.4e}".format(pvm[3][1]))+'} &\n')
    lf.write('\multicolumn{1}{|c|}{'+str("{:.4e}".format(pvm[4][0]))+','+str("{:.4e}".format(pvm[4][1]))+'} &\n')
    lf.write('\multicolumn{1}{|c|}{'+str("{:.4e}".format(pvm[5][0]))+','+str("{:.4e}".format(pvm[5][1]))+'} &\n')
    lf.write('\multicolumn{1}{|c|}{'+str("{:.4e}".format(pvm[6][0]))+','+str("{:.4e}".format(pvm[6][1]))+'} \\ \hline \n')
    lf.write('\n')
    lf.write('Correlations table below\n')
    lf.write('\n')
    lf.write("\multicolumn{1}{|c|}{"+str(argv[1])+"}         &\n")
    lf.write("\multicolumn{1}{|c|}{"+str("{:.4e}".format(dcave[0]))+"$\pm$"+str("{:.2e}".format(dcunc[0]))+"}     &\n")
    lf.write("\multicolumn{1}{|c|}{"+str("{:.4e}".format(dcave[3]))+"$\pm$"+str("{:.2e}".format(dcunc[3]))+"}     &\n")
    lf.write("\multicolumn{1}{|c|}{"+str("{:.4e}".format(dcave[9]))+"$\pm$"+str("{:.2e}".format(dcunc[9]))+"}     &\n")
    lf.write("\multicolumn{1}{|c|}{"+str("{:.4e}".format(dcave[5]))+"$\pm$"+str("{:.2e}".format(dcunc[5]))+"}     &\n")
    lf.write("\multicolumn{1}{|c|}{"+str("{:.4e}".format(dcave[11]))+"$\pm$"+str("{:.2e}".format(dcunc[11]))+"}     &\n")
    lf.write("\multicolumn{1}{|c|}{"+str("{:.4e}".format(dcave[24]))+"$\pm$"+str("{:.2e}".format(dcunc[24]))+"}  \\ \hline \n")
    lf.write('\n')
    lf.write('Correlations p-value table below \n')
    lf.write('\n')
    lf.write('\multicolumn{1}{|c|}{'+str(argv[1])+','+str(argv[6])+'} &\n')
    lf.write('\multicolumn{1}{|c|}{'+str("{:.4e}".format(pvc[0][0]))+','+str("{:.4e}".format(pvc[0][1]))+'} &\n')
    lf.write('\multicolumn{1}{|c|}{'+str("{:.4e}".format(pvc[1][0]))+','+str("{:.4e}".format(pvc[1][1]))+'} &\n')
    lf.write('\multicolumn{1}{|c|}{'+str("{:.4e}".format(pvc[2][0]))+','+str("{:.4e}".format(pvc[2][1]))+'} &\n')
    lf.write('\multicolumn{1}{|c|}{'+str("{:.4e}".format(pvc[3][0]))+','+str("{:.4e}".format(pvc[3][1]))+'} &\n')
    lf.write('\multicolumn{1}{|c|}{'+str("{:.4e}".format(pvc[4][0]))+','+str("{:.4e}".format(pvc[4][1]))+'} &\n')
    lf.write('\multicolumn{1}{|c|}{'+str("{:.4e}".format(pvc[5][0]))+','+str("{:.4e}".format(pvc[5][1]))+'} \\ \hline \n')
    lf.write('\n')
#format follows this:
#\multicolumn{1}{|c|}{Run Number} & 
#\multicolumn{1}{l|}{Input Energy} & 
#\multicolumn{1}{l|}{$E_1$ Corr,$E_2$ Corr} & 
#\multicolumn{1}{c|}{Average $\frac{E_1}{E_b}$} & 
#\multicolumn{1}{l|}{Average $\frac{E_2}{E_b}$} & 
#\multicolumn{1}{l|}{$z_{pv}$ (um)} & 
#\multicolumn{1}{l|}{Time} & 
#\multicolumn{1}{l|}{$\frac{\sqrt{s}}{\sqrt{s}_b}$} & 
#\multicolumn{1}{l|}{$\frac{E_1-E_2}{E_b}$} & 
#\multicolumn{1}{l|}{\# of Events} & \\ \hline
#And then for the correlation table:
#\multicolumn{1}{l|}{$E_1 E_2$ Corr.} & 
#\multicolumn{1}{l|}{$E_1 z_{pv}$ Corr.} & 
#\multicolumn{1}{l|}{$E_2 z_{pv}$ Corr.} &
#\multicolumn{1}{l|}{$E_1$ $\sqrt{s}$ Corr.} &
#\multicolumn{1}{l|}{$E_2$ $\sqrt{s}$ Corr.} &
#\multicolumn{1}{l|}{$E_1 - E_2$ $z_{pv}$ Corr.}  \\ \hline
