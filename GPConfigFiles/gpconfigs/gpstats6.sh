#!/bin/bash
#SBATCH --job-name=gpig               # Job name
#SBATCH --partition=wilson            # Partition Name (Required)
#SBATCH --mail-type=ALL               # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=b047m507@ku.edu   # Where to send mail	
#SBATCH --ntasks=1                    # Run on a single CPU
#SBATCH --mem=1gb                     # Job memory request
#SBATCH --time=0-06:00:00             # Time limit days-hrs:min:sec
#SBATCH --output=gpig_%j.log          # Standard output and error log

VER=$1
ENE=$2
ECORR=$3
PCORR=$4
ESPRD=$5
PSPRD=$6
TRUN=$7
NUM=$8
BEAMS=$9
SEED=${10}

echo 'Version '$VER
echo 'Energy '$ENE
echo 'Electron Correlation '$ECORR
echo 'Positron Correlation '$PCORR
echo 'Electron Spread '$ESPRD
echo 'Positron Spread '$PSPRD
echo 'Beamstrahlung '$BEAMS
echo 'Random seed '$SEED

echo 'Running job as '
echo 'User '$USER

pwd
hostname
date

echo 'PATH '
echo $PATH
 
echo 'LD_LIBRARY_PATH'
echo $LD_LIBRARY_PATH

module load fftw3
module list

echo 'Run Guinea-Pig++ script'
 
WORKG=/panfs/pfs.local/work/wilson/b047m507

DATDIR=${WORKG}/GPRuns/Run${VER}

mkdir ${DATDIR}

MYWDIR=${WORKG}/GPRuns/Run${VER}/Seed${SEED}
echo 'Creating directory '${MYWDIR}
mkdir ${MYWDIR}
MYXDIR=$WORKG/GPInstall/bin
MYCDIR=$WORKG/GPConfigFiles
MYCDIRG=/panfs/pfs.local/work/wilson/b047m507/GPConfigFiles/gpconfigs

sed 's/BEAMSTR/'$BEAMS'/' ${MYCDIRG}/acc-master.dat > ${MYCDIRG}/acc-tmp${VER}-${SEED}.dat
sed 's/SEEDSTR/'$SEED'/' ${MYCDIRG}/acc-tmp${VER}-${SEED}.dat > ${MYCDIRG}/acc-${VER}-${SEED}.dat
rm ${MYCDIRG}/acc-tmp${VER}-${SEED}.dat

echo 'Creating .ini beam files'

EFILE=${MYCDIRG}/ini/electron_${VER}_${SEED}.ini
PFILE=${MYCDIRG}/ini/positron_${VER}_${SEED}.ini

echo 'Electron file is ' ${EFILE}
echo 'Positron file is ' ${PFILE}

root -b -q ${MYCDIRG}/ini/MultivariateGaussian.C'("'${EFILE}'",1,'${ESPRD}','${ECORR}','${ENE}',0,'${TRUN}','${NUM}')'
root -b -q ${MYCDIRG}/ini/MultivariateGaussian.C'("'${PFILE}'",1,'${PSPRD}','${PCORR}','${ENE}',0,'${TRUN}','${NUM}')'

echo 'Script defines'
echo 'MYWDIR:  '${MYWDIR}
echo 'MYXDIR:  '${MYXDIR}
echo 'MYCDIR:  '${MYCDIR}
echo 'MYCDIRG: '${MYCDIRG}

cd ${MYWDIR}

echo 'Now in output directory '
pwd
echo 'Making symbolic links to control file and beam files'
ln -s ${MYCDIRG}/acc-${VER}-${SEED}.dat acc.dat
ln -s ${EFILE} electron.ini
ln -s ${PFILE} positron.ini

ls -lrt

echo 'Start execution'
date

accel=SETA_250GeV
parms=par
outfile=GPResults.out

echo "Accelerator " ${accel}
echo "Parameters  " ${parms}
echo "Results file " ${outfile}

${MYXDIR}/guinea ${accel} ${parms} ${outfile}

# Make a copy of the input file for posterity
cp acc.dat acc-Run${VER}-${SEED}.dat

date

echo "Running lumistats"

STATSDIR=${WORKG}/beamstats-main
STATSFILE=${MYWDIR}/Stats_${VER}_${SEED}.dat

echo "Output is " ${STATSFILE}

cd ${STATSDIR}

./checklumicorr ${ENE} ${MYWDIR}/lumi.ee.out ${MYWDIR}/Analysis_${VER}_${SEED} > ${STATSFILE}

cd ${MYWDIR}

cat *m.csv >> ../Datm.csv
cat *c.csv >> ../Datc.csv

#Clean up a bit by compressing output files
gzip *.out
#Compress *.dat files starting with b,c,h,m, or p characters like pairs.dat
gzip [bchmp]*.dat

date

#cd ${DATDIR}

#echo "Concatenating csv files to " ${DATDIR}

#cat *m.csv > ${DATDIR}/Datm.csv
#cat *c.csv > ${DATDIR}/Datc.csv

exit
