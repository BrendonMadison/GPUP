# GPUP
Updated peripheral programs for GuineaPig

Allows for:  
  
1.) Multivariate normal initial states for electron and positron beams (.C file)  
2.) Turning on and off beamstrahlung  
3.) Compiling multiple runs into one result file (.f file)  
4.) Calculating mean and uncertainties of the results with a latex table output (.py file)  
5.) Calculate p-values of run statistics when compared to a "vanilla" run (Run 5060)  
6.) Shell script to automatically submit analysis job after GuineaPig jobs are done. Thus is entirely automatic.  
  
Designed to run on KU's HPC (slurm and linux based).  
  
Requires ROOT v6 , Python v3, GuineaPig, GNU Fortran 8.3.0
