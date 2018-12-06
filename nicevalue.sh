#!/bin/bash

top -b -o +%MEM | head -n 12 | tail -n 5 | awk '{print $1, $3, $4, $10}' > nice.txt

