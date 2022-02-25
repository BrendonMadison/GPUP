#!/bin/bash
#SBATCH --job-name=SMC               # Job name
#SBATCH --partition=wilson            # Partition Name (Required)
#SBATCH --mail-type=ALL               # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=b047m507@ku.edu   # Where to send mail
#SBATCH --ntasks=1                    # Run on a single CPU
#SBATCH --mem=1gb                     # Job memory request
#SBATCH --time=0-06:00:00             # Time limit days-hrs:min:sec
#SBATCH --output=SMC_%j.log          # Standard output and error log

RUN=$1
ENE=$2
ECORR=$3
PCORR=$4
DIR1=$5
DIR2=$6
OUTF=$7

echo 'Loading python3...'
module load python
echo 'Python3 loaded!'

WORKDIR=/panfs/pfs.local/work/wilson/b047m507/beamstats-main

cd ${WORKDIR}

pwd
hostname
date

squeue -u b047m507 >> tmptmp.txt
NUMLINES=$(wc -l < tmptmp.txt)
date

while [ $NUMLINES -ne 2 ]
do
  sleep 30
  echo ${NUMLINES}
  squeue -u b047m507 > tmptmp.txt
  NUMLINES=$(wc -l < tmptmp.txt)
done

rm tmptmp.txt
echo 'All GP jobs are done!'
echo 'Starting SMC analysis.'
date

python3 SMCsimple.py ${RUN} ${ENE} ${ECORR} ${PCORR} ${DIR1} ${DIR2} >> ${OUTF} 

echo 'SMC analysis done!'
date

exit
