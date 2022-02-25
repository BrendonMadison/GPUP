#!/bin/sh


#for i in {0..9}
#do

#sbatch gpstats5.sh 5130 125.0 0.3 0.3 0.00190 0.00152 3 80000 1 $((17+$i))
#sleep 30

#done

#for i in {0..9}
#do

#sbatch gpstats5.sh 5131 125.0 0.3 -0.3 0.00190 0.00152 3 80000 1 $((2+$i))
#sleep 30

#done

#for i in {0..9}
#do

#sbatch gpstats5.sh 5132 125.0 -0.3 0.3 0.00190 0.00152 3 80000 1 $((4+$i))
#sleep 30

#done

#for i in {0..9}
#do

#sbatch gpstats5.sh 5133 125.0 -0.3 -0.3 0.00190 0.00152 3 80000 1 $((23+$i))
#sleep 30
#sbatch gpstats6.sh 5090 125.0 0.9 0.9 0.00190 0.00152 3 80000 1 $((41+$i))
#sbatch gpstats6.sh 5091 125.0 0.9 -0.9 0.00190 0.00152 3 80000 1 $((84+$i))
#sbatch gpstats6.sh 5330 125.0 0.0 -0.3 0.00190 0.00152 3 80000 1 $((13+$i))
#
#done

echo 'Submitting GP jobs'

for i in {0..9}
do

sbatch gpstats6.sh 5171 123.0 0.0 0.0 0.00190 0.00152 3 80000 1 $((72+$i))
sleep 30

done

echo 'Submitting SMC job'

#sbatch launchSMC.sh 5090 125 0.9 0.9 ../GPRuns/Run5090 ../GPRuns/Run5060 ../GPRuns/Run5090/SMCsimpleOutput.txt
#sbatch launchSMC.sh 5330 125 0.0 -0.3 ../GPRuns/Run5330 ../GPRuns/Run5330 ../GPRuns/Run5330/SMCsimpleOutput.txt
sbatch launchSMC.sh 5171 123 0.0 0.0 ../GPRuns/Run5171 ../GPRuns/Run5060 ../GPRuns/Run5171/SMCsimpleOutput.txt

date

#for i in {0..9}
#do

#sbatch gpstats5.sh 5071 123.0 0.0 0.0 0.00190 0.00152 3 80000 1 $((6+$i))
#sleep 30

#done

#for i in {0..9}
#do

#sbatch gpstats5.sh 5072 122.0 0.0 0.0 0.00190 0.00152 3 80000 1 $((6+$i))
#sleep 30

#5060 is 3 sigma , 5020 is 20 sigma

#done

#sbatch gpstats2.sh 701 62.5 0.0 0.0 0.00190 0.00152 4 80000 1
#sbatch gpstats2.sh 702 250.0 0.0 0.0 0.00190 0.00152 4 80000 1
#sbatch gpstats2.sh 703 500.0 0.0 0.0 0.00190 0.00152 4 80000 1
#sbatch gpstats2.sh 704 1000.0 0.0 0.0 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 162 125.0 0.0 0.0 0.00190 0.00152 4 200000 1
#sbatch gpstats_launch.sh 163 124.0 0.0 0.0 0.00190 0.00152 4 200000 1
#sbatch gpstats_launch.sh 164 123.0 0.0 0.0 0.00190 0.00152 4 200000 1

#sbatch gpstats_launch.sh 30 125.0 0.3 0.3 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 31 125.0 -0.3 0.3 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 32 125.0 0.3 -0.3 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 33 125.0 -0.3 -0.3 0.00190 0.00152 4 80000 1

#sbatch gpstats_launch.sh 90 125.0 0.9 0.9 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 91 125.0 -0.9 0.9 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 92 125.0 0.9 -0.9 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 192 125.0 0.9 -0.9 0.001905 0.0015205 4 80000 1
#sbatch gpstats_launch.sh 93 125.0 -0.9 -0.9 0.00190 0.00152 4 80000 1

#sbatch gpstats_launch.sh 930 125.0 -0.9 0.3 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 931 125.0 -0.9 -0.3 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 932 125.0 0.9 -0.3 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 933 125.0 0.9 0.3 0.00190 0.00152 4 80000 1

#sbatch gpstats_launch.sh 393 125.0 0.3 0.9 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 392 125.0 0.3 -0.9 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 390 125.0 -0.3 0.9 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 391 125.0 -0.3 -0.9 0.00190 0.00152 4 80000 1

#sbatch gpstats_launch.sh 01 125.0 0.0 -0.9 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 02 125.0 0.0 0.9 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 03 125.0 0.0 0.3 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 04 125.0 0.0 -0.3 0.00190 0.00152 4 80000 1

#sbatch gpstats_launch.sh 05 125.0 -0.9 0.0 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 06 125.0 0.9 0.0 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 07 125.0 0.3 0.0 0.00190 0.00152 4 80000 1
#sbatch gpstats_launch.sh 08 125.0 -0.3 0.0 0.00190 0.00152 4 80000 1

exit
