#! /bin/bash

# part 1
cat input.txt | paste -s -d "+" - | sed -e 's/++/\n/g' | sed -e 's/+$//g' | bc | sort -n | tail -n 1

# part 2
cat input.txt | paste -s -d "+" - | sed -e 's/++/\n/g' | sed -e 's/+$//g' | bc | sort -n | tail -n 3 | paste -s -d + - | bc
