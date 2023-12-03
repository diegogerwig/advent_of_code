#!/usr/bin/env python3

from string import digits

# with open("inp_test_a.txt") as f:
#     lines = f.read().split("\n")

# with open("inp_test_b.txt") as f:
#     lines = f.read().split("\n")

with open("inp.txt") as f:
    lines = f.read().split("\n")


#########################
###      PART A      ####
#########################

answer_a = 0

for line in lines:
    numbers = []
    
    for digit in digits:
        idx = line.find(digit)
        if idx != -1:
            numbers.append((idx, digit))
        idx = line.rfind(digit)
        if idx != -1:
            numbers.append((idx, digit))

    numbers.sort()
    answer_a += int(f"{numbers[0][1]}{numbers[-1][1]}")

print('ANSWER Part A -> ', answer_a)


#########################
###      PART B      ####
#########################

answer_b = 0
spelled = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

for line in lines:
    numbers = []
    for word, digit in spelled.items():
        idx = line.find(word)
        if idx != -1:
            numbers.append((idx, digit))
        idx = line.rfind(word)
        if idx != -1:
            numbers.append((idx, digit))
    for digit in digits:
        idx = line.find(digit)
        if idx != -1:
            numbers.append((idx, digit))
        idx = line.rfind(digit)
        if idx != -1:
            numbers.append((idx, digit))
   
    numbers.sort()
    answer_b += int(f"{numbers[0][1]}{numbers[-1][1]}")

print('ANSWER Part B -> ', answer_b)
