#!/bin/bash

rm newcpu.txt
for i in `awk -F'[/:]' '{if ($3 >= 1000 && $3 != 65534) print $1}' /etc/passwd`; 
do
    echo $i >> newcpu.txt
    top -b -n 1 -u $i | awk 'NR>7 { sum += $9; } END { print sum; }' >> newcpu.txt;
    echo;
done
