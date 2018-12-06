#!/bin/bash

ps aux | awk 'NR>2{arr[$1]+=$6}END{for(i in arr) print i,arr[i]/1024}' > Memory.txt