#!/bin/bash

dirname=$1
filename=$2

file_arr=(ls -d ${dirname}/*)
file_arr=("${file_arr[@]:2}")
for (( i=0 ; i<$(( ${#file_arr[@]} - 1 )) ; i++ )); do
    echo "${file_arr[$i]} TO ${file_arr[$(( $i + 1 ))]}" >> $filename
    python3 imgCmp.py ${file_arr[$i]} ${file_arr[$(( $i + 1 ))]} \
	    >> $filename
    echo "" >> $filename
done
    
