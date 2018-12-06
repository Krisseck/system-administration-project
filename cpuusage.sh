#!/bin/bash

ps aux | awk 'NR>2{arr[$1]+=$3}END{for(i in arr) print i,arr[i] " % "}' > cpu.txt