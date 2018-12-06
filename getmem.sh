#!/bin/bash

rm newmem.txt

for i in `awk -F'[/:]' '{if ($3 >= 1000 && $3 != 65534) print $1}' /etc/passwd`; 
do
    echo $i >> newmem.txt
    top -b -n 1 -u $i | awk 'NR>7 { sum += $10; } END { print sum; }' >> newmem.txt;
    echo;
done
